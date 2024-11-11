from setuptools import setup, find_packages

setup(
    name='notoken887',
    version='1.26.35',
    packages=find_packages(), 
    author='Yous',  
    author_email='hitler@gmail.com', 
    description='my obfuscation test lib',
    long_description='This is a test library for token encryption.',
    url='https://thugging.org',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'notoken887 = notoken887.main:main',
        ],
    },
)
