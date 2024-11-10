from setuptools import setup, find_packages

setup(
    name='superpacman',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pygame',
    ],
    include_package_data=True,
    license='MIT',
    description='A sample Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='',
    author_email='',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
