#!/usr/bin/env python3
"""Setup file for the ARL package."""

import os
from setuptools import find_packages, setup

# Get the version from palaestrai.__version__ without executing the module:
version = {}
with open(
    os.path.join(os.path.dirname(__file__), "src", "palaestrai", "version.py")
) as fp:
    exec(fp.read(), version)
VERSION = version["__version__"]

with open("VERSION", "w") as fp:
    fp.write(VERSION)

with open("README.rst") as freader:
    README = freader.read()

install_requirements = [
    # CLI
    "click~=8.1.7",
    "click-aliases~=1.0.4",
    "appdirs~=1.4.4",
    "tabulate~=0.9.0",
    # YAML, JSON
    "yamale~=4.0.4",
    "ruamel.yaml~=0.17.40",
    "simplejson~=3.19.2",
    "jsonpickle~=3.0.2",
    # Process and IPC handling
    "aiomultiprocess~=0.9.0",
    "setproctitle~=1.3.3",
    "pyzmq~=25.1.2",
    "nest_asyncio~=1.5.8",
    # Data handling and storage
    "numpy~=1.23.5",
    "pandas~=2.1.4",
    "dask~=2023.12.1",
    "gymnasium",
    "psycopg2-binary~=2.9.9",
    "SQLalchemy~=1.4.50",
    "sqlalchemy-utils~=0.41.1",
    # Documentation
    "pandoc",
    # Scheduler
    "GPUtil~=1.4.0",
    "psutil~=5.9.0",
    "docker~=7.0.0",
]

influx_requirements = [
    "elasticsearch>=7.0.0",
    "influxdb-client[ciso]",
]

development_requirements = [
    "Cython~=3.0.5",
    # Tests
    "tox~=4.11.4",
    "robotframework~=6.1.1",
    "robotframework-stacktrace~=0.4.1",
    "pytest~=7.4.3",
    "pytest-asyncio~=0.23.2",
    "pytest-cov~=4.1.0",
    "coverage~=7.3.2",
    "lxml~=4.9.3",
    "mock~=5.1.0",
    "alchemy-mock~=0.4.3",
    # Linting
    "black~=24.1.0",
    # Type checking
    "mypy~=1.7.1",
    "types-click~=7.1.8",
    "types-setuptools",
    # Documentation
    "sphinx",
    "nbsphinx~=0.9.3",
    "furo~=2023.9.10",
    "ipython~=8.17.2",
    "ipykernel~=6.29.2",
    "plotly",
    "eralchemy2",
]

fullstack_requirements = [
    "palaestrai-arsenai~=3.5.0",
    "palaestrai-agents~=3.5.0",
    "palaestrai-environments~=3.5.0",
    "palaestrai-mosaik~=3.5.0",
    "midas-mosaik==1.2.2",
    "midas-util==1.1.2",
    "midas-palaestrai~=3.5.0",
    "pysimmods",
]

fullstack_development_requirements = [
    "palaestrai-arsenai@git+https://gitlab.com/arl2/arsenai.git@development#egg=palaestrai-arsenai",
    "palaestrai-agents@git+https://gitlab.com/arl2/harl.git@development#egg=harl",
    "palaestrai-environments@git+https://gitlab.com/arl2/palaestrai-environments.git@development#egg=palaestrai-environments",
    "palaestrai-mosaik@git+https://gitlab.com/arl2/palaestrai-mosaik.git@main#egg=palaestrai-mosaik",
    "midas-mosaik@git+https://gitlab.com/midas-mosaik/midas.git@development#egg=midas_mosaik",
    "midas-util@git+https://gitlab.com/midas-mosaik/midas-util.git@main#egg=midas_util",
    "pysimmods@git+https://gitlab.com/midas-mosaik/pysimmods.git@development#egg=pysimmods",
    "midas-palaestrai@git+https://gitlab.com/midas-mosaik/midas-palaestrai.git@main#egg=midas_palaestrai",
    "midas-powergrid@git+https://gitlab.com/midas-mosaik/midas-powergrid.git@main#egg=midas_powergrid",
]

full_dev = development_requirements + fullstack_development_requirements

extras = {
    "dev": development_requirements,
    "full": fullstack_requirements,
    "influx": influx_requirements,
}

# This line gets removed for PyPi upload
# extras.update({"full-dev": full_dev})

setup(
    name="palaestrai",
    version=VERSION,
    description="A Training Ground for Autonomous Agents",
    long_description=README,
    author="The ARL Developers",
    author_email="eric.veith@offis.de",
    python_requires=">=3.10",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPLv2",
    url="http://palaestr.ai/",
    entry_points={
        "console_scripts": [
            "palaestrai = palaestrai.cli.manager:cli",
            "palaestrai-scheduler = palaestrai.cli.scheduler:scheduler_setup",
            "arl-apply-migrations = palaestrai.store.migrations.apply:main",
        ]
    },
    package_data={"palaestrai": ["run_schema.yaml", "py.typed"]},
    data_files=[
        ("etc/bash_completion.d/", ["palaestrai_completion.sh"]),
        ("etc/zsh_completion.d/", ["palaestrai_completion.zsh"]),
        ("etc/fish_completion.d/", ["palaestrai_completion.fish"]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
