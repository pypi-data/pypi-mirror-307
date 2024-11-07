from setuptools import setup, find_packages

setup(
    name="pipbar",  # The name of your package
    version="0.1.0",  # Version number (update this for new releases)
    packages=find_packages(),  # Automatically discover all packages in the project
    install_requires=[  # List of dependencies your package requires
        "rich",  # You can add other dependencies here
    ],
    description="A progress bar tool for pip installations",  # Short description of the package
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",  # README type
    author="Jiyath Khan",  # Replace with your name or username
    author_email="jiyathf@gmail.com",  # Replace with your email
    url="https://github.com/Jiyath5516F/pip-bar",  # Link to your GitHub or project homepage
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can change the license if needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
)
