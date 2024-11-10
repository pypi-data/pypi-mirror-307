from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / 'README.md').read_text()

setup(
        name="inputwhile",
        version="1.0.2",
        description="A simple input while loop utility",
        long_description=long_description,
        long_description_content_type='text/markdown',
        author="Benjas333",
        packages=find_packages(),
)
