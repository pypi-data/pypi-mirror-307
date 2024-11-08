from cbr_shared.cbr_sites.CBR__Shared_Objects import cbr_shared_objects
from osbot_utils.utils.Status                 import status_ok

class Temp_DB_User:

    def __init__(self):
        self.db_users = cbr_shared_objects.db_users()
        self.db_users.s3().dont_use_threads()
        self.db_user  = self.db_users.random_db_user()

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        assert self.db_user.create() == status_ok()
        return self.db_user

    def delete(self):
        assert self.db_user.delete() is True