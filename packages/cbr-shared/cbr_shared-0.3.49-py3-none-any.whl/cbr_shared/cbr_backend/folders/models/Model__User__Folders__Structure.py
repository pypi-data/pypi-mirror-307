from typing                                                             import Dict
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File    import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folder          import Model__User__Folder
from osbot_utils.base_classes.Type_Safe                                 import Type_Safe
from osbot_utils.helpers.Random_Guid                                    import Random_Guid


#@dataclass
class Model__User__Folders__Structure(Type_Safe):
    root_id: Random_Guid = None
    folders: Dict[Random_Guid, Model__User__Folder        ]
    files  : Dict[Random_Guid, Model__User__Folder__File  ]



