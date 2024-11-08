from cbr_shared.cbr_backend.folders.User__Folders__Structure                import User__Folders__Structure
from cbr_shared.cbr_backend.users.S3_DB__User                               import S3_DB__User
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self

class User__Folders(Type_Safe):
    db_user             : S3_DB__User


    def add_folder(self, parent_folder_id=None, folder_name=None, ):
        return self.user_folders_operations().add_folder__to_folder_id(parent_folder_id=parent_folder_id, folder_name=folder_name)

    def add_file(self, folder_id, file_id=None, file_name=None):
        return self.user_folders_operations().add_file__to_folder_id(folder_id=folder_id, file_id=file_id, file_name=file_name)

    @cache_on_self
    def folders_structure(self):
        return self.user_folders_structure().folders_structure

    @cache_on_self
    def user_folders_structure(self):
        return User__Folders__Structure(db_user=self.db_user)

    @cache_on_self
    def user_folders_operations(self):
        return self.user_folders_structure().folders_operations()

    def root_folder__id(self):
        return self.folders_structure().root_id

    def setup(self):
        self.user_folders_structure().create()
        if self.root_folder__id() is None:
            self.user_folders_structure().folders_operations().create_root()
        return self

    def tree_view(self):
        return self.user_folders_operations().tree_view()
