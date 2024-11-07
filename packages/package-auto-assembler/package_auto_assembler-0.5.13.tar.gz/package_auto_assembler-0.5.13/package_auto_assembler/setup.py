from setuptools import setup

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Package auto assembler

Package auto assembler is a tool that meant to streamline creation of single module packages.
Its purpose is to automate as many aspects of python package creation as possible,
to shorten a development cycle of reusable components, maintain certain standard of quality
for reusable code. It provides tool to simplify the process of package creatrion
to a point that it can be triggered automatically within ci/cd pipelines,
with minimal preparations and requirements for new modules.

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="package_auto_assembler",
    packages=["package_auto_assembler"],
    install_requires=['fastapi', 'uvicorn', 'numpy==1.26.0', 'attrs>=22.2.0', 'pyyaml', 'nbformat', 'stdlib-list', 'mkdocs-material==9.5.30', 'requests', 'streamlit>=1.39.0', 'packaging', 'click==8.1.7', 'nbconvert==7.16.4', 'pip_audit==2.7.3', 'mkdocs==1.6.0'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan",
    author_email="parachute.repo@gmail.com",
    description="A tool to automate package creation within ci based on just .py and optionally .ipynb file.",
    keywords="['python', 'packaging', 'aa-paa-tool']",
    license="mit",
    url="https://kiril-mordan.github.io/reusables/package_auto_assembler/",
    version="0.5.13",
    entry_points = {'console_scripts': ['paa = package_auto_assembler.cli:cli']},
    include_package_data = True,
    package_data = {'package_auto_assembler': ['mkdocs/**/*', 'artifacts/package_licenses.json', 'artifacts/package_mapping.json', '.paa.tracking/version_logs.csv', '.paa.tracking/release_notes.md', '.paa.tracking/lsts_package_versions.yml', '.paa.tracking/notebook.ipynb', '.paa.tracking/package_mapping.json', '.paa.tracking/package_licenses.json', '.paa.tracking/.drawio', 'tests/**/*', '.paa.tracking/.paa.config', '.paa.tracking/python_modules/package_auto_assembler.py', '.paa.tracking/python_modules/components/paa_deps/mkdocs_handler.py', '.paa.tracking/python_modules/components/paa_deps/local_dependencies_handler.py', '.paa.tracking/python_modules/components/paa_deps/import_mapping_handler.py', '.paa.tracking/python_modules/components/paa_deps/ppr_handler.py', '.paa.tracking/python_modules/components/paa_deps/streamlit_handler.py', '.paa.tracking/python_modules/components/paa_deps/cli_handler.py', '.paa.tracking/python_modules/components/paa_deps/artifacts_handler.py', '.paa.tracking/python_modules/components/paa_deps/metadata_handler.py', '.paa.tracking/python_modules/components/paa_deps/long_doc_handler.py', '.paa.tracking/python_modules/components/paa_deps/fastapi_handler.py', '.paa.tracking/python_modules/components/paa_deps/setup_dir_handler.py', '.paa.tracking/python_modules/components/paa_deps/release_notes_handler.py', '.paa.tracking/python_modules/components/paa_deps/drawio_handler.py', '.paa.tracking/python_modules/components/paa_deps/version_handler.py', '.paa.tracking/python_modules/components/paa_deps/requirements_handler.py', '.paa.tracking/python_modules/components/paa_deps/tests_handler.py', '.paa.tracking/python_modules/components/paa_deps/dependencies_analyzer.py', '.paa.tracking/.paa.version']} ,
    )
