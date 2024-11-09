from cbr_shared.cbr_backend.cbr.S3_DB__CBR          import S3_DB__CBR
from cbr_shared.cbr_backend.session.S3_DB__Session  import S3_DB__Session

class S3_DB__Sessions(S3_DB__CBR):

    def db_session(self, session_id):
        return S3_DB__Session(session_id)

    def db_sessions_ids(self):
        return self.s3_folder_list(folder=self.s3_folder_users_sessions())

    def sessions(self):
        for session_id in self.db_sessions_ids():
            yield self.db_session(session_id)

    def sessions__all_data(self, size=None):
        all_data = {}
        for session in self.sessions():
            all_data[session.session_id] = session.session_config()
            if size and len(all_data) >= size:
                break
        return all_data