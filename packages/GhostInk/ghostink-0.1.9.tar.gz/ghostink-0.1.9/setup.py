from setuptools import setup, find_packages

setup(
    name="GhostInk",
    version="0.1.9",
    packages=find_packages(),
    author="Yeeloman",
    author_email="yami.onlyme@gmail.com",
    description="A task management tool for developers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yeeloman/GhostInk",
    install_requires=["colorama"],
    keywords=[
        "task management",
        "debugging",
        "development tools",
        "logging",
        "task tracker",
        "Python",
        "console output",
        "debugging tools",
        "task organizer",
        "development",
        "productivity",
        "software development",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
