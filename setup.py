try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Heat Transfer',
    'author': 'Daniel Magee',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'mageed@oregonstate.edu',
    'version': '0.01',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)