# setup.py

from setuptools import setup

setup(
    name='md_replace',
    version='1.0.0',
    py_modules=['md_replace'],
    entry_points={
        'console_scripts': [
            'md_replace=md_replace:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Replace file paths in markdown files with the contents of the files.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://your.repository.url',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
