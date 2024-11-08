from cbr_shared.cbr_backend.folders.User__Folders__Tree_View                import User__Folders__Tree_View
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File        import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folder              import Model__User__Folder
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.folders.User__Folders__Operations               import User__Folders__Operations
from cbr_shared.cbr_backend.users.User__Section_Data                        import User__Section_Data
from osbot_utils.utils.Dev import pprint

SECTION__NAME__USER__FOLDERS   = 'user-folders'                                                                 # Section name for folders
FILE_NAME__FOLDERS__STRUCTURE  = 'folders-structure.json'                                                        # Storage file name

class User__Folders__Structure(User__Section_Data):
    folders_structure      : Model__User__Folders__Structure
    section_name           : str                             = SECTION__NAME__USER__FOLDERS                                # Section identifier

    def create(self):
        if self.not_exists():
            self.save()
        return self

    def delete(self) -> bool:                                                                     # Check if folder structure exists.
        return self.file_delete(self.file_name__folder_structure())

    def exists(self) -> bool:                                                               # Check if folder structure exists.
        return self.file_exists(self.file_name__folder_structure())

    def file(self, file_id) -> Model__User__Folder__File:                                          # Get folder by ID.
        return self.folders_structure.folders.get(file_id)

    def file_name__folder_structure(self) -> str:                                              # Get file name for folder structure.
        return FILE_NAME__FOLDERS__STRUCTURE

    def folders_operations(self):
        return User__Folders__Operations(folders_structure=self.folders_structure)

    def load(self) -> Model__User__Folders__Structure:                                                  # Load existing structure
        folder_structure_data  = self.file_data(self.file_name__folder_structure())
        self.folders_structure = Model__User__Folders__Structure.from_json(folder_structure_data)
        return self.folders_structure

    def load__raw_data(self):
        return self.file_data(self.file_name__folder_structure())

    def not_exists(self):
        return self.exists() is False

    def print(self):
        tree_view = self.folders_operations().tree_view()
        print()
        print(tree_view)

    def save(self) -> bool:                                                                 # Save folder structure to storage.
        return self.file_save(self.file_name__folder_structure(), self.folders_structure.json())