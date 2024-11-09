from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / 'README.md').read_text()

setup(
        name="inputwhile",
        version="1.0.0",
        description="A simple input while loop utility",
        long_description=long_description,
        long_description_content_type='text/markdown',
        author="Benjas333",
        author_email="seston30@gmail.com",
        packages=find_packages(),
)
