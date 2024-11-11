from cbr_shared.cbr_backend.users.S3_DB__User   import S3_DB__User
from osbot_utils.base_classes.Type_Safe         import Type_Safe
from osbot_utils.utils.Http                     import url_join_safe

class User__Section_Data(Type_Safe):
    db_user  : S3_DB__User
    section_name: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.db_user.not_exists():                                       # If the user doesn't exist we can't use this class
            raise ValueError("User__Section_Data: db_user not found")
        if not self.section_name:                                           # a section name also needs to be set
            raise ValueError("User__Section_Data: section_name not defined")

    def file_bytes  (self, path      ): return self.db_user.s3_file_bytes       (s3_key=self.s3_key(path)                   )
    def file_data   (self, path      ): return self.db_user.s3_file_data        (s3_key=self.s3_key(path)                   )
    def file_delete (self, path      ): return self.db_user.s3_file_delete      (s3_key=self.s3_key(path)                   )
    def file_exists (self, path      ): return self.db_user.s3_file_exists      (s3_key=self.s3_key(path)                   )
    def file_save   (self, path, data): return self.db_user.s3_save_data        (s3_key=self.s3_key(path), data=data        )

    def folder_all_files(self, folder='' , full_path=False):
        return self.db_user.s3_folder_files__all(folder=self.s3_key(folder), full_path=full_path)

    def user_id(self):
        return self.db_user.user_id

    def section_folder_files_all(self):
        return self.db_user.s3_folder_files__all(self.section_root_folder(), full_path=True)

    def section_folder_list(self):
        return self.db_user.s3_folder_list(self.section_root_folder())

    def s3_key(self, path):
        return url_join_safe(self.section_root_folder(), path)

    def section_root_folder(self):
        return url_join_safe(self.db_user.s3_folder_user_data(), self.section_name)