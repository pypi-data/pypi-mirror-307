import setuptools

setuptools.setup(
    name="autoskinning",
    version="0.1",
    author="beanliu",
    description="tool for autoskinning",
    url="https://github.com/project/autoskinning",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'autoskinning=autoskinning:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
)