from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Safe_Id        import Safe_Id

class Model__User__Folder__File(Type_Safe):
    file_id  : Random_Guid                      # ID of the file
    file_name: Safe_Id
    folder_id: Random_Guid                      # ID of containing folder
