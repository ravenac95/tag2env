import re
from setuptools import setup, find_packages

# Parse the version from the __init__.py file
version = ''
with open('tag2env/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name="tag2env",
    version=version,
    license="MIT",
    author="Reuven V. Gonzales",
    url="https://github.com/ravenac95/tag2env",
    author_email="reuven@virtru.com",
    description="Turns EC2 tags into environment variables",
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='*nix',
    install_requires=[
        "boto3==1.2.3",
        "python-json-logger==0.1.2",
        "click==5.0",
        "requests==2.9.1",
    ],
    entry_points={
        'console_scripts': [
            'tag2env = tag2env.cli:cli',
        ],
    },
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
