from dataclasses                        import dataclass, field
from typing                             import Dict, Any
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
from osbot_utils.utils.Misc             import timestamp_to_str_date, timestamp_to_str_time


@dataclass
class Model__User__File__Data(Type_Safe):
    file_name        : str                                                          # current file name (can be changed)
    file_size        : int
    file_type        : str
    metadata         : Dict[str, Any] = field(default_factory=dict)
    updated__date    : str            = None
    updated__time    : str            = None
    updated_timestamp: Timestamp_Now  = None
    user_folder_id   : Random_Guid    = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.updated_timestamp is None:
            self.updated_timestamp = Timestamp_Now()
        if self.updated__date is None:
            self.updated__date = timestamp_to_str_date(self.updated_timestamp)
        if self.updated__time is None:
            self.updated__time = timestamp_to_str_time(self.updated_timestamp)

    def update_timestamp(self):
        self.updated_timestamp = Timestamp_Now()
        self.updated__date     = timestamp_to_str_date(self.updated_timestamp)
        self.updated__time     = timestamp_to_str_time(self.updated_timestamp)