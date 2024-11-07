from setuptools import setup, find_packages

setup(
    name='testing_step_generator',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    description='A CLI tool for initializing and generating output.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='kel89@cornell.edu',
    url='https://github.com/kel89',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'tsg=tsg.cli:main',
        ],
    },
    python_requires='>=3.6',
)
