import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

version = {}
with open("src/d4kms_info/__init__.py") as fp:
  exec(fp.read(), version)

setuptools.setup(
  name="d4kms",
  version=version['__package_version__'],
  author="D Iberson-Hurst",
  author_email="",
  description="A python package for building d4k microservcies",
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=['pydantic', 'requests', 'pyyaml', 'python-dotenv', 'neo4j', 'markdown', 'fastapi', 'Authlib', 'starlette', 'itsdangerous'],
  packages=setuptools.find_packages(where="src"),
  package_dir={"": "src"},
  tests_require=['pytest'],
  classifiers=[
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent"
  ],
)