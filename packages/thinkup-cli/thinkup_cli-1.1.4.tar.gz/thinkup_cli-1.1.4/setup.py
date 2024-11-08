from setuptools import setup, find_packages

setup(
    name="thinkup-cli",
    version="1.1.4",
    packages=find_packages(),
    install_requires=[
        "questionary",
        "requests",
        "prompt_toolkit",
        "oauth2client"
    ],
    entry_points={
        'console_scripts': [
            'tkup.cli=thinkup_cli.main:main_function',
        ],
    },
)
