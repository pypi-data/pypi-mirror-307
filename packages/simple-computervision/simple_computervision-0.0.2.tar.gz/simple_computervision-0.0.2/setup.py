import setuptools


__version__ = "0.0.2"
AUTHER_NAME = "Sathishmahi"
SRC_REPO = "simple_computervision"
REPO_NAME = "simple_computervision"
AUTHER_EMAIL = "sathishmahi433@gmail.com"

with open("README.md",mode="r") as f:
    long_description = f.read()

setuptools.setup(name = SRC_REPO,
                 version=__version__,
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author_email=AUTHER_EMAIL,
                 author=AUTHER_NAME,
                 url=f"https://github.com/sathishmahi/{REPO_NAME}",
                 package_dir={"":"src"},
                 packages=setuptools.find_packages(where="src"),
                description="A small python package",
                  )
