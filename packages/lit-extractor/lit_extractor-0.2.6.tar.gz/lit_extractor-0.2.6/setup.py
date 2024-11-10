from setuptools import setup, find_packages

setup(
    name='lit-extractor',
    version='0.2.6',
    author="Munish chandra jha",
    author_email="mcj130101@gmail.com",
    description="A mini script to read a list of url and extract all the url's present in the webpage",
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",
    url="https://github.com/username/my_project",
    packages=find_packages(),
    py_modules=['extract'],
    install_requires=[
        'click',
        'fanficfare',
        'tqdm',
        'requests',
        'rich',
        'packaging'
    ],
    entry_points='''
      [console_scripts]
      lit-extract=extract:extract
      ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  # Include data files specified in MANIFEST.in
    keywords="extractor, lit-extractor",  # Keywords for search
    license="MIT",
)
