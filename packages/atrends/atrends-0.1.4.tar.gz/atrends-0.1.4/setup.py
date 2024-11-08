# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atrends']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5,<4.0', 'pytrends>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'atrends',
    'version': '0.1.4',
    'description': 'A project to fetch and plot Google Trends data',
    'long_description': None,
    'author': 'David Shivaji',
    'author_email': 'davidshivaji@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
