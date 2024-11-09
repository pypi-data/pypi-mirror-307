
from cbr_shared.cbr_backend.folders.Temp_Folder_Structure__Generator        import Temp_Folder_Structure__Generator
from cbr_shared.cbr_backend.folders.User__Folders__Structure                import User__Folders__Structure
from cbr_shared.cbr_backend.folders.User__Folders__Operations               import User__Folders__Operations
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.users.S3_DB__User                               import S3_DB__User
from cbr_shared.cbr_backend.users.Temp_DB_User                              import Temp_DB_User
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe



class Temp_Folders_Structure(Type_Safe):
    folders_structure       : Model__User__Folders__Structure  = None
    user_folders_operations : User__Folders__Operations        = None
    user_folders_structure  : User__Folders__Structure         = None
    temp_folder_generator   : Temp_Folder_Structure__Generator = None
    temp_user               : S3_DB__User                      = None
    delete_temp_user        : bool                             = False

    def __enter__(self):
        self.create()
        return self.user_folders_structure

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        if self.user_folders_structure is None:
            if self.temp_user is None:
                self.temp_user          = Temp_DB_User().create()
                self.delete_temp_user   = True
            self.user_folders_structure = User__Folders__Structure(db_user=self.temp_user)
            self.folders_structure      = self.user_folders_structure.folders_structure
        if self.user_folders_structure.not_exists():
            self.user_folders_structure.create()
        self.user_folders_operations = self.user_folders_structure.folders_operations()
        self.temp_folder_generator   = Temp_Folder_Structure__Generator(folders_structure=self.folders_structure)
        return self

    def create_folder_structure__with_multiple_folders_and_files(self):
        self.temp_folder_generator.create_folder_structure__with_multiple_folders_and_files()
        self.user_folders_structure.save()

    def delete(self):
        self.user_folders_structure.delete()
        if self.delete_temp_user:
            self.temp_user.delete()