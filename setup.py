"""Augment pandas DataFrame with common used methods"""
__version__ = '0.0.1'
import os
import re

from distutils.core import setup
from setuptools import find_packages
from setuptools.command.sdist import sdist

URL = 'https://github.com/Pandas-Quant-Finance/trade-engine'
NAME = 'trade-engine'


class SDist(sdist):

    def fix_github_links(self, lines):
        #   ist  https://github.com/KIC/pandas-ml-quant/pandas-ml-common/tree/0.2.0/./examples/
        #   soll https://github.com/KIC/pandas-ml-quant/tree/0.2.0/pandas-ml-common/./examples/
        def fix_line(line):
            fixed_images = re.sub(r'(^\[ghi\d+]:\s+)', f'\\1{URL}/raw/{__version__}/{NAME}/', line)
            fixed_location = re.sub(r'(^\[ghl\d+]:\s+)', f'\\1{URL}/tree/{__version__}/{NAME}/', fixed_images)
            fixed_files = re.sub(r'(^\[ghf\d+]:\s+)', f'\\1{URL}/blob/{__version__}/{NAME}/', fixed_location)
            return fixed_files

        return [fix_line(line) for line in lines]

    def make_release_tree(self, base_dir, files):
        # create the regular distribution files
        super().make_release_tree(base_dir, files)

        # but then fix the github links
        readme_file = os.path.join(base_dir, 'Readme.md')
        readme_lines = open(readme_file).readlines()

        with open(readme_file, 'w') as f:
            f.writelines(self.fix_github_links(readme_lines))


setup(
    name=NAME,
    version=__version__,
    author='KIC',
    author_email='',
    package_dir={'': NAME},
    packages=find_packages(where=NAME),
    scripts=[],
    url=f'{URL}/{NAME}',
    license='MIT',
    description=__doc__,
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={
    },
    include_package_data=True,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    keywords=['python', 'trade', 'engine'],
    cmdclass={
        'sdist': SDist
    },
)
