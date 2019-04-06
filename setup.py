import os

from setuptools import setup

requires = []


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setup(
    # Basic package information:
    name='pythonish-validator',
    version='0.3',
    py_modules=('pythonish_validator',),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,
    packages=('pythonish_validator',),

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],

    # Package dependencies:
    requires=requires,
    tests_require=requires + ["pytest"],
    setup_requires=requires + ["pytest-runner"],
    install_requires=requires,

    # Metadata for PyPI:
    author='Georgy Bazhukov',
    author_email='georgy.bazhukov@gmail.com',
    license='BSD',
    url='https://github.com/bugov/pythonish-validator',
    keywords='validator data check structure scheme',
    description='Pythonish object scheme validator',
    long_description=read('readme.md'),
)