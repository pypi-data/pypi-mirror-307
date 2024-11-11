from typing                             import Dict, Optional
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now

class Model__User__Folder__JSON_Base(Type_Safe):
    node_id     : Random_Guid                       # Unique identifier
    name        : str                               # Display name
    created_at  : Timestamp_Now         = None      # Creation timestamp
    updated_at  : Timestamp_Now         = None      # Last update timestamp
    parent_id   : Optional[Random_Guid] = None      # Parent folder ID (None for root)
    metadata    : Dict                  = None      # Additional metadata