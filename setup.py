from setuptools import setup

setup(
    name='spotify',
    version='0.1',
    py_modules=['spotify'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        spotify=spotify:cli
    ''',
)
