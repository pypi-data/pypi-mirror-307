from setuptools import setup, find_packages

setup(
    name="tnr",
    version="1.4.16",
    package_dir={"": "src"},  # Specify the root directory for packages
    packages=find_packages(where="src"),  # Tell setuptools to find packages under src
    include_package_data=True,  # Include other files specified in MANIFEST.in
    install_requires=[
        "Click>=8.0",  # Specify a minimum version if needed
        "requests>=2.2",  # Same here, adjust the version as per your compatibility requirements
        "cryptography>=40.0",  # Adjust based on the features you're using
        "pathlib>=1.0.1",
        "packaging>=21.0",
        "paramiko==3.4.0",
        "yaspin==3.0.2",
        "scp==0.15.0",
        "rich-click==1.8.3",
        "rich==13.7.1",
    ],
    entry_points={"console_scripts": ["tnr=thunder.thunder:cli"]},
)

# delete old dist folder first, and increment version number

# to build: python3 setup.py sdist bdist_wheel
# to distribute: twine upload dist/*
