import hashlib
import json
import os
from datetime import datetime, timedelta
from multiprocessing import Lock
from multiprocessing.managers import SyncManager
from typing import Optional, Callable

import pyvista as pv
import requests
from pyvista import DataSet

from streamlit_pyvista import ENV_VAR_PREFIX, DEFAULT_CACHE_DIR
from streamlit_pyvista.helpers.streamlit_pyvista_logging import root_logger
from .utils import with_lock

DEFAULT_THRESHOLD = int(os.environ.get(ENV_VAR_PREFIX + "DECIMATION_THRESHOLD", 6000))
DEFAULT_TTL = int(os.environ.get(ENV_VAR_PREFIX + "CACHE_TTL_MINUTES", 60*24*90))
DEFAULT_VIEWER_CACHE_NAME = "viewer.py"


class SharedLockManager(SyncManager):
    pass


SharedLockManager.register('Lock', Lock)


def get_lock():
    manager = SharedLockManager()
    manager.start()
    return manager.Lock()


# Create a global lock
file_lock = get_lock()


def get_decimated_content(pv_mesh_instance: DataSet, file_ext: str) -> str:
    """
    This function extract the String that represent a mesh.

    Args:
        pv_mesh_instance (DataSet): The mesh from which you want to get the String representation.
        file_ext (str): The file extension of the mesh.

    Returns:
        str: A string representing the mesh.

    Note:
        It could be then be written in a file and read by pv.read function.
        This function is mainly copied from pv.DataDet.save method.
    """
    if pv_mesh_instance._WRITERS is None:
        raise NotImplementedError(f'{pv_mesh_instance.__class__.__name__} writers are not specified,'
                                  ' this should be a dict of (file extension: vtkWriter type)')

    if file_ext not in pv_mesh_instance._WRITERS:
        raise ValueError('Invalid file extension for this data type.'
                         f' Must be one of: {pv_mesh_instance._WRITERS.keys()}')

    # store complex and bitarray types as field data
    pv_mesh_instance._store_metadata()

    writer = pv_mesh_instance._WRITERS[file_ext]()
    writer.SetInputData(pv_mesh_instance)
    writer.SetWriteToOutputString(1)
    writer.Write()
    return writer.GetOutputString()


def decimated_mesh_from_file(mesh: pv.DataSet, save_dir: str, decimation_factor: float = 0.5) -> str:
    """
    Decimate a mesh and store it in a file.

    Args:
        mesh (pv.DataSet): The mesh you want to decimate.
        save_dir (str): The directory in which to save the decimated mesh.
        decimation_factor (float, optional): The reduction factor to aim for. Defaults to 0.5.
            E.g., if decimation_factor = 0.25 and the initial mesh has 1000 cells,
            the resulting mesh will have 750 cells.

    Returns:
        str: The path to the decimated mesh.

    Note:
        For more information about decimation using PyVista, see:
        https://docs.pyvista.org/version/stable/examples/01-filter/decimate#decimate-example
    """
    pv_mesh = mesh.triangulate().extract_geometry().decimate(decimation_factor, attribute_error=True).sample(mesh)
    content = get_decimated_content(pv_mesh, ".vtk")
    checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()
    save_path = f"{save_dir}/{checksum}.vtk"
    if not os.path.exists(save_path):
        pv_mesh.save(save_path)
    return save_path


def compute_decimation_factor(current_nbr_points: float, target_nbr_points: float) -> float:
    """
    Compute the decimation reduction factor required to get to a target size number of points.

    Args:
        current_nbr_points(float): The number of points of the initial mesh.
        target_nbr_points(float): The number of points aimed after decimation.

    Returns:
        float: The decimation_factor required to reach the target
    """
    return min(1 - target_nbr_points / current_nbr_points, 1.0)


