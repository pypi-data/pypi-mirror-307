from setuptools import setup, find_packages

setup(
    name='toffeepirates',  # The name of the package you want to publish
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.2',
    ],
    description='A Flask-based application for Toffee Pirates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/toffeepirates',  # GitHub URL of the project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'toffeepirates=toffeepirates.app:main',  # Entry point for the app
        ],
    },
)
