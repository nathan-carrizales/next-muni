from setuptools import setup
from setuptools import setup, find_packages

setup(
    name='next_muni',
    version='0.1.0',
    author='Nathan Carrizales',
    packages=find_packages(),
    license='Public',
    description='',
    install_requires=[
        'numpy==1.23.3',
        'pandas==1.5.0',
        'requests==2.28.1',
        'playsound==1.3.0',
        'PyObjC'
    ]
)
