import os

class FolderValidator:
    @staticmethod
    def validate_folder(folder_path):
        """
        Validate folder existence and permissions.
        
        Args:
            folder_path (str): Path to validate
            
        Raises:
            FileNotFoundError: If folder doesn't exist
            NotADirectoryError: If path is not a directory
            PermissionError: If lacking read permissions
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder path does not exist: {folder_path}")
        
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Provided path is not a directory: {folder_path}")
        
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"No read permissions for folder: {folder_path}")