@with_lock(lock=file_lock)
def save_file_content(file_content: bytes, save_path: str, ttl_minutes: int = DEFAULT_TTL,
                      process_func: Optional[Callable] = None,
                      process_args: Optional[dict] = None) -> tuple[str, Optional[str]]:
    """
    Save file content to a cache, optionally process it, and return the path.

    Args:
        file_content(bytes): Content of the file to save in the cache
        save_path(str): {Cache directory}/{filename} to ideally store the content. The checksum will be added to
        the filename
        ttl_minutes(int): Time to live of the element in the cache
        process_func(Optional[Callable]): Optional function to process the file (e.g., decimation for meshes)
        process_args(Optional[dict]): Optional arguments for the process_func

    Returns:
        tuple[str, Optional[str]]: A tuple with The path to the saved file and its processed version if there exists one

    Note:
        The cache works as follows:
            - The hash of content passed as argument is computed. If one entry with the same hash exists already in the\
            cache json, we take the file that was stored in it (we try to take the processed one if it exists) and we\
            update the last access time to avoid deleting it if it was recently used
            - If the hash is not in the cache then a new entry is created and the content is processed with the\
            function passed as parameter if there is one
            - Then the function return the path to the processed file in priority and to the original file if no\
            processing happened
    """
    # Compute checksum and create the cache directory
    checksum = hashlib.sha256(file_content).hexdigest()

    # Get all relevant data of the filename and generate a new unique one
    directory, filename = os.path.split(save_path)
    os.makedirs(directory, exist_ok=True)
    name, extension = os.path.splitext(filename)
    filename = f"{name}_{checksum}{extension}"
    file_path = os.path.join(directory, filename)

    # Load or initialize checksums
    checksum_file = os.path.join(directory, "checksums.json")
    if os.path.exists(checksum_file):
        with open(checksum_file, 'r') as f:
            try:
                checksums = json.load(f)
            except json.JSONDecodeError:
                checksums = {}
    else:
        checksums = {}

    valid_entries = list(filter(lambda x: x[1]["checksum"] == checksum, checksums.items()))

    # Check if file exists in cache
    if len(valid_entries) > 0:
        filename = valid_entries[0][0]
        checksums[filename]["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(directory, filename)
        if checksums[filename]["processed_path"] is not None:
            result_path = file_path, checksums[filename]["processed_path"]
        else:
            result_path = file_path, None
        root_logger.debug(f"Cache - Found a file with matching checksum: {result_path}")
    else:
        # Save new file
        root_logger.debug(f"Cache - No matching file already stored, writing {filename} to {file_path}")
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Process file if function provided
        processed_path = None
        if process_func and callable(process_func):
            processed_path = process_func(file_path, directory, **(process_args or {}))
            root_logger.debug(f"Cache - Processed the file with the following arguments: {process_args}")

        # Create new entry in cache
        checksums[filename] = {"checksum": checksum, "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "ttl_minutes": ttl_minutes, "processed_path": processed_path}

        # Set result path
        result_path = (file_path, processed_path) if processed_path else (file_path, None)
        root_logger.debug(f"Cache - Created new cache entry an returning the following path: {result_path}")
    # Update cache state in file
    with open(checksum_file, 'w') as f:
        json.dump(checksums, f, indent=4)

    return result_path


def process_mesh(file_path: str, save_dir: str, decimation_factor: float, decimation_threshold: int) -> Optional[str]:
    """
    Decimate a mesh and store it in a file

    Args:
        file_path(str): The path to the mesh to decimate
        save_dir(str): The directory in which we should save the decimated mesh
        decimation_factor(float): The reduction factor to aim. e.g. decimation_factor = 0.25, initial mesh number of
        cells 1000 -> resulting mesh will have 750 cells
        decimation_threshold(int): The threshold under which we don't decimate the mesh
    Returns:
        Optional[str]: the path to the decimated mesh or None if the mesh is under the decimation threshold
    """
    m = pv.read(file_path)
    nbr_points = m.GetNumberOfCells()
    # If the number of points is already below the threshold, we don't decimate
    if nbr_points < decimation_threshold:
        return None
    if not decimation_factor:
        decimation_factor = compute_decimation_factor(nbr_points, DEFAULT_THRESHOLD)
    root_logger.debug(
        f"Cache - Processing mesh with {nbr_points} points and using a decimation factor of {decimation_factor}")
    return decimated_mesh_from_file(m, save_dir, decimation_factor)


def save_mesh_content(mesh_content: bytes, save_dir: str, ttl_minutes: int = DEFAULT_TTL,
                      decimation_factor: float = None,
                      decimation_threshold: int = DEFAULT_THRESHOLD) -> tuple[str, Optional[str]]:
    """
    Save mesh content to a cache, optionally decimate it, and return the path.

    Args:
        mesh_content(bytes): content of the mesh
        save_dir(str): {Cache directory}/{filename} to ideally store the content. The checksum will be added to the
        filename.
        ttl_minutes(int): Time to live of the element in the cache
        decimation_factor(float): The reduction factor to aim. e.g. decimation_factor = 0.25, initial mesh number of
        cells 1000
            -> resulting mesh will have 750 cells
        decimation_threshold(int): The threshold under which we don't decimate the mesh

    Returns
        str: The path to file decimated or not (depending on the threshold) in the cache
    """
    process_args = {"decimation_factor": decimation_factor, "decimation_threshold": decimation_threshold}
    return save_file_content(mesh_content, save_dir, ttl_minutes, process_mesh, process_args)


def save_mesh_content_from_url(url: str, save_path: str, ttl_minutes: int = DEFAULT_TTL,
                               decimation_factor: float = None,
                               decimation_threshold: int = DEFAULT_THRESHOLD) -> tuple[Optional[str], Optional[str]]:
    """
    Save mesh content from a URL to a cache, optionally decimate it, and return the path.

    Args:
        url(str): URL to the mesh
        save_path(str): {Cache directory}/{filename} to ideally store the content. The checksum will be added to
        the filename
        ttl_minutes(int): Time to live of the element in the cache
        decimation_factor(float): The reduction factor to aim. e.g. decimation_factor = 0.25, initial mesh number of
        cells 1000 -> resulting mesh will have 750 cells
        decimation_threshold(int): The threshold under which we don't decimate the mesh
    Returns
        Optional[str]: The path to file decimated or not (depending on the threshold) in the cache
    """
    response = requests.get(url)
    if response.status_code != 200:
        return None, None
    root_logger.debug(f"Cache - Saving {url} in the cache...")
    process_args = {"decimation_factor": decimation_factor, "decimation_threshold": decimation_threshold}
    return save_file_content(response.content, save_path, ttl_minutes, process_mesh, process_args)


def save_mesh_content_from_file(path: str, save_path: str, ttl_minutes: int = DEFAULT_TTL,
                                decimation_factor: float = None,
                                decimation_threshold: int = DEFAULT_THRESHOLD) -> tuple[Optional[str], Optional[str]]:
    """
    Save mesh content from a file to a cache, optionally decimate it, and return the path.

    Args:
        path(str): Path to the mesh file
        save_path(str): {Cache directory}/{filename} to ideally store the content. The checksum will be added to
        the filename
        ttl_minutes(str): Time to live of the element in the cache
        decimation_factor(float): The reduction factor to aim. e.g. decimation_factor = 0.25, initial mesh number of
        cells 1000 -> resulting mesh will have 750 cells
        decimation_threshold(int): The threshold under which we don't decimate the mesh
    Returns
        Optional[str]: The path to file decimated or not (depending on the threshold) in the cache
    """
    if not os.path.exists(path):
        return None, None
    with open(path, "rb") as f:
        content = f.read()
    root_logger.debug(f"Cache - Saving {path} in the cache...")
    process_args = {"decimation_factor": decimation_factor, "decimation_threshold": decimation_threshold}
    return save_file_content(content, save_path, ttl_minutes, process_mesh, process_args)


def update_cache(cache_directory: str = DEFAULT_CACHE_DIR):
    """
    Update the cache by removing entries that are out of ttl

    Args:
        cache_directory(str): The directory in which the cache is stored
    """
    # Open the cache file
    checksum_file = os.path.join(cache_directory, "checksums.json")
    if not os.path.exists(checksum_file):
        return

    with open(checksum_file, 'r') as f:
        try:
            checksums = json.load(f)
        except json.JSONDecodeError:
            return

    # Check if the entries are still valid
    current_time = datetime.now()
    keys_to_remove = []
    for filename, entry in checksums.items():
        last_used = datetime.strptime(entry["last_used"], "%Y-%m-%d %H:%M:%S")
        ttl_minutes = entry["ttl_minutes"]
        if current_time - last_used > timedelta(minutes=ttl_minutes):
            keys_to_remove.append((filename, entry.get("processed_path", None)))

    root_logger.debug(
        f"Cache - Update cache: found {len(keys_to_remove)} invalid entries. Trying to remove "
        f"{', '.join(list(map(lambda x: x[0], keys_to_remove)))}")
    # Remove the keys of old entries
    for key in keys_to_remove:
        if os.path.exists(os.path.join(cache_directory, key[0])):
            os.remove(os.path.join(cache_directory, key[0]))
        if key[1] is not None and os.path.exists(os.path.join(cache_directory, key[1])):
            os.remove(os.path.join(cache_directory, key[1]))
        root_logger.debug(f"Cache - Removed {key[0]} from cache")
        del checksums[key[0]]

    # Rewrite the checksums.json file
    with open(checksum_file, 'w') as f:
        json.dump(checksums, f, indent=4)
