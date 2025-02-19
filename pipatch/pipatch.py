import importlib.metadata
import os
from pathlib import Path
import shutil
import requests

class Pipatch:
    def __init__(self, package_name: str, version: str, print_log: bool = False):
        self.package_name = package_name
        self.version = version
        self.print_log = print_log
        self.has_error = False

        try:
            self.package_dir, self.package_version = self.get_package_info()
        except ModuleNotFoundError:
            self.has_error = True
        pass

    def get_package_info(self):
        try:
            import importlib.util
            spec = importlib.util.find_spec(self.package_name)
            if spec is None:
                raise ModuleNotFoundError
            return Path(spec.origin).parent, importlib.metadata.version(self.package_name)
        except ModuleNotFoundError:
            if self.print_log:
                print(f"[ERROR] Package '{self.package_name}' not found.")
            raise ModuleNotFoundError(f"Package '{self.package_name}' not found.")

    def versions_match(self) -> bool:
        if self.has_error:
            if self.print_log:
                print(f"[ERROR] Exiting.")
            return False
        return self.version == self.package_version

    def download_file(self, url: str, filename: str):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            if self.print_log:
                print(f"[INFO] Downloaded file from {url} to {filename}.")
        except Exception as e:
            if self.print_log:
                print(f"[ERROR] Failed to download file: {e}")
            raise e

    def replace_file(self, filename: str, new_file: str) -> bool:
        if self.has_error:
            if self.print_log:
                print(f"[ERROR] Exiting.")
            return False
        if not self.package_dir:
            if self.print_log:
                print(f"[ERROR] Exiting.")
            self.has_error = False
            return False

        original_file = self.package_dir / filename
        new_file_path = Path(new_file)

        if not original_file.exists():
            if self.print_log:
                print(f"[ERROR] File {original_file} does not exist in the package.\n[ERROR] Exiting.")
            self.has_error = False
            return False

        if not new_file_path.exists():
            if self.print_log:
                print(f"[ERROR] File {new_file_path} does not exist.\n[ERROR] Exiting.")
            self.has_error = False
            return False

        # Replace the file
        try:
            shutil.copy(new_file, original_file)
            if self.print_log:
                print(f"[INFO] Replaced {original_file} with {new_file_path}.")
            return True
        except Exception as e:
            self.has_error = False
            print(f"[ERROR] Failed to replace file: {e}")
            return False

    def replace_file_from_url(self, filename: str, url: str) -> bool:
        # Download the new file
        temp_file = "temp_new_file.py"
        if not self.download_file(url, temp_file):
            return False

        def remove_temp_file():
            if os.path.exists(temp_file):
                os.remove(temp_file)

        # Replace the file
        if not self.replace_file(filename, temp_file):
            remove_temp_file()
            return False

        remove_temp_file()
        return True
