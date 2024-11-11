from cbr_shared.cbr_backend.users.S3_DB__User            import S3_DB__User
from cbr_shared.cbr_backend.users.Temp_DB_User           import Temp_DB_User
from cbr_shared.cbr_backend.user_personas.User__Persona  import User__Persona
from osbot_utils.base_classes.Type_Safe                  import Type_Safe

class Temp_User_Persona(Type_Safe):
    temp_user              : S3_DB__User   = None
    user_persona           : User__Persona = None
    user_persona_db_user   : S3_DB__User   = None
    create_persona_db_user : bool          = False

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        self.temp_user            = Temp_DB_User().create()
        self.user_persona         = User__Persona(db_user=self.temp_user).create()
        if self.create_persona_db_user:
            self.user_persona_db_user = self.user_persona.persona__db_user()             # this will create the user for the db_persona
        return self.user_persona

    def delete(self):
        assert self.user_persona.delete() is True
        assert self.temp_user   .delete() is True
        if self.create_persona_db_user:
            assert self.user_persona_db_user.delete() is True
