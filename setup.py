from setuptools import setup
from setuptools import find_packages

setup(
    name = "Timed-Client",
    version = "0.0.1",
    packages = find_packages('.'),
    entry_points = {
        'console_scripts': [
            'timed = timed_client.cli:main',
        ]
    },
    install_requires = [
        'click',
        'pyyaml',
        'requests',
        'pytz',
        'texttable',
        'pytimeparse',
    ],

    author = "Adfinis-Sygroup AG",
    author_email = "http://adfinis-sygroup.ch/contact",
    description = "Commandline client for Timed",
    license = "Modified BSD",
    keywords = "adfinis-sygroup time-tracking",
    url = "http://adfinis-sygroup.ch",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
