from typing                                                                 import List
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__JSON_File   import Model__User__Folder__JSON_File
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__JSON_Folder import Model__User__Folder__JSON_Folder
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe


class Model__User__Folders__JSON_Flat(Type_Safe):
    folders: List[Model__User__Folder__JSON_Folder]
    files  : List[Model__User__Folder__JSON_File  ]