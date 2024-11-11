from cbr_shared.cbr_sites.CBR__Shared_Objects       import cbr_shared_objects
from osbot_utils.helpers.Random_Guid                import Random_Guid


class Temp_DB_Session:
    def __init__(self, data=None, session_id = None, security=None, user_id=None, user_name=None):
        self.data       = data
        self.security   = security
        self.user_id    = user_id
        self.user_name  = user_name
        self.session_id = session_id or Random_Guid()
        self.db_session = cbr_shared_objects.db_sessions().db_session(session_id=self.session_id)

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()
        pass

    def create(self):
        kwargs = dict(data      = self.data     ,
                      security  = self.security ,
                      user_id   = self.user_id  ,
                      user_name = self.user_name)
        self.db_session.create(**kwargs)
        return self.db_session

    def delete(self):
        self.db_session.delete()
        return self

    def exists(self):
        return self.db_session.exists()