from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File        import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.folders.User__Folders__Operations               import User__Folders__Operations
from cbr_shared.cbr_backend.users.User__Section_Data                        import User__Section_Data
from osbot_utils.helpers.Random_Guid                                        import Random_Guid

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
        return self.folders_structure.files.get(file_id)

    def file_name__folder_structure(self) -> str:                                              # Get file name for folder structure.
        return FILE_NAME__FOLDERS__STRUCTURE

    def folders_operations(self):
        return User__Folders__Operations(folders_structure=self.folders_structure)

    def load(self):                                                                        # Load existing structure
        folder_structure_data  = self.file_data(self.file_name__folder_structure())
        folders_structure      = Model__User__Folders__Structure.from_json(folder_structure_data)
        if folders_structure:
            self.folders_structure = folders_structure
        return self

    def load__raw_data(self):
        return self.file_data(self.file_name__folder_structure())

    def not_exists(self):
        return self.exists() is False

    def print(self):
        print()
        print(self.tree_view())

    def json_view(self):
        return self.folders_operations().json_view()

    def tree_view(self):
        return self.folders_operations().tree_view()

    def save(self) -> bool:                                                                 # Save folder structure to storage.
        return self.file_save(self.file_name__folder_structure(), self.folders_structure.json())

    def user_folder(self, user_folder_id: Random_Guid=None):
        if not user_folder_id:
            user_folder_id = self.folders_structure.root_id

        return self.folders_structure.folders.get(user_folder_id)