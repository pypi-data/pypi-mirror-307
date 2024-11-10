from cbr_shared.cbr_backend.user_personas.User__Persona import SECTION__NAME__USER__PERSONAS, User__Persona
from cbr_shared.cbr_backend.users.User__Section_Data    import User__Section_Data
from osbot_utils.helpers.Random_Guid                    import Random_Guid

class User__Personas(User__Section_Data):
    section_name = SECTION__NAME__USER__PERSONAS

    def persona(self, persona_id: Random_Guid):
        kwargs = dict(db_user=self.db_user, persona_id=persona_id)
        return User__Persona(**kwargs)

    def personas_ids(self):
        return self.section_folder_list()

    def personas_data(self):
        data = {}
        for persona_id in self.personas_ids():
            persona = self.persona(persona_id)
            persona_user         = persona.persona__db_user()                # this will create the user if it doesn't exist
            persona_config       = persona     .config      ().json()
            persona_user_profile = persona_user.user_profile().json()
            data[persona_id]     = dict(persona_config       = persona_config      ,
                                        persona_user_profile = persona_user_profile)
        return data


