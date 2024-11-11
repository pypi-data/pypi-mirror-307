import setuptools

setuptools.setup(
    name="autoluv",
    version="0.1",
    author="beanliu",
    description="tool for autoluv",
    url="https://github.com/project/autoluv",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'autoluv=autoluv:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
)