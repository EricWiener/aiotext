from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install


class InstallWrapper(install):
    """Install punkt."""

    def run(self):
        # Run this first so the install stops in case
        # these fail otherwise the Python package is
        # successfully installed
        self._post_install()
        # Run the standard PyPi copy
        install.run(self)

    def _post_install(self):
        """Post-installation for installation mode."""
        print("Downloading wordnet")
        import nltk
        nltk.download('wordnet')
        print("Download succeeded")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aiotext",
    version="1.0.1",
    author="Eric Wiener",
    author_email="ericwiener3@gmail.com",
    description="All in one text processor and cleaner.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EricWiener/aiotext",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'scikit-learn',
        'pycontractions',
        'nltk',
    ],
    packages=["aiotext"],
    cmdclass={
        'install': InstallWrapper
    },
)
