#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("version.txt") as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

# with open("test_requirements.txt") as f_tests:
#    required_for_tests = f_tests.read().splitlines()


def get_file_content(file_name):
    with open(file_name) as f:
        return f.read()


setup(
    name="torque_bulk_deployer",
    version=version_from_file,
    description="Torque bulk deployer - a Quali tool for deploying Environments on Quali Torque in Bulk",
    long_description=get_file_content("README.md"),
    long_description_content_type="text/markdown",
    author="QualiSystems",
    author_email="info@qualisystems.com",
    url="https://github.com/QualiSystemsLab/Torque-Bulk-Deployer",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#   package_data={"torque_bulk_deployer": ["data/*.yml", "data/*.json"]},
#   include_package_data=True,
#   test_suite="tests",
    entry_points={"console_scripts": ["torque_bulk_deployer = torque_bulk_deployer.bulk_deployer"]},
    install_requires=required,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords="torque_bulk_deployer torque sandbox cloud virtualization vcenter cmp quali command-line cli",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9.9",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
)

