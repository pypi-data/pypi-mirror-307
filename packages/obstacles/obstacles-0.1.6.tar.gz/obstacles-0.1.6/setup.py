from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='obstacles',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        # Dependencies
    ],
    entry_points={
        "console_scripts": [
            "obstacles-game = Obstacles:obstacles_game"
        ]
    },
    long_description=description,
    long_description_content_type='text/markdown',
)