from setuptools import setup, find_packages

setup(
    name="tractor_db",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get-tractor=tractor_db.main:get_tractor_name',
        ],
    },
    author="Mike Lawson",
    author_email="mike@allmachines.com",
    description="A package to get random tractor information",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'tractor_db': ['db.json'],
    },
)
