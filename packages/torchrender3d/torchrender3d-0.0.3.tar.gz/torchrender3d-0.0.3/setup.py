from skbuild import setup
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='torchrender3d',
    version='0.0.3',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['numpy==2.1.3', 'torch==2.5.1','torchvision==0.20.1', 'vtk==9.3.1', 'tqdm==4.66.6'],
    #install_requires=['numpy>=1.21.0', 'torch==2.4.1','torchvision>=0.16.0', 'vtk==9.3.1', 'tqdm==4.66.6'],
    author='Tanumoy Saha',
    author_email='sahat@htw-berlin.de',
    description='Render NNs in 3D',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ml-ppa-derivatives/torchrender3d',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10'
)