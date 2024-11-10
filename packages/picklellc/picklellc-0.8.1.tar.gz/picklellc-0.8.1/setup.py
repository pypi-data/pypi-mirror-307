from setuptools import setup, find_packages

setup(
    name='picklellc',
    version='0.8.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy'
    ],
    author='Pickle LLC',    
    author_email='peterfarag12@gmail.com',
    description='Python client for Pickle LLC API',
    long_description="A package to submit requests to the Pickle API for NP problems and AI training and Solutions with Pickle's algorithms",
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)