from setuptools import setup, find_packages

setup(
    name="automatically_change_wallpaper",
    version="1.0",
    packages=find_packages(where="automatically_change_wallpaper"),
    package_dir={"": "automatically_change_wallpaper"},
    entry_points={
        "console-scripts": [
            "acw=automatically_change_wallpaper.__main__:main"
        ]
    },
)

