from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.utils.Misc             import random_text


@dataclass
class Model__User__Persona__Config(Type_Safe):
    persona_name : str         = None                           # todo: see if we need this
    persona_id   : Random_Guid = None
    user_id      : Random_Guid = None
    session_id   : Random_Guid = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.persona_id   is None: self.persona_id   = Random_Guid   ()
        if self.persona_name is None: self.persona_name = random_text   ('persona', lowercase=True, length=5)
        if self.user_id      is None: self.user_id      = Random_Guid()
        if self.session_id   is None: self.session_id   = Random_Guid()