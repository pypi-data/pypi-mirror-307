# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bedspec', 'bedspec.overlap', 'cgranges', 'cgranges.test']

package_data = \
{'': ['*'],
 'cgranges': ['cpp/*', 'python/*'],
 'cgranges.test': ['3rd-party/*',
                   '3rd-party/AIList/*',
                   '3rd-party/AITree/*',
                   '3rd-party/NCList/*']}

install_requires = \
['typeline>=0.3,<0.4', 'typing-extensions>=4.12,<5.0']

setup_kwargs = {
    'name': 'bedspec',
    'version': '0.3.0',
    'description': 'An HTS-specs compliant BED toolkit.',
    'long_description': '# bedspec\n\n[![PyPi Release](https://badge.fury.io/py/bedspec.svg)](https://badge.fury.io/py/bedspec)\n[![CI](https://github.com/clintval/bedspec/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/clintval/bedspec/actions/workflows/tests.yml?query=branch%3Amain)\n[![Python Versions](https://img.shields.io/badge/python-3.10_|_3.11_|_3.12-blue)](https://github.com/clintval/typeline)\n[![basedpyright](https://img.shields.io/badge/basedpyright-checked-42b983)](https://docs.basedpyright.com/latest/)\n[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)\n[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/)\n\nAn HTS-specs compliant BED toolkit.\n\n## Installation\n\nThe package can be installed with `pip`:\n\n```console\npip install bedspec\n```\n\n## Quickstart\n\n### Building a BED Feature\n\n```pycon\n>>> from bedspec import Bed3\n>>> \n>>> bed = Bed3("chr1", start=2, end=8)\n\n```\n\n### Writing\n\n```pycon\n>>> from bedspec import BedWriter\n>>> from tempfile import NamedTemporaryFile\n>>> \n>>> temp_file = NamedTemporaryFile(mode="w+t", suffix=".txt")\n>>>\n>>> with BedWriter.from_path(temp_file.name, Bed3) as writer:\n...     writer.write(bed)\n\n```\n\n### Reading\n\n```pycon\n>>> from bedspec import BedReader\n>>> \n>>> with BedReader.from_path(temp_file.name, Bed3) as reader:\n...     for bed in reader:\n...         print(bed)\nBed3(refname=\'chr1\', start=2, end=8)\n\n```\n\n### BED Types\n\nThis package provides builtin classes for the following BED formats:\n\n```pycon\n>>> from bedspec import Bed2\n>>> from bedspec import Bed3\n>>> from bedspec import Bed4\n>>> from bedspec import Bed5\n>>> from bedspec import Bed6\n>>> from bedspec import Bed12\n>>> from bedspec import BedGraph\n>>> from bedspec import BedPE\n\n```\n\n### Overlap Detection\n\nUse a fast overlap detector for any collection of interval types, including third-party:\n\n```pycon\n>>> from bedspec import Bed3, Bed4\n>>> from bedspec.overlap import OverlapDetector\n>>>\n>>> bed1 = Bed3("chr1", start=1, end=4)\n>>> bed2 = Bed3("chr1", start=5, end=9)\n>>> \n>>> detector = OverlapDetector[Bed3]([bed1, bed2])\n>>> \n>>> my_feature = Bed4("chr1", start=2, end=3, name="hi-mom")\n>>> detector.overlaps(my_feature)\nTrue\n\n```\n\nThe overlap detector supports the following operations:\n\n- `overlapping`: return all overlapping features\n- `overlaps`: test if any overlapping features exist\n- `enclosed_by`: return those enclosed by the input feature\n- `enclosing`: return those enclosing the input feature\n\n### Custom BED Types\n\nTo create a custom BED record, inherit from the relevant BED-type (`PointBed`, `SimpleBed`, `PairBed`).\n\nFor example, to create a custom BED3+1 class:\n\n```pycon\n>>> from dataclasses import dataclass\n>>> \n>>> from bedspec import SimpleBed\n>>> \n>>> @dataclass(eq=True)\n... class Bed3Plus1(SimpleBed):\n...     refname: str\n...     start: int\n...     end: int\n...     my_custom_field: float | None\n\n```\n\n## Development and Testing\n\nSee the [contributing guide](./CONTRIBUTING.md) for more information.\n',
    'author': 'Clint Valentine',
    'author_email': 'valentine.clint@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/clintval/bedspec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
