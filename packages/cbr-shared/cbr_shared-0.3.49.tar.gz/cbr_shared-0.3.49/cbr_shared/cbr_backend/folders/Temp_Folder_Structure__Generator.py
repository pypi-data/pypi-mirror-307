from cbr_shared.cbr_backend.folders.User__Folders__Operations               import User__Folders__Operations
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from osbot_utils.base_classes.Type_Safe                         import Type_Safe
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self


class Temp_Folder_Structure__Generator(Type_Safe):
    folders_structure: Model__User__Folders__Structure

    @cache_on_self
    def operations(self):
        return User__Folders__Operations(folders_structure=self.folders_structure)

    #def create_random_folder_structure(self):
    def create_folder_structure__with_multiple_folders_and_files(self):
        with self.operations() as _:
            root_folder  = _.create_root()
            folder_1a    = _.add_folder(root_folder, "folder-1a")
            folder_1b    = _.add_folder(root_folder, "folder-1b")
            folder_2a    = _.add_folder(folder_1a  , "folder-2a")
            folder_2b    = _.add_folder(folder_1a  , "folder-2b")
            folder_3a    = _.add_folder(folder_2b  , "folder-3a")
            folder_3b    = _.add_folder(folder_2b  , "folder-3b")
            _.add_file(folder=root_folder, file_name='in root_folder 1')
            _.add_file(folder=root_folder, file_name='in root_folder 2')
            _.add_file(folder=folder_1a  , file_name='in folder_1a'  )
            _.add_file(folder=folder_1a  , file_name='in folder_1a'  )
            _.add_file(folder=folder_2b  , file_name='in folder_2b'  )
            _.add_file(folder=folder_1b  , file_name='in folder_1b'  )
            _.add_file(folder=folder_3b  , file_name='in folder_3b')