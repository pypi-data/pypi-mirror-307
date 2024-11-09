import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yae",
    version="0.0.1",
    author="malanore",
    author_email="malanore.z@gmail.com",
    description="DevOps Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malanore-z/yae",
    project_urls={
        "Bug Tracker": "https://github.com/malanore-z/yae/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include="dot.*"),
    package_data={'dot': ['resources/*']},
    python_requires=">=3.6",
    install_requires=[
        "psutil",
        "PyYAML",
        "numpy",
    ],
    extras_requires={
    }

)