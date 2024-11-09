from setuptools import setup, find_packages

setup(
    name='cosinorage',
    version='0.1.0',
    description='A package for computing the ConsinorAge from raw '
                'accelerometer data.',
    author='Jacob Leo Oskar Hunecke',
    url='https://github.com/jlohunecke/CosinorAge.git',
    packages=find_packages(),  # Automatically finds subpackages
    install_requires=[],  # Add any dependencies here

    extras_require={
        'docs': [
            'sphinx',
            'furo',
            'pandas',
            # other doc dependencies
        ],
    },
)
