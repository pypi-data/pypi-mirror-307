from cbr_shared.cbr_backend.files.Model__User__File__Config         import Model__User__File__Config
from cbr_shared.cbr_backend.files.Model__User__File__Data           import Model__User__File__Data
from cbr_shared.cbr_backend.users.User__Section_Data                import User__Section_Data
from osbot_utils.helpers.Random_Guid                                import Random_Guid
from osbot_utils.utils.Files                                        import file_extension
from osbot_utils.utils.Http                                         import url_join_safe

SECTION__NAME__USER__FILES = 'user-files'
FILE_NAME__FILE_CONFIG     = 'file-config.json'
FILE_NAME__FILE_DATA       = 'file-data.json'
FILE_NAME__FILE_CONTENT    = 'file-content.bin'

class User__File(User__Section_Data):
    file_id     : Random_Guid
    section_name: str = SECTION__NAME__USER__FILES

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.file_id is None:
            self.file_id = Random_Guid()

    def config(self) -> Model__User__File__Config:                                                              # Get immutable file configuration
        config_json = self.file_data(self.file_path__config())
        return Model__User__File__Config(**config_json)

    def config__update(self, file_config: Model__User__File__Config):                                            # Update file configuration
        if type(file_config) is not Model__User__File__Config:
            raise ValueError("file_config needs to be of type Model__User__File__Config")
        self.file_save(self.file_path__config(), file_config.json())
        return self

    def create(self, file_bytes: bytes, file_name: str, user_folder_id: Random_Guid = None):                              #   Create a new file with content and metadata
        if self.exists():
            raise ValueError("File already exists")

        file_config = Model__User__File__Config( file_id        = self.file_id              ,               # file config
                                                 original_name  = file_name                 )
        file_data   = Model__User__File__Data  ( current_name   = file_name                 ,               # file data
                                                 file_type      = file_extension(file_name) ,
                                                 file_size      = len(file_bytes)           ,
                                                 user_folder_id = user_folder_id            )               # folder id that maps to the data stored in the User__Folders

        self.config__update(file_config )                                                                         # Save all components
        self.data__update(file_data     )
        self.contents__update(file_bytes, update_size=False)

        return self


    def contents(self):                                                                                         # Get file contents
        return self.file_bytes(self.file_path__content())

    def contents__update(self, file_bytes, update_size=True):                                                   # update file contents
        if type(file_bytes) is not bytes:
            raise ValueError("file_bytes needs to be of type bytes")
        if file_bytes is None:
            file_bytes = b''

        self.file_save(self.file_path__content(), file_bytes)
        if update_size:
            self.data__update_file_size(len(file_bytes))
        return self

    def data(self) -> Model__User__File__Data:
        data_json = self.file_data(self.file_path__data())
        return Model__User__File__Data(**data_json)

    def data__update(self, file_data: Model__User__File__Data):                                                   # update file data
        if type(file_data) is not Model__User__File__Data:
            raise ValueError("file_data needs to be of type Model__User__File__Data")
        file_data.update_timestamp()                                                                            # apply the update_timestamp here (to make sure it happens, and it is consistent)
        self.file_save(self.file_path__data(), file_data.json())
        return self

    def data__update_file_size(self, file_size: int):                                                           # update file size
        file_data           = self.data()
        file_data.file_size = file_size
        self.data__update(file_data)
        return self

    def delete(self):                                                                                           # Delete all file components
        paths_to_delete = [ self.file_path__config (),
                            self.file_path__data   (),
                            self.file_path__content()]
        for path in paths_to_delete:
            self.file_delete(path)
        return self.all_files() == []                                                                           # Confirm that there are no files left

    def exists(self):
        return self.file_exists(self.file_path__config())

    def rename(self, new_name):                                                                                 # rename file
        file_data              = self.data()
        file_data.current_name = new_name
        file_data.file_type    = file_extension(new_name)
        self.file_save(self.file_path__data(), file_data.json())
        return self


    # Path management methods

    def all_files(self, full_path=False):
        return self.folder_all_files(folder=self.file_path__base(), full_path=full_path)

    def file_path__base(self):                                                                                          # Base path for file storage
        return str(self.file_id)

    def file_path__config(self):                                                                                        # Path to config file
        return url_join_safe(self.file_path__base(), FILE_NAME__FILE_CONFIG)

    def file_path__data(self):                                                                                          # Path to data file
        return url_join_safe(self.file_path__base(), FILE_NAME__FILE_DATA)

    def file_path__content(self):                                                                                       # Path to content file
        return url_join_safe(self.file_path__base(), FILE_NAME__FILE_CONTENT)