import os
from pathlib import Path

def add_umask_to_shell_configs():
    """Add 'umask 0002' to .bashrc and .zshrc"""
    home = Path.home()
    umask_line = "\n# Make new files group-writable by default (files 664, dirs 775 instead of 644/755)\numask 002\n"
    
    for config_file in [".bashrc", ".zshrc"]:
        config_path = home / config_file
        
        # Create file if it doesn't exist
        if not config_path.exists():
            config_path.touch()
        
        # Read existing content
        with open(config_path, "r") as f:
            content = f.read()
        
        # Add umask line if not already present
        if "umask 002" not in content:
            with open(config_path, "a") as f:
                f.write(umask_line)
            print(f"Added 'umask 002' to {config_path}")
        else:
            print(f"'umask 002' already exists in {config_path}")

if __name__ == "__main__":
    add_umask_to_shell_configs()