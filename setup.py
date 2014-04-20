import ast
import codecs
import os
import sys

from setuptools import setup, find_packages


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version

install_requires = [
    'pyserial==2.7'
]

# We only want to install asyncio on Python 3.3 - it comes with 3.4 and wont
# work on earlier versions.
if sys.version_info[:2] == (3, 3):
    install_requires.append('asyncio==0.4.1')

setup(
    name="rfxcom",
    version=find_version("rfxcom", "__init__.py"),
    url='https://github.com/d0ugal/rfxcom',
    license='BSD',
    description="RFXCOM RFXtrx Library for Python 3.3+",
    long_description=read('README.rst'),
    author='Dougal Matthews',
    author_email='dougal@dougalmatthews.com',
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)
