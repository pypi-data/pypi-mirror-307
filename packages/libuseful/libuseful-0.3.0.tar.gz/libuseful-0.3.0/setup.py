# -*- coding: utf-8 -*-
import os
import platform
from setuptools import setup, find_packages
from libuseful import __version__

# Collect file-path as list in specific-directory with wanted relative-path.
def package_files(directory:str, stand_dir:str) -> list:
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        rel_dir = os.path.relpath(path, stand_dir)
        for filename in filenames:
            paths.append(os.path.join( rel_dir, filename))
    return paths


if( platform.system() == "Linux" ):
    setup_requires = [
        'numpy>=1.19.5',
        'python-dateutil>=2.8.2',
        'pandas>=1.1.5',
        'opencv-python>=4.8.1',
        'chardet>=5.2.0',
        'psutil>=6.0.0',
        'openpyxl>=3.1.5',
        'retry>=0.9.2'
    ]

    install_requires = [
        'numpy>=1.19.5',
        'python-dateutil>=2.8.2',
        'pandas>=1.1.5',
        'opencv-python>=4.8.1',
        'chardet>=5.2.0',
        'psutil>=6.0.0',
        'openpyxl>=3.1.5',
        'retry>=0.9.2'
    ]
        
elif( platform.system() == "Windows" ):
    setup_requires = [
        'numpy>=1.19.5',
        'python-dateutil>=2.8.2',
        'pandas>=1.1.5',
        'opencv-python>=4.8.1',
        'chardet>=5.2.0',
        'psutil>=6.0.0',
        'openpyxl>=3.1.5',
        'retry>=0.9.2'
    ]

    install_requires = [
        'numpy>=1.19.5',
        'python-dateutil>=2.8.2',
        'pandas>=1.1.5',
        'opencv-python>=4.8.1',
        'chardet>=5.2.0',
        'psutil>=6.0.0',
        'openpyxl>=3.1.5',
        'retry>=0.9.2'
    ]
        

dependency_links = [
    # 'git+http://1626534@mgit.mobis.co.kr/bitbucket/scm/mvpu1_0/MVPU1.0.annotation_interface.git@release/v2.3#egg=mvpuai'
]

setup(
    name='libuseful',
    version=__version__,
    license="Commutial-License",
    author=['Eunseok Kim'],
    author_email=['es.odysseus@gmail.com'],
    description="It's useful library, commonly. (path/file/shell/thread/process/watchdog/async/args/logger/retry/singleton/time/cam/dynamic_import/excel/geometry_math/user_mng)",
    packages=find_packages(where='.', exclude=['.vscode', '_venv_', '_run_script_']),
    long_description=open('README.md', "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    package_data={
        'libuseful' : [] 
    },
    zip_safe=False,
    setup_requires=setup_requires,

    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    python_requires='>=3.8.0',
    keywords=["libuseful", "useful", "library", "common-lib", "util"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ]
)
# END_OF_FILE

