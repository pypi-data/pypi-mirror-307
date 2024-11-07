from setuptools import setup, find_packages

setup(
    name="electrox",
    version="1.1.24",  # Updated version format
    packages=find_packages(),
    install_requires=[
        'pygame',  # Dependency on pygame for graphics and game functionality
    ],
    entry_points={
        'console_scripts': [
            'electrox = electrox.main:main',  # Ensure main.py exists with a main() function
        ],
    },
    author="Hussain Luai",
    author_email="hxolotl15@gmail.com",
    description="Electrox is a Python framework for 2D game development with Gen Z and Gen Alpha vibes for some reason... nvm enjoy electrox.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
