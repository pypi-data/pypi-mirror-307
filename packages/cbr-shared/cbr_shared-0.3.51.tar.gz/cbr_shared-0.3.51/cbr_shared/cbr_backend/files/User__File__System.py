from cbr_shared.cbr_backend.files.User__File        import User__File
from cbr_shared.cbr_backend.folders.User__Folders   import User__Folders
from cbr_shared.cbr_backend.users.S3_DB__User       import S3_DB__User
from cbr_shared.cbr_sites.CBR__Shared_Objects       import cbr_shared_objects
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.Random_Guid                import Random_Guid

class User__File__System(Type_Safe):
    db_user : S3_DB__User

    def add_file(self, file_name: str, file_bytes: bytes, user_folder_id: Random_Guid = None):
        with self.user_folders() as user_folders:
            user_folder = user_folders.user_folder(user_folder_id=user_folder_id)
            if user_folder:
                if user_folder_id is None:
                    user_folder_id = user_folder.folder_id                                              #

                user_file = User__File(db_user=self.db_user)
                user_file   .create  (file_bytes=file_bytes, file_name=file_name, user_folder_id=user_folder_id)
                user_folders.add_file(folder_id=user_folder_id, file_id=user_file.file_id, file_name=file_name)
                return user_file

    def add_folder(self, parent_folder_id=None, folder_name=None):
        with self.user_folders() as user_folders:
            return user_folders.add_folder(folder_name=folder_name, parent_folder_id=parent_folder_id)


    def delete_file(self, file_id):
        file = User__File(file_id=file_id, db_user=self.db_user)
        if file.exists():
            with self.user_folders() as user_folders:
                user_folders.delete_file(file_id=file_id)
            file.delete()
            return True

    def root_folder(self):
        return self.user_folders().root_folder()

    def tree_view(self):
        return self.user_folders().tree_view()

    @cache_on_self
    def user_files(self):
        return cbr_shared_objects.file

    @cache_on_self
    def user_folders(self):
        return User__Folders(db_user=self.db_user)

    def setup(self):
        if self.db_user is None:
            raise ValueError("in User__File__System.setup db_user cannot be None")

        if self.db_user.has__file_system() is False:                                    # if the file_system is not set of this user
            self.user_folders().setup()                                                 #     set up  the user_folders (which will create the user_folders_structure file and add a root folder)
            self.db_user.user_config__update_value('file_system', True)                 #     update the user_config object to set the file_system to True
        return self
