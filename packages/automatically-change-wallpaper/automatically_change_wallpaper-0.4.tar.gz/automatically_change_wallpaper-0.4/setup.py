from setuptools import setup, find_packages

setup(
    name='automatically_change_wallpaper',
    version='0.4', 
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts": [
            "acw = automatically_change_wallpaper:main",
        ]
    }
)
