from starlette.requests                                 import Request
from cbr_shared.cbr_backend.session.S3_DB__Session      import S3_DB__Session
from cbr_shared.cbr_backend.session.Temp_DB_Session     import Temp_DB_Session
from cbr_shared.cbr_backend.users.S3_DB__User           import S3_DB__User
from cbr_shared.cbr_backend.users.Temp_DB_User          import Temp_DB_User
from cbr_shared.cbr_sites.CBR__Shared__Constants        import COOKIE_NAME__CBR__SESSION_ID__ACTIVE
from osbot_fast_api.utils.Fast_API__Request             import Fast_API__Request
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.helpers.Random_Guid                    import Random_Guid


class Temp_User_Request(Type_Safe):
    fast_api_request : Fast_API__Request = None
    request          : Request           = None
    session_id       : Random_Guid       = None
    temp_user        : S3_DB__User       = None
    temp_db_session  : S3_DB__Session    = None
    user_id          : Random_Guid       = None

    def __enter__(self):
        self.create()
        return self.request

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()
        pass

    def create(self):
        if self.temp_user is None:
            self.temp_user        = Temp_DB_User().create()
        self.user_id          = self.temp_user.user_id
        self.temp_db_session  = Temp_DB_Session(user_id=self.user_id).create()
        self.session_id       = self.temp_db_session.session_id
        self.fast_api_request = Fast_API__Request().set_cookie(COOKIE_NAME__CBR__SESSION_ID__ACTIVE, self.session_id)
        self.request          = self.fast_api_request.request()
        return self

    def delete(self):
        self.temp_db_session.delete()
        self.temp_user      .delete()
        return self