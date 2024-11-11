from typing                                                                 import Optional, Dict
from cbr_shared.cbr_backend.folders.User__Folders__Tree_View                import User__Folders__Tree_View
from cbr_shared.cbr_backend.folders.models.Model__User__Folder              import Model__User__Folder
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__File        import Model__User__Folder__File
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__JSON_Flat  import Model__User__Folders__JSON_Flat
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__JSON_Folder import Model__User__Folder__JSON_Folder
from cbr_shared.cbr_backend.folders.models.Model__User__Folder__JSON_File   import Model__User__Folder__JSON_File
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.Random_Guid                                        import Random_Guid

class User__Folders__JSON_View(Type_Safe):
    folders_structure: Model__User__Folders__Structure

    def folder_from_structure(self, folder_id: str) -> Optional[Model__User__Folder]:                                               # Helper method to get folder from structure
        return self.folders_structure.folders.get(folder_id)

    def create_file_node(self, folder_file: Model__User__Folder__File, parent_id: Random_Guid) -> Model__User__Folder__JSON_File:   # Create a JSON node for a file
        node           = Model__User__Folder__JSON_File()
        node.node_id   = folder_file.file_id
        node.name      = folder_file.file_name
        node.parent_id = parent_id
        # node.created_at = folder_file.metadata.timestamp__created
        # node.updated_at = folder_file.metadata.timestamp__updated
        # node.metadata = folder_file.metadata.json()
        return node

    def create_folder_node(self, folder: Model__User__Folder, include_children: bool = True) -> Model__User__Folder__JSON_Folder:               # Create a JSON node for a folder
        node            = Model__User__Folder__JSON_Folder()
        node.node_id    = folder.folder_id
        node.name       = folder.folder_name
        node.parent_id  = folder.parent_id
        node.created_at = folder.metadata.timestamp__created
        node.updated_at = folder.metadata.timestamp__updated
        node.metadata   = folder.metadata.json()

        if include_children:                                                                                    # Add files
            for file_id in folder.files:
                folder_file = self.folders_structure.files.get(file_id)
                if folder_file:
                    file_node = self.create_file_node(folder_file, folder.folder_id)
                    node.files.append(file_node)

            for child_folder_id in folder.folders:                                                              # Add subfolders recursively
                child_folder = self.folder_from_structure(child_folder_id)
                if child_folder:
                    child_node = self.create_folder_node(child_folder)
                    node.children.append(child_node)

        return node

    def to_json(self) -> Dict:                                                                                  # Convert folder structure to hierarchical JSON
        if not self.folders_structure:
            return {}

        root_id     = self.folders_structure.root_id
        root_folder = self.folder_from_structure(root_id)

        if not root_folder:
            return {}

        return self.create_folder_node(root_folder).json()

    def to_flat_json(self) -> Dict:                                                                             # Convert folder structure to flat JSON structure
        flat_structure = Model__User__Folders__JSON_Flat()
        visited = set()

        def process_folder(folder: Model__User__Folder):
            if folder.folder_id in visited:
                return
            visited.add(folder.folder_id)

            folder_node = self.create_folder_node(folder, include_children=False)                               # Add folder node
            flat_structure.folders.append(folder_node)

            for file_id in folder.files:                                                                        # Add file nodes
                folder_file = self.folders_structure.files.get(file_id)
                if folder_file:
                    file_node = self.create_file_node(folder_file, folder.folder_id)
                    flat_structure.files.append(file_node)

            for child_folder_id in folder.folders:                                                                          # Process subfolders
                child_folder = self.folder_from_structure(child_folder_id)
                if child_folder:
                    process_folder(child_folder)

        root_folder = self.folder_from_structure(self.folders_structure.root_id)
        if root_folder:
            process_folder(root_folder)

        return flat_structure.json()

    def tree_view(self):                                                                                        # return the folder structure in a tree format
        return User__Folders__Tree_View(folders_structure=self.folders_structure).tree_view()
