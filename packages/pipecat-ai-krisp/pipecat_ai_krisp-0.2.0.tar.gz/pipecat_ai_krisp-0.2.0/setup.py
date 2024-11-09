from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import os
import subprocess
import shutil
import re


class CustomBuild(build_ext):
    def run(self):
        build_script = "./scripts/build.sh"
        if not os.access(build_script, os.X_OK):
            print(f"Making {build_script} executable...")
            os.chmod(build_script, 0o755)

        print("Running build.sh script...")
        subprocess.check_call(build_script)

        # Locate the built library in lib/bin
        lib_dir = os.path.join("lib", "bin")
        pattern = r"krisp_python\..*\.so"

        try:
            files = os.listdir(lib_dir)
        except FileNotFoundError:
            raise FileNotFoundError(f"Library directory not found: {lib_dir}")

        matching_files = [f for f in files if re.match(pattern, f)]
        if not matching_files:
            raise FileNotFoundError(
                f"No library file matching pattern '{pattern}' found in {lib_dir}"
            )

        # Copy the built library to the `src` directory
        src_dir = os.path.join(os.path.dirname(__file__), "src", "pipecat_ai_krisp")
        for file in matching_files:
            shutil.copy(os.path.join(lib_dir, file), src_dir)
            print(f"Copied {file} to {src_dir}")

        # Copying all files and directories from src_dir to build_lib_dir
        # We need this to make it work after we install this package in other libraries
        # Since we are only creating the .so after the user provides the Krisp SDK
        # path and install time
        pipecat_ai_krisp_dir = os.path.join(self.build_lib, "pipecat_ai_krisp")
        os.makedirs(pipecat_ai_krisp_dir, exist_ok=True)
        for root, dirs, files in os.walk(src_dir):
            # Calculate the relative path from the src_dir root
            relative_path = os.path.relpath(root, src_dir)
            # Destination directory path in build_lib
            dest_dir = os.path.join(pipecat_ai_krisp_dir, relative_path)
            os.makedirs(dest_dir, exist_ok=True)  # Create directories as needed

            # Copy each file in the current directory
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                shutil.copy(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")


setup(
    name="pipecat_ai_krisp",
    version="0.1.0",
    ext_modules=[Extension("krisp_python", sources=[])],
    cmdclass={"build_ext": CustomBuild},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
