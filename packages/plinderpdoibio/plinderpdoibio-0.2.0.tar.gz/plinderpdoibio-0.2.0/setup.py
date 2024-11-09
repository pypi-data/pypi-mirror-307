from setuptools import setup, find_packages

setup(
    name='plinderpdoibio',
    version='0.2.0',
    description='A Python package to interact with the Plinderp DOI Bio API.',
    author='doi.bio',
    author_email='doidotbio@gmail.com',
    url='https://github.com/doi-dot-bio/plinderp',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
