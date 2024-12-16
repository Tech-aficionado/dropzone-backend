from setuptools import setup, find_packages

setup(
    name="Jholi-fastapi",
    version="0.1.0",
    author="Shivansh Goel",
    author_email="shivansh.goela12@gmail.com",
    description="A short description of your package",
    packages=find_packages(),
    install_requires=[
        "mariadb",
    ],
    # ... other metadata
)
