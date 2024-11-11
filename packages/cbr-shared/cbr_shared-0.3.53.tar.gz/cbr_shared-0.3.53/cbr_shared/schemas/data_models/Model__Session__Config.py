from dataclasses                                            import dataclass, field
from cbr_shared.schemas.data_models.Model__Config__Base     import Model__Config__Base
from cbr_shared.schemas.data_models.Model__Security__Groups import Model__Session_Security
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.utils.Misc                                 import random_text
from osbot_utils.utils.Str                                  import safe_str


@dataclass
class Model__Session__Config(Model__Config__Base):
    data       : dict                    = None
    security   : Model__Session_Security = None
    session_id : Random_Guid             = None
    user_name  : str                     = None
    user_id    : Random_Guid             = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.data        is None: self.data        = {}
        if self.security    is None: self.security    = Model__Session_Security()
        if self.session_id  is None: self.session_id  = Random_Guid            ()
        if self.user_id     is None: self.user_id     = Random_Guid            ()
        if self.user_name   is None: self.user_name   = random_text            ('user', lowercase=True, length=5)

        self.user_name = safe_str(self.user_name)  # todo: create Safe_Str class (similar to Random_Guid)
