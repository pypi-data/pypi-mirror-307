from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="NetManage",
    version="0.1.3",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Jakub Olejnik",
    author_email="jacobole2000@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'NetManage=NetManage.__main__:main',
        ],
    },

)
