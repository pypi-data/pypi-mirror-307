from setuptools import setup, find_packages
import os

setup(
    name="auto_clean_data",  # Just the package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'matplotlib',
        'pymysql',
        'psycopg2',
        'pyodbc'
    ],
    entry_points={
        'console_scripts': [
            'auto_clean=auto_clean.main:main',  # Corrected to reflect your script entry point
        ],
    },
    include_package_data=True,
    long_description=open('README.md').read() if os.path.exists('README.md') else "Your package description goes here.",
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
