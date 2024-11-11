from dataclasses                            import dataclass, field
from typing                                 import Dict, Optional
from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.helpers.Random_Guid        import Random_Guid
from osbot_utils.helpers.Timestamp_Now      import Timestamp_Now

class Model__User__Folder__Metadata(Type_Safe):
    timestamp__created: Timestamp_Now                   # Creation timestamp
    timestamp__updated: Timestamp_Now                   # Last modification timestamp
