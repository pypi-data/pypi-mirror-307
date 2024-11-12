from typing import Optional

import pyvista as pv

from streamlit_pyvista.helpers.cache import save_mesh_content_from_file, save_mesh_content_from_url
from streamlit_pyvista.helpers.utils import is_web_link


class LazyMesh:
    """
    LazyMesh is a class that is a pyvista mesh container that loads the mesh only when its first requested
    """

    def __init__(self, path, target_path):
        self.path = path
        self.target_path = target_path
        self._is_available = False
        self._full_mesh = None
        self._decimated_mesh = None
        self._expect_decimated = True

    def _load_mesh(self) -> pv.DataSet:
        """
        This function load the mesh after having inserted it in the cache

        Returns:
            pv.DataSet: the decimated mesh if it exists else the original mesh
        """
        if is_web_link(self.path):
            full_mesh_path, decimated_mesh_path = save_mesh_content_from_url(self.path, self.target_path)
        else:
            full_mesh_path, decimated_mesh_path = save_mesh_content_from_file(self.path, self.target_path)
        self._full_mesh = pv.read(full_mesh_path)
        self._is_available = True
        if decimated_mesh_path:
            self._decimated_mesh = pv.read(decimated_mesh_path)
            return self._decimated_mesh
        return self._full_mesh

    def set_decimated_as_default(self, v):
        """
        Set the default version of the mesh that is return by the mesh property
        """
        self._expect_decimated = v

    @property
    def is_available(self) -> bool:
        """
        Define whether the mesh was already loaded

        Returns:
            bool: True if the mesh is available, False otherwise
        """
        return self._is_available

    def has_decimated(self) -> bool:
        """
        Get if the mesh has a decimated version of it

        Returns:
            bool: True if the mesh has a decimated version of it, and False if it doesn't or if it still wasn't loaded
        """
        if self._is_available and self._decimated_mesh:
            return True
        return False

    def decimated_mesh(self) -> pv.DataSet:
        """
        Try to get the decimated version of the mesh

        Returns:
            pv.DataSet: The decimated version of the mesh, and if it doesn't exist, return the original version
            of the mesh
        """

        if self._decimated_mesh:
            return self._decimated_mesh

        if self._full_mesh:
            return self._full_mesh

        return self._load_mesh()

    @property
    def full_mesh(self) -> pv.DataSet:
        """
        Get the original version of the mesh

        Returns:
            pv.DataSet: The original(without any decimation applied) version of the mesh
        """
        if self._full_mesh:
            return self._full_mesh

        return self._load_mesh()

    @property
    def mesh(self) -> pv.DataSet:
        """
        Get the mesh requested by the user. It automatically chose the best one depending if the decimated mesh exists
        and if the user asked for the decimated on with the set_decimated_as_default function

        Returns:
            pv.DataSet: Get the mesh preferred by the user if possible. If not, just returns the original mesh
        """
        if self._decimated_mesh and self._expect_decimated:
            return self._decimated_mesh

        if self._full_mesh:
            return self._full_mesh

        return self._load_mesh()


class LazyMeshList(list[Optional[LazyMesh]]):
    """
    LazyMeshList class is child of the list class designed to contain None or LazyMesh, and to support certain features
    of the LazyMesh such as setting default version of mesh requested for the whole list or checking if a specific item
    possess a decimated version of the mesh
    """

    def __init__(self):
        super().__init__()
        self._expect_decimated = True
        self.loaded_count = 0

    def set_show_decimated(self, v):
        """
        Set behaviour of the list, if true then all item retrieve will be decimated mesh, else the list
        will return original version of the mesh
        """
        self._expect_decimated = v

    def load_mesh(self, index: int):
        m: Optional[LazyMesh] = super().__getitem__(index)
        if m is not None:
            m._load_mesh()
            return m
        return None

    def __getitem__(self, item: int) -> Optional[pv.DataSet]:
        """
        Get the mesh at a specific index

        Args:
            item (int): Index accessed

        Returns:
            Optional[pv.DataSet]: The mesh (decimated or not depending on what was defined with set_show_decimated)
            at the index specified
        """
        m: LazyMesh = super().__getitem__(item)
        if m is None:
            return m
        m.set_decimated_as_default(self._expect_decimated)
        if not m.is_available:
            self.loaded_count += 1

        return m.mesh

    def has_decimated_version(self, idx: int) -> bool:
        """
        Get whether the mesh at an index has a decimated version of itself

        Returns:
            bool: True if the mesh has a decimated version, False if it doesn't of if the mesh is None
        """
        m = super().__getitem__(idx)
        if m is None:
            return False
        return m.has_decimated()

    def number_mesh_loaded(self) -> int:
        """
        Get the number of loaded meshes in the list

        Returns:
            int: The count of loaded meshes
        """
        return self.loaded_count

    def __len__(self) -> int:
        return super().__len__()
