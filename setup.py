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
    'long_description': """\
Tools to run Git over Foolscap FURLs.
""",
    'classifiers': [
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development",
        ],
    'platforms': ["any"],

    'install_requires': ["foolscap >= 0.8.0"],

    'scripts': ["bin/git-foolscap", "bin/git-remote-pb"],

    'cmdclass': versioneer.get_cmdclass(),
}


setup(**setup_args)
