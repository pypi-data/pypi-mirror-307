from typing                                                                 import List
from cbr_shared.cbr_backend.folders.models.Model__User__Folder              import Model__User__Folder
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File        import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe

CHAR__DASH       = "─"
CHAR__SPACE      = " "

EMOJI__CORNER    = "└"
EMOJI__FILE      = "📄"
EMOJI__FOLDER    = "📁"
EMOJI__PIPE      = "│"
EMOJI__ROOT      = "🏠"
EMOJI__TEE       = "├"

SIZE__PADDING    = 2

class User__Folders__Tree_View(Type_Safe):
    folders_structure: Model__User__Folders__Structure
    lines            : List[str]

    def add_folder(self, folder:Model__User__Folder, level:int, is_last:bool):
        line_segments = [self.create_padding(level)                ,
                         self.create_prefix__folder (level, is_last),
                         folder.folder_name                        ]
        self.add_line_segments(line_segments)

    def add_folder_file(self, folder_file: Model__User__Folder__File, level: int, is_last: bool):
        line_segments = [self.create_padding(level),
                         self.create_prefix__file(is_last),
                         folder_file.file_name]
        self.add_line_segments(line_segments)

    def add_line_segments(self, line_segments):
        line = ''.join(line_segments)
        self.add_line(line)

    def add_line(self, line):
        self.lines.append(line)

    def add_line__recursive_folder(self, folder, level):
        line_segments = [self.create_padding(level),
                         self.create_prefix__recursive(),
                         folder.folder_name]
        self.add_line_segments(line_segments)

    def create_prefix__file(self, is_last: bool) -> str:     # Create the prefix characters for files
        prefix = EMOJI__CORNER if is_last else EMOJI__PIPE
        return prefix + CHAR__SPACE + CHAR__SPACE + EMOJI__FILE

    def create_prefix__folder(self, level: int, is_last: bool) -> str: # create prefix characters based on level and position"""
        folder_emoji = EMOJI__ROOT if level == 0 else EMOJI__FOLDER

        if level <= 0:
            return folder_emoji

        prefix = EMOJI__CORNER if is_last else EMOJI__TEE
        if level > 0:
            return prefix + CHAR__DASH + CHAR__SPACE + folder_emoji
        return prefix + folder_emoji

    def create_prefix__recursive(self):
        return f"⚠️🔄 Recursive link to:" + CHAR__SPACE + EMOJI__FOLDER

    def create_padding(self, level: int) -> str:                                                                        # Create padding string based on level
        if level <= 0:
            return ''
        padding = ''
        for i in range(1, level):
            padding += EMOJI__PIPE + CHAR__SPACE * SIZE__PADDING
        return padding

    def folder_from_structure(self, folder_id: str):                                                                    # Helper method to get folder from structure
        return self.folders_structure.folders.get(folder_id)

    def process__folder(self, folder_id: str, prefix: str, level: int, is_last: bool, visited: set) -> None:             # Recursively build the tree structure.
        folder = self.folder_from_structure(folder_id)
        if not folder:
            return
        if level == 0:
            self.process__folder__root(folder, folder_id, prefix, level, is_last, visited)
        else:
            self.process__folder__non_root(folder, folder_id, prefix, level, is_last, visited)

    def process__folder__root(self, folder, folder_id: str, prefix: str, level: int, is_last: bool, visited: set) -> None:       # Handle processing at root level (level 0).
        self.add_folder(folder=folder, level=level, is_last=is_last)

        kwargs = dict(folder_id = folder_id ,
                      prefix    = prefix    ,
                      level     = level + 1 ,  # increase level
                      is_last   = is_last   ,
                      visited   = visited   )
        self.process__folder(**kwargs)

        for folder_file_id in folder.files:                                             # Process root files
            folder_file = self.folders_structure.files.get(folder_file_id)
            if folder_file:
                self.add_folder_file(folder_file, level=level, is_last=False)

    def process__folder__non_root(self, folder, folder_id: str, prefix: str, level: int, is_last: bool, visited: set) -> None:   # Handle processing at non-root levels."""
        visited.add(folder_id)
        try:
            self.process__subfolders(folder, prefix, level, visited)
        finally:
            visited.remove(folder_id)

    def process__subfolders(self, folder, prefix: str, level: int, visited: set) -> None:                               # Process all subfolders within a folder.
        sub_folders = folder.folders
        sub_folder_size = len(sub_folders) - 1

        for index, sub_folder_id in enumerate(sub_folders):
            is_last = index == sub_folder_size
            self.process__subfolder(sub_folder_id, prefix, level, is_last, visited)

    def process__subfolder(self, sub_folder_id: str, prefix: str, level: int, is_last: bool, visited: set) -> None:     # Process an individual subfolder
        sub_folder = self.folder_from_structure(sub_folder_id)
        if sub_folder:
            if sub_folder.folder_id in visited:
                self.add_line__recursive_folder(sub_folder, level)
            else:
                self.process__subfolder__after_recursive_check(sub_folder, sub_folder_id, prefix, level, is_last, visited)

    def process__subfolder__after_recursive_check(self, sub_folder, sub_folder_id: str, prefix: str, level: int, is_last: bool, visited: set) -> None: # Process a non-recursive subfolder and its files.
        self.add_folder(folder=sub_folder, level=level, is_last=is_last)

        kwargs = dict(folder_id = sub_folder_id ,
                      prefix    = prefix        ,
                      level     = level + 1     ,
                      is_last   = is_last       ,
                      visited   = visited       )
        self.process__folder(**kwargs)

        self.process__subfolder__files(sub_folder, level)

    def process__subfolder__files(self, sub_folder, level: int) -> None:                                                # Process all files within a subfolder.
        for folder_file_id in sub_folder.files:
            folder_file = self.folders_structure.files.get(folder_file_id)
            self.add_folder_file(folder_file, level=level + 1, is_last=False)


    def tree_view(self) -> str:                                               # Generate a tree view of the folder structure.
        if not self.folders_structure.folders:
            return "Empty folder structure"

        root_id = self.folders_structure.root_id

        self.lines = []
        self.process__folder(root_id, "", 0, True, set())
        return "\n".join(self.lines)

    def print(self):
        print()
        print(self.tree_view())

