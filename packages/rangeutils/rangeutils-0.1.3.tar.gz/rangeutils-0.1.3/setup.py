# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rangeutils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'rangeutils',
    'version': '0.1.3',
    'description': 'Utilities for manipulating and converting Python ranges and boolean lists',
    'long_description': '# rangeutils\n\n`rangeutils` is a Python package that provides utilities for converting, manipulating, and processing Python `range` objects and boolean lists. This package includes a variety of functions to convert between boolean lists and ranges, merge adjacent ranges, find complementary ranges, and trim ranges based on specific conditions.\n\n## Features\n\n- **Convert lists to ranges**: Convert `[start, end]` lists to Python range objects, with optional handling for `None` values.\n- **Boolean list to ranges**: Converts a boolean list to a list of range objects representing `True` or `1` sequences.\n- **Ranges to boolean list**: Converts a list of ranges back to a boolean list of specified length.\n- **Flip ranges**: Generate complementary ranges that are not covered by input ranges.\n- **Fill ranges**: Fill ranges that are within a specified gap size.\n- **Trim ranges**: Perform trimming on ranges based on length, percentage, or a specified trimming size.\n\n## Installation\n\nYou can install `rangeutils` using pip:\n\n```bash\npip install rangeutils\n',
    'author': 'kris.wang',
    'author_email': 'wenhom.wang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hom-Wang/rangeutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
