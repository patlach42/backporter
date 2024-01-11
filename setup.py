from setuptools import setup

setup(
    name='backporter',
    version='0.1',
    py_modules=['backporter'],
    entry_points={
        'console_scripts': [
            'backporter = backporter:cli',
        ],
    },
)
