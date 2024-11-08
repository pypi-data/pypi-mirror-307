from cbr_shared.cbr_backend.session.S3_DB__Session  import S3_DB__Session
from cbr_shared.cbr_backend.users.S3_DB__User       import S3_DB__User
from cbr_shared.cbr_sites.CBR__Shared__Constants    import COOKIE_NAME__CBR__SESSION_ID__ACTIVE
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from fastapi                                        import Request, HTTPException

#api_key_header   = APIKeyHeader(name="Authorization", auto_error=False)

class CBR__Session__Load(Type_Safe):

    def session__from_request(self, request:Request):
        session_id = self.session_id__from_request(request)
        if session_id:
            return self.session__from_session_id(session_id)

    def session__from_session_id(self, session_id: str):
        db_session = S3_DB__Session(session_id)
        if db_session.exists():
            return db_session

    def session_config__from_request(self, request: Request):
        session = self.session__from_request(request)
        if session:
            return session.session_config()
        return {}

    def session_id__from_request(self, request: Request):
        if 'authorization' in request.headers:                                          # first see if there is an Authorization header (which takes priority
            return request.headers['authorization']

        if COOKIE_NAME__CBR__SESSION_ID__ACTIVE in request.cookies:                    # then see if we are in 'persona mode'
            return request.cookies.get(COOKIE_NAME__CBR__SESSION_ID__ACTIVE)           #

    def user__from_session(self, db_session: S3_DB__Session):
        user_id = db_session.session_config__user_id()
        db_user = S3_DB__User(user_id=user_id)
        if db_user.exists():
            return db_user

    def user__from_request(self, request: Request):
        db_session = self.session__from_request(request)
        if db_session:
            return self.user__from_session(db_session)


cbr_session_load = CBR__Session__Load()