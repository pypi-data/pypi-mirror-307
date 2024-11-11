from typing                                                               import List
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__Metadata  import Model__User__Folder__Metadata
from osbot_utils.base_classes.Type_Safe                                   import Type_Safe
from osbot_utils.helpers.Random_Guid                                      import Random_Guid
from osbot_utils.helpers.Safe_Id                                          import Safe_Id


class Model__User__Folder(Type_Safe):
    folder_id         : Random_Guid                             # Unique identifier for the folder
    folder_name       : Safe_Id                                 # Display name of the folder
    metadata          : Model__User__Folder__Metadata           # Folder metadata
    parent_id         : Random_Guid                     = None  # ID of parent folder (None for root only)
    files             : List[Random_Guid]
    folders           : List[Random_Guid]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.folder_id   is None:
            raise ValueError("Invalid ID:Folder Id must not be None")
        if self.folder_name is None:
            raise ValueError("Invalid Name: Folder Name must not be None")



    def __repr__(self):
        return f"<Model__User__Folder> {self.folder_name} ({self.folder_id})"