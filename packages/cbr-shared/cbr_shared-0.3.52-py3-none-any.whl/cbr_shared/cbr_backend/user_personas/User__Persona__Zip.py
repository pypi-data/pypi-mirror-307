from cbr_shared.cbr_backend.user_personas.User__Persona          import User__Persona
from cbr_shared.schemas.data_models.Model__User__Config          import Model__User__Config
from cbr_shared.schemas.data_models.Model__User__Persona__Config import Model__User__Persona__Config
from cbr_shared.schemas.data_models.Model__User__Profile         import Model__User__Profile
from osbot_utils.base_classes.Type_Safe                          import Type_Safe
from osbot_utils.helpers.Random_Guid                             import Random_Guid
from osbot_utils.helpers.Zip_Bytes                               import Zip_Bytes
from osbot_utils.utils.Json                                      import json_to_bytes, bytes_to_json
from osbot_utils.utils.Zip                                       import zip_bytes__file, zip_bytes__files


class User__Persona__Zip(Type_Safe):

    def user_persona__and__persona_db_user__to__zip_bytes(self, user_persona:User__Persona):
        with user_persona as persona:
            persona__id          = persona.persona_id
            persona__all_files   = persona.all_files()
            persona__base_folder = persona.s3_folder__user_persona()
            persona__zip_bytes   = persona.db_user.zip_bytes__with_paths_bytes(persona__base_folder, persona__all_files)

        with user_persona.persona__db_user() as db_user:
            db_user__id          = db_user.user_id
            db_user__all_files   = db_user.s3_folder_user_data__all_files()
            db_user__base_folder = db_user.s3_folder_user_data()
            db_user__zip_bytes   = db_user.zip_bytes__with_paths_bytes(db_user__base_folder, db_user__all_files)

        persona_zip_config       = dict(persona__id = persona__id ,
                                        db_user__id = db_user__id )

        persona_zip_config_bytes = json_to_bytes(persona_zip_config)
        with Zip_Bytes() as _:
            _.add_file('persona_zip_config' , persona_zip_config_bytes)
            _.add_file('persona__zip_bytes' , persona__zip_bytes      )
            _.add_file('db_user__zip_bytes' , db_user__zip_bytes      )
            return _.zip_bytes

    def create__user_persona__and__persona_db_user__from__zip_bytes(self, db_user, zip_bytes, reassign_ids=True):
        persona_zip_config_bytes = zip_bytes__file(zip_bytes, 'persona_zip_config')
        persona__zip_bytes       = zip_bytes__file(zip_bytes, 'persona__zip_bytes')
        db_user__zip_bytes       = zip_bytes__file(zip_bytes, 'db_user__zip_bytes')
        persona__zip_bytes_files = zip_bytes__files(persona__zip_bytes)
        db_user__zip_bytes_files = zip_bytes__files(db_user__zip_bytes)
        persona_zip_config       = bytes_to_json(persona_zip_config_bytes)
        persona_id               = persona_zip_config.get('persona__id')
        db_user_id               = persona_zip_config.get('db_user__id')

        persona_config__json      = bytes_to_json(persona__zip_bytes_files.get('persona-config.json'))
        user_config__json         = bytes_to_json(db_user__zip_bytes_files.get('user-config.json'   ))
        user_profile__json        = bytes_to_json(db_user__zip_bytes_files.get('user-profile.json'  ))

        user_persona_config = Model__User__Persona__Config(**persona_config__json)
        user_config         = Model__User__Config         (**user_config__json   )
        user_profile        = Model__User__Profile        (**user_profile__json  )


        if reassign_ids:                   # this is needed when importing user_personas and db_users into the same server
            persona_id                     = Random_Guid()
            db_user_id                     = Random_Guid()
            session_id                     = Random_Guid()
            user_persona_config.persona_id = persona_id
            user_persona_config.user_id    = db_user_id
            user_persona_config.session_id = session_id
            user_config.user_id            = db_user_id

        user_persona         = User__Persona(persona_id=persona_id, db_user=db_user).create(user_persona_config)
        persona__db_user     = user_persona.persona__db_user()
        persona__db_user.user_profile__update(user_profile)
        return user_persona