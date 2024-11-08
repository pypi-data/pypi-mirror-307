import os
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

__version__ = "0.2.0"

packages = find_packages(exclude=("deeva.tests",))
setup(
    name="deeva",
    version=__version__,
    author = read("AUTHORS.txt").replace('\n', ', ').replace('-', ''),
    author_email="vahram.babadjanyan@gmail.com",
    description="Object Detection Data Analysis Toolbox",
    long_description=read('README.md'),
    long_description_content_type = 'text/markdown',
    keywords = "object-detection analysis visualization data",
    url = "https://github.com/vbyan/DEEVA",
    packages=packages,
    package_dir={"DEEVA": "deeva"},
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'deeva=deeva.start:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)