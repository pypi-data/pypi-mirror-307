from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
from osbot_utils.utils.Misc             import timestamp_to_str_date, timestamp_to_str_time


class Model__Config__Base(Type_Safe):
    created__date      : str               = None
    created__time      : str               = None
    created__timestamp : Timestamp_Now     = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created__timestamp is None: self.created__timestamp = Timestamp_Now()
        if self.created__date      is None: self.created__date      = timestamp_to_str_date(self.created__timestamp)
        if self.created__time      is None: self.created__time      = timestamp_to_str_time(self.created__timestamp)
