from setuptools import setup, find_packages

setup(
    name='snvannotators',               # The name of your package
    version='0.0.1',                 # Initial version
    description='SNV annotation',
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',
    author='Mark J Chen',
    author_email='mjchen.gene@gmail.com',
    url='https://github.com/markgene/snvannotators',  # Project URL
    packages=find_packages(),         # Automatically find all packages
    # include_package_data=True,  # Ensure package data is included
    # package_data={
    #     'my_package': ['data/*.csv'],  # Include specific data files
    # },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',          # Minimum Python version
    install_requires=[                # List of dependencies
        'pyoncokb',                   # Add your dependencies here
        'snvmodels',
        'transcriptfeatures',
        'myvariant',
        'hgvs',
    ],
)
