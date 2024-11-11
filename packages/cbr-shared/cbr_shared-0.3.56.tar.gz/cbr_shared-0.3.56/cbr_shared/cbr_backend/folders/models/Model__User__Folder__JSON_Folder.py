from typing                                                                 import List
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__JSON_Base   import Model__User__Folder__JSON_Base
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe


class Model__User__Folder__JSON_Folder(Model__User__Folder__JSON_Base):
    node_type  : str = 'folder'             # Constant type identifier
    children   : List[Type_Safe]            # List of child folders
    files      : List[Type_Safe]            # List of files in this folder