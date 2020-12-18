from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ezMail',
    version='0.0.2',
    description='Easy to use python mailing app',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Jirapong Pansak',
    author_email='me@jirapongpansak.com',
    license='MIT',
    classifiers=classifiers,
    keywords='emails',
    packages=find_packages(),
    install_requires=[''],
    download_url="https://github.com/MaoMaoCake/ezMail/archive/v0.0.2.tar.gz"
)