from setuptools import setup, find_packages

setup(
    name='computer_sim',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'computer_sim=main:main',  # Adjust if your main function is named differently
        ],
    },
    author='Roberto Scalas',
    author_email='scalas.roberto@gmail.com',
    description='A computer simulation package',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/robsca/computer_sim',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)