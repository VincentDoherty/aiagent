import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Check that the target directory is within the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check that it exists and is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        output_lines = []
        # List files and directories in the target directory
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            output_lines.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: {str(e)}"