from setuptools import setup, find_packages

setup(
    name="create-lillie",  
    version="0.1.0",  
    description="A tool for creating lilliepy projects",  
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create-lillie=create_lillie.main:create',
        ],
    },
    install_requires=[ 
        'typer',
        'colorama',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
