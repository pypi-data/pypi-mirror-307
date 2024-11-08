from setuptools import setup, find_packages

setup(
    name="multiriver",
    version="1.1.1",
    packages=find_packages(),
    author="Oleksandr Baranov",
    author_email="oleksandr.baranov@rivery.io",
    description="A tool for bulk river reation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    entry_points={
        'console_scripts': [
            'multiriver = bulk_river_creation.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['azure_blob_session'],
    include_package_data=True,
    install_requires=[
        "azure_storage==0.36.0",
        "azure-storage-blob==12.23.1",
        "azure.identity==1.19.0",
        "click==7.1.2",
        "pymongo==3.13.0",
        "Requests==2.32.3",
        "rich==13.9.4",
        "simplejson==3.19.2"
    ],
)
