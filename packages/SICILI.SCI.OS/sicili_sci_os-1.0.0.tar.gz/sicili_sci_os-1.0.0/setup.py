from setuptools import setup, find_packages

setup(
    name="SICILI.SCI.OS",  # Name of your module
    version="1.0.0",
    packages=find_packages(),  # Automatically find packages in your project directory
    include_package_data=True,  # Ensure that package data is included
    package_data={
        'kernel': ['apps/*.py', 'BIOS/*.py'],  # Include .py files from subfolders
    },
    entry_points={
        "console_scripts": [
            "SICILI.SCI.OS=kernel.kernel:start_kernel",  # Entry point for the command-line script
        ],
    },
    install_requires=[
        "scratchattach",  # Third-party dependencies
    ],
    description="A command-line OS module",
    author="Shahzain Khan/ArtificialXDev",
    author_email="shahzaingenious@gmail.com",
    url="https://github.com/ArtificialXDev/SICILI.SCI.OS",
)
