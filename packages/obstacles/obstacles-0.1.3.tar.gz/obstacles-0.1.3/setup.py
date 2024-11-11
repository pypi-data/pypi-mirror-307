from setuptools import setup, find_packages

setup(
    name='obstacles',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # Dependencies
    ],
    entry_points={
        "console_scripts": [
            "obstacles-game = Obstacles:obstacles_game"
        ]
    }
)