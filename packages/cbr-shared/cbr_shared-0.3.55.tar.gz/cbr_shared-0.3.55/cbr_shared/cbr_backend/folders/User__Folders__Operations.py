from typing                                                                  import List
from cbr_shared.cbr_backend.folders.User__Folders__Tree_View                 import User__Folders__Tree_View
from cbr_shared.cbr_backend.folders.models.Model__User__Folder               import Model__User__Folder
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File         import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure   import Model__User__Folders__Structure
from osbot_utils.base_classes.Type_Safe                                      import Type_Safe
from osbot_utils.helpers.Random_Guid                                         import Random_Guid
from osbot_utils.helpers.Safe_Id                                             import Safe_Id
from osbot_utils.utils.Misc                                                  import random_text

USER_FOLDER__NAME__ROOT = 'root'

class User__Folders__Operations(Type_Safe):
    folders_structure      : Model__User__Folders__Structure

    def file(self, file_id):
        return self.folders_structure.files.get(file_id)

    def file__add(self, folder: Model__User__Folder, file_id: Random_Guid=None, file_name: Safe_Id=None) -> Model__User__Folder__File:
        if folder is None:
            raise ValueError(f"in User__Folders__Operations.file__add folder cannot be None")
        if not file_id: file_id = Random_Guid()
        if not file_name: file_name = random_text('file_name')
        if file_id in self.folders_structure.files:
            raise ValueError(f"in User__Folders__Operations.file__add there was already a file mapping with id: {file_id} ")
        kwargs = dict(file_id    = file_id          ,
                      file_name  = file_name        ,
                      folder_id  = folder.folder_id )
        folder_file = Model__User__Folder__File(**kwargs)
        self.folders_structure.files[file_id] = folder_file
        folder.files.append(file_id)

        return folder_file

    def file__add__to_folder_id(self, folder_id: Random_Guid, file_id: Random_Guid = None, file_name: Safe_Id = None) -> Model__User__Folder__File:
        if not folder_id:
            folder_id = self.folders_structure.root_id
        folder = self.folders_structure.folders.get(folder_id)
        if not folder:
            raise ValueError(f"In User__Folders__Operations.add_file__to_folder_id Could not find target folder with id: {folder_id}")
        return self.file__add(folder=folder, file_id=file_id, file_name=file_name)

    def file__delete(self, file_id):
        file = self.file(file_id)
        if file:
            folder_id = file.folder_id
            folder    = self.folder(folder_id)
            if folder:
                folder.files.remove(file_id)
                del self.folders_structure.files[file_id]
                return True
        return False

    def file__exists(self, file_id):
        return self.file(file_id) is not None

    def folder(self, folder_id):
        return self.folders_structure.folders.get(folder_id)

    def folder__add(self, parent_folder: Model__User__Folder, folder_name) -> Model__User__Folder:
        if parent_folder is None:
            raise ValueError(f"in User__Folders__Operations.folder__add folder cannot be None")
        new_folder    = Model__User__Folder(folder_name=folder_name, parent_id=parent_folder.folder_id)
        new_folder_id = new_folder.folder_id
        parent_folder         .folders.append(new_folder_id)                        # add reference to parent folder
        self.folders_structure.folders[new_folder_id] = new_folder                  # add object to folders_structure
        return new_folder

    def folder__add__to_folder_id(self, parent_folder_id=None, folder_name=None):
        if not parent_folder_id:
            parent_folder_id = self.folders_structure.root_id
        parent_folder = self.folders_structure.folders.get(parent_folder_id)
        if not parent_folder:
            raise ValueError(f"In User__Folders__Operations.add_folder__to_folder_id Could not find target folder with id: {parent_folder_id}")
        return self.folder__add(parent_folder=parent_folder,folder_name=folder_name)

    def folder__delete(self, folder_id):
        folder = self.folder(folder_id)
        if folder:
            for file_id in folder.files:
                file = self.file(file_id)
                if file:
                    if file.folder_id == folder_id:
                        raise ValueError(f"File {file_id} is still referencing folder {folder_id}")
            parent_folder = self.folder(folder.parent_id)
            if parent_folder:
                parent_folder.folders.remove(folder_id)
            del self.folders_structure.folders[folder_id]
            return True
        return False

    def folder__root(self):
        return self.folders_structure.folders.get(self.folders_structure.root_id)


    def files(self, file_id):
        return self.folders_structure.files

    def create_root(self, root_name=USER_FOLDER__NAME__ROOT) -> Model__User__Folder:
        folder = Model__User__Folder(folder_name=root_name)
        with self.folders_structure as _:
            _.folders[folder.folder_id] = folder
            _.root_id                   = folder.folder_id
        return folder

    def folder__children(self, structure: Model__User__Folders__Structure, folder_id: Random_Guid) -> List[Random_Guid]: # Get direct child folder IDs.
        if folder_id not in structure.folders:
            raise ValueError(f"Folder {folder_id} not found")

        return [fid for fid, folder in structure.folders.items()
                if folder.parent_id == folder_id]

    def folder__files(self, structure: Model__User__Folders__Structure, folder_id: Random_Guid) -> List[Random_Guid]:       # Get files in folder
        if folder_id not in structure.folders:
            raise ValueError(f"Folder {folder_id} not found")

        return [file_id for file_id, location in structure.files.items()
                if location.folder_id == folder_id]

    def folder__path(self, structure: Model__User__Folders__Structure, folder_id: Random_Guid) -> List[Random_Guid]:        # Get folder path from root."""
        if folder_id not in structure.folders:
            raise ValueError(f"Folder {folder_id} not found")

        path    = []
        current = folder_id
        visited = set()

        while current:
            if current in visited:
                raise ValueError(f"Circular dependency detected in path to {folder_id}")
            path   .append(current)
            visited.add(current)
            folder = structure.folders.get(current)
            if not folder:
                break
            current = folder.parent_id

        return list(reversed(path))

    def structure__reachable_folders(self, structure: Model__User__Folders__Structure, start_id: str, max_depth: int) -> set: # Get folders within depth limit
        if start_id not in structure.folders:
            raise ValueError(f"Start folder {start_id} not found")

        reachable = {start_id}
        if max_depth != 0:
            current_depth = 0
            current_level = {start_id}

            while current_level and (max_depth == -1 or current_depth < max_depth):
                next_level = set()
                for folder_id in current_level:
                    children = self.folder__children(structure, folder_id)
                    next_level.update(children)
                reachable.update(next_level)
                current_level = next_level
                current_depth += 1

        return reachable

    def tree_view(self):
        return User__Folders__Tree_View(folders_structure=self.folders_structure).tree_view()