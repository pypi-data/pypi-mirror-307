from setuptools import setup, find_packages

setup(
    name="UseMod",
    version="1.0.1",
    author="Grivy16",
    author_email="grivy16public@gmail.com",
    description="UseMod",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Grivy16/UseMod/wiki",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "UseMod": ["assets/*.ico", "assets/*.jpg"],  # Chemin vers les images dans le dossier UseMod/assets
    },
    install_requires=[
        'requests',
        'dropbox',
        "clipboard",
        "customtkinter",
        "PIL",
        "tkinter",
        "json",
        "base64",
        "setuptools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
