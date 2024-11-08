# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streaming_form_data']

package_data = \
{'': ['*']}

install_requires = \
['smart-open>=6.0,<7.0']

setup_kwargs = {
    'name': 'streaming-form-data',
    'version': '1.19.0',
    'description': 'Streaming parser for multipart/form-data',
    'long_description': '# Streaming multipart/form-data parser\n\n[![image](https://img.shields.io/pypi/v/streaming-form-data.svg)](https://pypi.python.org/pypi/streaming-form-data)\n[![image](https://img.shields.io/pypi/pyversions/streaming-form-data.svg)](https://pypi.python.org/pypi/streaming-form-data)\n[![Downloads](https://static.pepy.tech/badge/streaming-form-data)](https://pepy.tech/project/streaming-form-data)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)\n\n`streaming_form_data` provides a Python parser for parsing `multipart/form-data`\ninput chunks (the encoding used when submitting data over HTTP through HTML\nforms).\n\n## Testimonials\n\n> [_this speeds up file uploads to my Flask app by **more than factor 10**_](https://github.com/pallets/werkzeug/issues/875#issuecomment-429287766)\n\n> [_Thanks a lot for your fix with streaming-form-data. I can finally upload gigabyte sized files at good speed and without memory filling up!_](https://github.com/pallets/werkzeug/issues/875#issuecomment-530020990)\n\n> [_huge thanks to @siddhantgoel with his "streaming-form-data" that saves me from the slow file reads I get with @FastAPI!_](https://twitter.com/bebenzrr/status/1654952147132248064)\n\n## Installation\n\n```bash\n$ pip install streaming-form-data\n```\n\nIn case you prefer cloning the Github repository and installing manually, please\nnote that `main` is the development branch, so `stable` is what you should be\nworking with.\n\n## Usage\n\n```python\n>>> from streaming_form_data import StreamingFormDataParser\n>>> from streaming_form_data.targets import FileTarget, NullTarget, GCSTarget, S3Target, ValueTarget\n>>>\n>>> headers = {"Content-Type": "multipart/form-data; boundary=boundary"}\n>>>\n>>> parser = StreamingFormDataParser(headers=headers)\n>>>\n>>> parser.register("name", ValueTarget())\n>>> parser.register("file-local", FileTarget("/path/to/file.txt"))\n>>> parser.register("file-s3", S3Target("s3://bucket/path/to/key"))\n>>> parser.register("file-gcs", GCSTarget("gs://bucket/path/to/key"))\n>>> parser.register("discard-me", NullTarget())\n>>>\n>>> for chunk in request.body:\n...     parser.data_received(chunk)\n...\n>>>\n```\n\n## Documentation\n\nUp-to-date documentation is available on [Read the Docs].\n\n## Development\n\nPlease make sure you have Python 3.9+, [poetry], and [just] installed.\n\nSince this package includes a C extension, please make sure you have a working C\ncompiler available. On Debian-based distros this usually means installing the\n`build-essentials` package.\n\n1. Git clone the repository:\n   `git clone https://github.com/siddhantgoel/streaming-form-data`\n\n2. Install the packages required for development:\n   `poetry install`\n\n4. That\'s basically it. You should now be able to run the test suite: `just test`\n\nNote that if you make any changes to Cython files (`.pyx, .pxd, .pxi`), you\'ll need to\nre-compile (`just compile`) and re-install `streaming_form_data` before you can test\nyour changes.\n\n[just]: https://just.systems\n[poetry]: https://python-poetry.org\n[Read the Docs]: https://streaming-form-data.readthedocs.io\n',
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
