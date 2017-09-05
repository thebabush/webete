from setuptools import setup

setup(
    name='webete',
    version='0.1',
    description='WEBETE - WEB Extensive Testing Environment',
    url='https://github.com/kenoph/webete',
    author='Paolo Montesel',
    license='GPLv3',
    packages=['webete'],
    entry_points={
        'console_scripts': [
            'webete=webete.webete:main'
        ],
    },
    install_requires=[
        'requests',
        'uncompyle6',
    ],
    classifiers=[
    ],
    zip_safe=False
)

