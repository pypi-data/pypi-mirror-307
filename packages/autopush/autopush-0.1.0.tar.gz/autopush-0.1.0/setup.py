from setuptools import setup, find_packages
from pathlib import Path

try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = "AutoPush CLI Tool for simplified Git commands"

setup(
    name='autopush',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'gitpython',
        'inquirepy',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'autopush=bin.main:main',  # Make sure this path exists in your project
        ],
    },
    author='w3cdpass',
    author_email='kupasva663@gmail.com',
    description='autopush cli tool allows to run git commands more simply',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/w3cdpass/autopush',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
