from setuptools import setup, find_packages

setup(
    name='spotify-cli',
    version='0.0.25',
    author='Benj Ledesma',
    description='Control Spotify playback on any device through the command line.',
    url='https://github.com/ledesmablt/spotify-cli',

    packages=find_packages(),
    install_requires=[
        'Click',
        'PyInquirer',
    ],
    entry_points='''
        [console_scripts]
        spotify=cli.main:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
