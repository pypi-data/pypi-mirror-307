from setuptools import setup, find_packages

with open('README.md', 'r') as txt:
    description = txt.read()

setup(
    name='automatically_change_wallpaper',
    version='1.3', 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[

    ],
    entry_points={
        "console_scripts": [
            "acw = automatically_change_wallpaper:main",
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
