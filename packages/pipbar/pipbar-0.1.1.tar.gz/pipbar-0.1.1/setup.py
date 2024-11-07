from setuptools import setup, find_packages

setup(
    name="pipbar",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    description="A progress bar tool for pip installations",
    long_description=open("README.md", encoding="utf-8").read(),  # Fixed encoding issue
    long_description_content_type="text/markdown",
    author="Jiyath Khan",
    author_email="jiyathf@gmail.com",
    url="https://github.com/Jiyath5516F/pip-bar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
