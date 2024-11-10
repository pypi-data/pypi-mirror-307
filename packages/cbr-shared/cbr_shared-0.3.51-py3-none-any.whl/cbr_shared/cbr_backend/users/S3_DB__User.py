import re
from cbr_shared.aws.s3.S3_DB_Base                        import S3_DB_Base
from cbr_shared.schemas.data_models.Model__Chat__Saved   import Model__Chat__Saved
from cbr_shared.schemas.data_models.Model__User__Config  import Model__User__Config, random__model_user_config
from cbr_shared.schemas.data_models.Model__User__Profile import Model__User__Profile
from cbr_shared.utils.Utils__Str_Parsing                 import split__user_name_into_first_and_last_names
from osbot_utils.helpers.Random_Guid                     import Random_Guid
from osbot_utils.helpers.Zip_Bytes                       import Zip_Bytes
from osbot_utils.utils.Http                              import url_join_safe
from osbot_utils.utils.Status                            import status_ok

S3_DB_User__BUCKET_NAME__SUFFIX     = "db-users"                    # refactor to the name structure of S3__FOLDER_NAME__DB__USER__PERSONAS
S3_DB_User__BUCKET_NAME__PREFIX     = 'cyber-boardroom'

FILE_NAME__USER__CONFIG         = 'user-config.json'
FILE_NAME__USER__PROFILE        = 'user-profile.json'
FILE_NAME__USER__PAST_CHATS     = 'user-past-chats.json'

