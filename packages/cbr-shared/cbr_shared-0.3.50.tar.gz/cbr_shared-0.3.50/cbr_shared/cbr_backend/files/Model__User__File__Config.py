from dataclasses                                        import dataclass
from cbr_shared.schemas.data_models.Model__Config__Base import Model__Config__Base
from osbot_utils.helpers.Random_Guid                    import Random_Guid

@dataclass
class Model__User__File__Config(Model__Config__Base):
    file_id: Random_Guid
    original_name: str                    # immutable original file name

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.file_id is None:
            self.file_id = Random_Guid()