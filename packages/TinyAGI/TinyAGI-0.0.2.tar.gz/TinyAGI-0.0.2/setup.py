# setup.py

from setuptools import setup, find_packages

setup(
    name='TinyAGI',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'ollama',
        'gitpython',
        'python-dotenv',
        'flask',
        # Add any other dependencies required by plugins
        'black',  # For code formatting
        # 'jsbeautifier',  # Example for JavaScript formatting
    ],
    include_package_data=True,
    description='TinyAGI is a modular AI agent framework controlled via JSON configuration.',
    author='Sully Greene',
    url='https://github.com/SullyGreene/TinyAGI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
