from setuptools import setup, find_packages

setup(
    name='pyoncokb',               # The name of your package
    version='0.0.3',                 # Initial version
    description='A simple package for OncoKB API',
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',
    author='Mark J Chen',
    author_email='mjchen.gene@gmail.com',
    url='https://github.com/markgene/pyoncokb',  # Project URL
    packages=find_packages(),         # Automatically find all packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',          # Minimum Python version
    install_requires=[                # List of dependencies
        'dacite',
        'requests',                   # Add your dependencies here
    ],
)
