#!/usr/bin/env python

from setuptools import setup
import versioneer

setup_args = {
    'name': "git-foolscap",
    'version': versioneer.get_version(),
    'description': "Tools to run Git over Foolscap FURLs.",
    'author': "Brian Warner",
    'author_email': "warner-foolscap@lothar.com",
    'url': "https://github.com/warner/git-foolscap",
    'license': "MIT",
    'long_description': open("README.md").read(),
    'classifiers': [
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development",
        ],
    'platforms': ["any"],

    'python_requires': ">=3.5",
    'install_requires': ["foolscap >= 20.4.0",
                         "magic-wormhole >= 0.10.5",
                         ],

    'scripts': ["bin/git-foolscap", "bin/git-remote-pb"],

    'cmdclass': versioneer.get_cmdclass(),
}


setup(**setup_args)
