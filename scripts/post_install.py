import shutil
import os
import pkg_resources

def copy_env_file():
    # Get the package directory
    package_dir = pkg_resources.resource_filename('exemplar_prompt_hub', '')
    # Get the parent directory of the package
    parent_dir = os.path.dirname(os.path.dirname(package_dir))
    
    # Define source and destination paths
    src_path = os.path.join(parent_dir, '.env.example')
    dst_path = os.path.join(parent_dir, '.env')
    
    if not os.path.exists(dst_path):
        try:
            shutil.copy(src_path, dst_path)
            print(f"Created .env file from .env.example at {dst_path}")
        except FileNotFoundError:
            print(f"Error: .env.example not found at {src_path}")
            return 1
    else:
        print(".env file already exists")
    return 0

if __name__ == '__main__':
    copy_env_file() 