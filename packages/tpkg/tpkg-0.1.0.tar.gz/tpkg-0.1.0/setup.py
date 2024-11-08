from setuptools import setup, find_packages

setup(
    name='tpkg',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    author='Prince Jassi',
    author_email='princejassi@cssoftsolutions.com',
    description='This package is only for the testing purpose',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/prince-jassi-m/python_package.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
