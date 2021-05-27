import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="minefob",
	version="1.0.1b",
	author="Caleb North",
	author_email="fivesixfive.contact@gmail.com",
	description="A package that provides full control over any Minehut server",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/thefivesixfive/Minefob",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6'
)
