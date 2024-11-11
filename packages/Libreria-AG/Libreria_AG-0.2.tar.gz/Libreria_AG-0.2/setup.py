from setuptools import setup, find_packages

setup(
    name='Libreria_AG',
    version='0.2',
    description='A genetic algorithm optimization library',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'matplotlib>=3.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
