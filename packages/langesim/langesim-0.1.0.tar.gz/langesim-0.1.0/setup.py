# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langesim']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupyterlab>=3.5.2,<4.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'langesim',
    'version': '0.1.0',
    'description': 'Langevin simulator of an overdamped brownian particle in an arbitrary time-dependent potential',
    'long_description': '# langesim\n\nLangevin simulator of an overdamped brownian particle in an arbitrary\ntime-dependent potential.\n\nSee the documentation at:\n\nhttps://gabrieltellez.github.io/langesim/\n',
    'author': 'Gabriel Tellez',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
