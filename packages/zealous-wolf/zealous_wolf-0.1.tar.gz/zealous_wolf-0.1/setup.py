# setup.py

from setuptools import setup, find_packages

setup(
    name='zealous_wolf',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'zealous-wolf=zealous_wolf.metrics:main',
        ],
    },
    description='A package to calculate net profit and ROI.',
    author='Semyon Drozdov',
    author_email='s.drozdov@edu.centraluniversity.ru',
    url='https://example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
