from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')
packages = find_packages(where='src.multiriver')
print(f"Discovered packages: {packages}")

setup(
    name="multiriver",
    version="1.1.8",
    packages=find_packages('src'),
    author="Oleksandr Baranov",
    author_email="oleksandr.baranov@rivery.io",
    description="A tool for bulk river creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'multiriver = multiriver.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "azure-storage-blob==12.23.1",
        "azure.identity==1.19.0",
        "click==7.1.2",
        "pymongo==3.13.0",
        "Requests==2.32.3",
        "rich==13.9.4",
        "simplejson==3.19.2"
    ],
)
