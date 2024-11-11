from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from setuptools import Command
import os
import platform
import subprocess
import shutil
import glob
import sysconfig
import sys


class bdist_wheel(_bdist_wheel):
    def run(self):
        self.run_command('build_ext')  
        super().run()


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        build_temp = os.path.abspath(self.build_temp)
        build_lib = os.path.abspath(self.build_lib)

        python_executable = sys.executable
        python_include_dir = sysconfig.get_path('include')

        # Determine the platform-specific library suffix
        if platform.system() == "Windows":
            python_library_file = f"python{py_version}.dll"
        elif platform.system() == "Darwin":  # macOS
            python_library_file = f"libpython{py_version}.dylib"
        else:  # Linux/Unix
            python_library_file = f"libpython{py_version}.so"

        python_library_dir = sysconfig.get_config_var('LIBDIR')
        python_library = os.path.join(python_library_dir, python_library_file) if python_library_dir else None

        cmake_args = [
            f"-DPython3_EXECUTABLE={python_executable}",
            f"-DPython3_INCLUDE_DIRS={python_include_dir}",
            f"-DPython3_VERSION={py_version}",
            f"-DPython3_LIBRARIES={python_library}" if python_library else "",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        build_args = ['--config', 'Release']

        if platform.system() == "Windows":
            cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            build_args += ['--', '-j2']

        os.makedirs(build_temp, exist_ok=True)

        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=build_temp)

        # Copy built files
        self._copy_generated_files(build_temp, build_lib, "autopysta")

    def _copy_generated_files(self, build_temp, build_lib, extra_copy):
        swig_generated_py = glob.glob(os.path.join(build_temp, '**', 'autopysta.py'), recursive=True)
        swig_generated_lib = glob.glob(os.path.join(build_temp, '**', '_autopysta.*'), recursive=True)

        os.makedirs(build_lib, exist_ok=True)

        for file_list in [swig_generated_py, swig_generated_lib]:
            for file in file_list:
                shutil.copy(file, build_lib)
                shutil.copy(file, extra_copy)


        example_dir = os.path.join('examples', 'autopysta')
        os.makedirs(example_dir, exist_ok=True)

        for file in glob.glob('autopysta/*'):
            if os.path.basename(file) in ['autopysta.py', '__init__.py'] or file.endswith(tuple(glob.glob('autopysta/_autopysta.*'))):
                shutil.copy(file, example_dir)

class CMakeClean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_dirs = ['build', 'dist', 'autopysta.egg-info']
        for build_dir in build_dirs:
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)

        # Clean up specific files in autopysta and examples/autopysta
        directories_to_clean = [
            os.path.abspath("autopysta"),
            os.path.abspath(os.path.join("examples", "autopysta"))
        ]

        for dir_path in directories_to_clean:
            if os.path.exists(dir_path):
                # Remove autopysta.py and _autopysta.* files
                for file_pattern in ['autopysta.py', '_autopysta.*']:
                    for file in glob.glob(os.path.join(dir_path, file_pattern)):
                        os.remove(file)

def read_version():
    with open("VERSION", "r") as f:
        return f.read().strip()

setup(
    name='autopysta',
    version=read_version(),
    author='Rafael Delpiano',
    description='2D traffic modeling.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rdelpiano/autopysta/",
    ext_modules=[CMakeExtension('autopysta', sourcedir='.')],
    cmdclass={
        'build_ext': CMakeBuild,
        'clean': CMakeClean,
        'bdist_wheel': bdist_wheel,
    },
    install_requires=["matplotlib"],
    packages=find_packages(include=["autopysta"]),
    package_data={
        'autopysta': ['*.py', '_autopysta.*'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
