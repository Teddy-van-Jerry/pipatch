from pipatch import Pipatch
import os

def main():
    # Initialize the Pipatch object
    pipatch = Pipatch("requests", "2.25.1", print_log=True)

    # Get the package directory and version
    package_dir, package_version = pipatch.package_dir, pipatch.package_version
    print(f"[INFO] Package directory: {package_dir}\n[INFO] Package version: {package_version}")

    # Check if the versions match
    versions_match = pipatch.versions_match()
    print(f"[INFO] Versions match: {versions_match} (patched for: {pipatch.version}, actual: {pipatch.package_version})")

    # Download a file
    url = "https://github.com/psf/requests/blob/main/src/requests/__init__.py"
    temp_file = "requests.py"
    pipatch.download_file(url, temp_file)
    def remove_temp_file():
        if os.path.exists(temp_file):
            os.remove(temp_file)
    remove_temp_file()

if __name__ == "__main__":
    main()
