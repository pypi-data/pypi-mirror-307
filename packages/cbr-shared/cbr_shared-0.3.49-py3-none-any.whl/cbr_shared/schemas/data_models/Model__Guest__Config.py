from dataclasses                                            import dataclass
from cbr_shared.schemas.data_models.Model__Session__Config  import Model__Session__Config
from osbot_utils.utils.Str                                  import safe_str
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.utils.Misc                                 import random_text

@dataclass
class Model__Guest__Config(Model__Session__Config):
    guest_name      : str               = None
    guest_id        : Random_Guid       = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.guest_id   is None: self.guest_id   = Random_Guid   ()
        if self.guest_name is None: self.guest_name = random_text   ('guest', lowercase=True, length=5)

        self.guest_name = safe_str(self.guest_name)  # todo: create Safe_Str class (similar to Random_Guid)




