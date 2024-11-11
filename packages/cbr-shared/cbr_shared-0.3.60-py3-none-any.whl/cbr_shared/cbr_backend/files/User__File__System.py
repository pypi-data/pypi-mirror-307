from cbr_shared.cbr_backend.files.User__File                 import User__File
from cbr_shared.cbr_backend.folders.User__Folders            import User__Folders
from cbr_shared.cbr_backend.folders.User__Folders__JSON_View import User__Folders__JSON_View
from cbr_shared.cbr_backend.users.S3_DB__User                import S3_DB__User
from osbot_utils.base_classes.Type_Safe                      import Type_Safe
from osbot_utils.decorators.methods.cache_on_self            import cache_on_self
from osbot_utils.helpers.Random_Guid                         import Random_Guid


class User__File__System(Type_Safe):
    db_user : S3_DB__User

    def add_file(self, file_name: str, file_bytes: bytes, user_folder_id: Random_Guid = None):
        with self.user_folders() as user_folders:
            user_folder = user_folders.user_folder(user_folder_id=user_folder_id)
            if user_folder:
                if not user_folder_id:
                    user_folder_id = user_folder.folder_id                                              #

                user_file = User__File(db_user=self.db_user)
                user_file   .create  (file_bytes=file_bytes, file_name=file_name, user_folder_id=user_folder_id)
                user_folders.add_file(folder_id=user_folder_id, file_id=user_file.file_id, file_name=file_name)
                return user_file

    def add_folder(self, parent_folder_id=None, folder_name=None):
        with self.user_folders() as user_folders:
            return user_folders.add_folder(folder_name=folder_name, parent_folder_id=parent_folder_id)

    def delete(self):
        self.user_folders().user_folders_structure().delete()
        self.db_user.user_config__update_value('file_system', False)                # todo: review this user_config.file_system set to False, since at the moment it is not consistent with way that True value is set
        return True

    def delete_file(self, file_id):
        file = User__File(file_id=file_id, db_user=self.db_user)
        if file.exists():
            with self.user_folders() as user_folders:
                user_folders.delete_file(file_id=file_id)
            file.delete()
            return True

    def delete_folder(self, folder_id):
        with self.user_folders() as user_folders:
            return user_folders.delete_folder(folder_id=folder_id)


    def file(self, file_id: Random_Guid):
        return User__File(db_user=self.db_user, file_id=file_id)

    def file__data(self, file_id: Random_Guid):
        return self.file(file_id).data()

    def file__contents(self, file_id: Random_Guid):
        file = self.file(file_id)
        if file.exists():
            file_data = self.file__data(file_id).json()
            file_contents = file.contents()
            return dict(file_data=file_data, file_contents=file_contents)
        return {}

    def folder(self, user_folder_id: Random_Guid):
        return self.user_folders().user_folder(user_folder_id)

    def folder_structure(self):
        return self.user_folders().folders_structure()

    def folder_structure__files(self):
        return self.folder_structure().files

    def root_folder(self):
        return self.user_folders().root_folder()

    def json_view(self):
        return User__Folders__JSON_View(folders_structure=self.folder_structure()).to_json()

    def tree_view(self):
        return self.user_folders().tree_view()


    @cache_on_self
    def user_folders(self):
        return User__Folders(db_user=self.db_user)

    def setup(self):
        if self.db_user is None:
            raise ValueError("in User__File__System.setup db_user cannot be None")
        self.user_folders().setup()
        return self
