from setuptools import setup, find_packages

setup(
    name='pasir',
    version='0.0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Your dependencies
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            # If you have any console scripts, specify them here
        ],
    },
    url='https://github.com/dudung/pasir',
    license='MIT',
    author='Sparisoma Viridi',
    author_email='dudung@gmail.com',
    description='granular-based simulation and related systems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
