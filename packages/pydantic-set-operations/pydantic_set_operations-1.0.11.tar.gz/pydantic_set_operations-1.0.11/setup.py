from setuptools import setup, find_packages

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name="pydantic_set_operations",
	version="1.0.11",
	description="An enhanced version of Pydantic's BaseModel, allowing for advanced model "
	            "manipulations. (Inspired in TypeScript)",
	package_dir={"": "src"},
	packages=find_packages(where="src"),
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/P1etrodev/pydantic-set-operations",
	author="P1etrodev",
	author_email="undefinedpietro@gmail.com",
	license="MIT",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.10",
		"Operating System :: OS Independent"
	],
	install_requires=[
		"pydantic"
	],
	extras_require={
		"dev": ["twine"]
	},
	python_requires=">=3.10",
)