class S3_DB__User(S3_DB_Base):
    bucket_name__suffix: str         = S3_DB_User__BUCKET_NAME__SUFFIX
    bucket_name__prefix: str         = S3_DB_User__BUCKET_NAME__PREFIX
    user_id            : Random_Guid

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.user_id is None:
            self.user_id = Random_Guid()

    def __enter__(self                        ): return self
    def __exit__ (self, type, value, traceback): pass
    def __repr__ (self                        ): return f"<DB_User: {self.user_id}>"

    def create(self, user_config: Model__User__Config = None, user_profile:Model__User__Profile = None):
        if self.exists():
            raise ValueError("S3_DB__User already exists")
        if user_config is None:
            user_config = random__model_user_config()
        if user_profile is None:
            first_name, last_name = split__user_name_into_first_and_last_names(user_config.user_name)
            user_profile = Model__User__Profile(first_name=first_name, last_name=last_name)

        self.user_config__update (user_config)
        self.user_profile__update(user_profile)
        return status_ok()

    def delete(self):
        s3_key_user_files = [self.s3_key_user__config    (),
                             self.s3_key_user__past_chats(),
                             self.s3_key_user__profile   ()]
        self.s3_files_delete(s3_key_user_files)
        return self.s3_folder_user_data__all_files() == []                  # this will confirm that everything has been deleted

    def exists(self):
        return self.s3_file_exists(self.s3_key_user__profile())

    def has__file_system(self):
        return self.user_config().file_system

    def not_exists(self):
        return self.exists() is False


    def user_config(self) -> Model__User__Config:
        s3_key_user_config = self.s3_key_user__config()
        if self.s3_file_exists(s3_key_user_config):
            user_config_json = self.s3_file_contents_json(s3_key_user_config)
            user_config      = Model__User__Config(**user_config_json)
            return user_config
        return None

    def user_config__update(self, user_config: Model__User__Config):
        if type(user_config) is Model__User__Config:
            user_config.user_id = self.user_id                                              # make sure these are always in sync
            return self.s3_save_data(data=user_config.json(), s3_key=self.s3_key_user__config())
        raise ValueError("user_config_data needs to be of type Model__User__Config_Data")

    def user_config__update_value(self, key, value):
        user_config = self.user_config()
        if user_config:
            setattr(user_config, key, value)
            return self.user_config__update(user_config)

    def user_profile__update(self, user_profile: Model__User__Profile):
        if type(user_profile) is Model__User__Profile:
            return self.s3_save_data(data=user_profile.json(), s3_key=self.s3_key_user__profile())
        raise ValueError("user_profile_data needs to be of type Model__User__Profile_Data")


    # user data related methods

    def user_past_chats(self):
        s3_key_past_chats = self.s3_key_user__past_chats()
        if self.s3_file_exists(s3_key_past_chats):
            return self.s3_file_contents_json(s3_key_past_chats)
        return {}

    def user_past_chats__clear(self):
        return self.s3_save_data({}, self.s3_key_user__past_chats())

    def user_past_chats__add_chat(self, chat_path):
        safe_chat_path = re.sub(r'[^0-9a-f\-/]', '', chat_path)     # refactor to central location with these regexes
        if safe_chat_path != chat_path:
            return False
        past_chats = self.user_past_chats()
        if 'saved_chats' not in past_chats:
            past_chats['saved_chats'] = {}
        new_chat = Model__Chat__Saved(chat_path=safe_chat_path, user_id=self.user_id)

        self.populate_new_chat_metadata(new_chat)

        past_chats['saved_chats'][new_chat.chat_id] = new_chat.json()
        if self.s3_save_data(past_chats, self.s3_key_user__past_chats()):
            return new_chat

    def user_past_chats__in_table(self):
        headers = ['chat_id', 'view', 'user_id']
        rows = []
        chats = self.user_past_chats()
        if chats:
            for chat_id, chat_raw in chats.get('saved_chats').items():
                chat = Model__Chat__Saved.from_json(chat_raw)
                row = []
                row.append(chat.chat_id)
                row.append(f"""<a href='chat/view/{chat.chat_path}'      target="_blank">web page</a> |  
                               <a href='chat/view/{chat.chat_path}/pdf'   target="_blank">pdf</a> |  
                               <a href='chat/view/{chat.chat_path}/image' target="_blank">image</a>""")
                row.append(chat.user_id)

                rows.append(row)

        return dict(headers=headers, rows=rows)

    def user_data(self):
        return { 'config'    : self.user_config     ().json(),
                 'past_chats': self.user_past_chats ()       ,
                 'profile'   : self.user_profile    ().json()}

    def user_profile(self) -> Model__User__Profile:
        s3_key_user_profile = self.s3_key_user__profile()
        if self.s3_file_exists(s3_key_user_profile):
            user_profile_json = self.s3_file_contents_json(s3_key_user_profile)
            user_profile      = Model__User__Profile.from_json(user_profile_json)
            return user_profile
        return None

    # todo: move to a new class
    def populate_new_chat_metadata(self, new_chat):
        from cbr_shared.cbr_sites.CBR__Shared_Objects import cbr_shared_objects
        chat_path = new_chat.chat_path
        s3_key = f"chat-threads/cbr-website-dev-local/{chat_path}/user-response.json.gz"
        chat_threads = cbr_shared_objects.s3_db_chat_threads()
        chat_data    = chat_threads.s3_file_data(s3_key)
        if chat_data:
            user_prompt      = chat_data.get('user_prompt', '')
            user_prompt_size = len(user_prompt)
            llm_answer_size  = len(chat_data.get('llm_answer', ''))
            history_size   = len(chat_data.get('histories', []))
            new_chat.last_user_prompt = user_prompt
            new_chat.history_size     = history_size
            new_chat.prompts_size     = user_prompt_size
            new_chat.responses_size   = llm_answer_size
            for history in chat_data.get('histories'):
                new_chat.prompts_size   += len(history.get('question', ''))
                new_chat.responses_size += len(history.get('answer', ''))
        return new_chat

    def zip_bytes__with_paths_bytes(self, base_folder, paths):
        with Zip_Bytes() as _:
            for path in paths:
                s3_key = url_join_safe(base_folder, path)
                file_bytes = self.s3_file_bytes(s3_key)
                _.add_file(path, file_bytes)
            return _.zip_bytes

    # s3 folders and keys
    def s3_folder_user_data(self):
        return self.user_id

    def s3_folder_user_data__files(self):
        return self.s3_folder_files(self.s3_folder_user_data())

    def s3_folder_user_data__all_files(self, full_path=False):
        return self.s3_folder_files__all(self.s3_folder_user_data(), full_path=full_path)

    def s3_key_in_user_folder(self, file_name):
        return url_join_safe(self.s3_folder_user_data(), file_name)

    def s3_key_user__config(self):
        return self.s3_key_in_user_folder(FILE_NAME__USER__CONFIG)

    def s3_key_user__profile(self):
        return self.s3_key_in_user_folder(FILE_NAME__USER__PROFILE)

    def s3_key_user__past_chats(self):
        return self.s3_key_in_user_folder(FILE_NAME__USER__PAST_CHATS)