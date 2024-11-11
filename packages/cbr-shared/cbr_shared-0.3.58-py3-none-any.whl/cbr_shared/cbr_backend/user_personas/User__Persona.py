from cbr_shared.cbr_backend.users.User__Section_Data                import User__Section_Data
from cbr_shared.cbr_sites.CBR__Shared_Objects                       import cbr_shared_objects
from cbr_shared.schemas.data_models.Model__User__Config             import Model__User__Config
from cbr_shared.schemas.data_models.Model__User__Persona__Config    import Model__User__Persona__Config
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.helpers.Random_Guid                                import Random_Guid
from osbot_utils.utils.Http                                         import url_join_safe

SECTION__NAME__USER__PERSONAS             = 'user-personas'
SECTION__FILE_NAME__USER__PERSONA__CONFIG = 'persona-config.json'

class User__Persona(User__Section_Data):
    persona_id   : Random_Guid
    section_name : str = SECTION__NAME__USER__PERSONAS

    def create(self, user_persona_config: Model__User__Persona__Config = None):
        if self.exists():
            raise ValueError("User__Persona already exists")
        if user_persona_config is None:
            user_persona_config = Model__User__Persona__Config()
        self.config__create(user_persona_config)
        return self

    @cache_on_self
    def config(self):
        return Model__User__Persona__Config.from_json(self.file_data(self.file_path__persona_config()))

    def config__create(self, user_persona_config: Model__User__Persona__Config):
        if type(user_persona_config) is Model__User__Persona__Config:
            user_persona_config.persona_id = self.persona_id                                                    # make sure this the persona_id in the config matches the persona_id of the current instance
            return self.file_save(path=self.file_path__persona_config(), data=user_persona_config.json())
        raise ValueError("user_persona_config needs to be of type Model__User__Persona__Config")

    def delete(self):
        self.file_delete(self.file_path__persona_config())
        return self.all_files() == []                                                           # this will confirm that everything has been deleted

    def exists(self):
        return self.file_exists(self.file_path__persona_config())

    @cache_on_self
    def persona__db_session(self):
        db_session = cbr_shared_objects.db_sessions().db_session(self.persona__session_id())
        if db_session.exists() is False:                                                        # create a session if this is the first time we access it
            kwargs = dict(user_id   = self.persona__user_id     (),
                          user_name = self.persona__persona_name())
            db_session.create(**kwargs)
        return db_session

    @cache_on_self
    def persona__db_user(self):
        persona_user_id   = self.persona__user_id()
        db_user = cbr_shared_objects.db_users().db_user(persona_user_id)
        if db_user.exists() is False:                                                           # create a user if this is the first time we access it
            persona_user_name = self.persona__persona_name()
            kwargs            = dict(user_id   = persona_user_id,
                                     user_name = persona_user_name)
            user_config      = Model__User__Config(**kwargs)
            db_user.create(user_config=user_config)
        return db_user

    def persona__persona_name(self):
        return self.config().persona_name

    def persona__session_id(self):
        return self.config().session_id

    def persona__user_id(self):
        return self.config().user_id


    # methods for files and folders

    def all_files(self, full_path=False):
        return self.folder_all_files(folder=self.folder_path__persona(), full_path=full_path)

    def folder_path__persona(self):
        return f'{self.persona_id}'

    def file_path__persona_config(self):
        return f'{self.folder_path__persona()}/{SECTION__FILE_NAME__USER__PERSONA__CONFIG}'

    def file_path__in__user_persona(self, path):
        return url_join_safe(self.folder_path__persona(), path)

    def file_data__in__user_persona(self, path):
        path_in_user_persona = self.file_path__in__user_persona(path)
        return self.file_data(path_in_user_persona)

    def s3_folder__user_persona(self):
        return self.s3_key(self.folder_path__persona())
