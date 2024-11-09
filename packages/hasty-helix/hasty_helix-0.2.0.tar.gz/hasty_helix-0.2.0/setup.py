from setuptools import setup, find_packages

setup(
    name='hasty-helix',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'hasty-helix=hasty_helix.cli:main',
        ],
    },
    description='A package to analyze transactions from a CSV file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Semyon Drozdov',
    author_email='s.drozdov@edu.centraluniversity.ru',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
