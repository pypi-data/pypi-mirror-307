from setuptools import setup, find_packages

version = '0.9'

long_description = (
    open('README.rst').read() +
    '\n' +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')

setup(
    name='robotframework-djangolaunch',
    version=version,
    description="A Robot Framework library for starting and stopping Django.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Web Environment',
        'Framework :: Robot Framework',
        'Framework :: Django',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='robotframework django test',
    author='Martti Rannanjärvi',
    author_email='martti.rannanjarvi@iki.fi',
    url='https://github.com/mrannanj/robotframework-djangolaunch',
    license='Apache License 2.0',
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'tests']
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django',
        'robotframework',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
