from setuptools import setup, find_packages

setup(
    name="oss_stats",
    version="0.1.0",
    description="A Python CLI tool to fetch GitHub stats from acmcsufoss",
    url="https://github.com/acmcsufoss/oss-stats",
    packages=find_packages(),
    install_requires=["click", "PyGithub", "python-dotenv", "rich"],
    entry_points={
        "console_scripts": ["oss_stats=oss_stats.cli:cli"],
    },
)
