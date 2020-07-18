from setuptools import setup, find_packages

VERSION = '0.0.25'

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setup(
    name='spotify-cli',
    version=VERSION,
    author='Benj Ledesma',
    author_email='benj.ledesma@gmail.com',
    description='Control Spotify playback on any device through the command line.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ledesmablt/spotify-cli',
    license=license,

    packages=find_packages(),
    install_requires=[
        'Click',
        'PyInquirer',
    ],
    entry_points='''
        [console_scripts]
        spotify=cli.spotify:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
