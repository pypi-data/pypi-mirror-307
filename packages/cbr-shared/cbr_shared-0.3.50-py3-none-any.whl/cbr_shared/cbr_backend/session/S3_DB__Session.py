from cbr_shared.cbr_sites.CBR__Shared__Constants            import COOKIE_NAME__CBR__SESSION_ID__ACTIVE
from cbr_shared.schemas.data_models.Model__Session__Config  import Model__Session__Config
from osbot_utils.utils.Http                                 import url_join_safe
from cbr_shared.cbr_backend.cbr.S3_DB__CBR                  import S3_DB__CBR
from osbot_utils.utils.Str                                  import str_safe

FILE_NAME__DB_SESSION__SESSION_CONFIG = 'session-config.json'

class S3_DB__Session(S3_DB__CBR):

    def __init__(self, session_id):
        self.session_id  = str_safe(session_id)
        super().__init__()

    def __repr__ (self                        ): return f"<DB_Session: {self.session_id}>"

    def cbr_cookie(self):
        return f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE}={self.session_id}"

    def create(self, user_id=None, user_name=None, data=None, security=None):
        return self.session_config__create(user_id=user_id, user_name=user_name, data=data, security=security)

    def delete(self):
        s3_keys_to_delete = [self.s3_key__session_config()]
        self.s3_files_delete(s3_keys_to_delete)
        return self.s3_folder__session__files() == []                 # this will confirm that everything has been deleted

    def exists(self):
        return self.s3_file_exists(self.s3_key__session_config())

    def session_config(self):
        if self.exists():
            session_data = self.s3_file_data(self.s3_key__session_config())
            return Model__Session__Config.from_json(session_data)
        return None

    def session_config__create(self, user_id=None, user_name=None, data=None, security=None):
        kwargs = dict(session_id = self.session_id ,
                      security   = security        ,
                      user_id    = user_id         ,
                      user_name  = user_name       ,
                      data       = data            )

        session_config = Model__Session__Config(**kwargs)
        self.s3_save_data(data=session_config.json(), s3_key=self.s3_key__session_config())
        return session_config

    def session_config__user_id(self):
        session_config = self.session_config()
        if session_config:
            return session_config.user_id


    # S3 keys

    def s3_folder__session(self):
        return url_join_safe(self.s3_folder_users_sessions(), self.session_id)

    def s3_folder__session__files(self):
        return self.s3_folder_files(self.s3_folder__session())

    def s3_key__session_config(self):
        return url_join_safe(self.s3_folder__session(), FILE_NAME__DB_SESSION__SESSION_CONFIG)