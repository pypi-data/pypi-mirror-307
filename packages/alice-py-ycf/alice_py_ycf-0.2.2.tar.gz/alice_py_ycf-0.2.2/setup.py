from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="alice-py-ycf",
    version="0.2.2",
    author="Aleks_Nevs",
    description="Module for easy writing of Yandex Alice skills.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author_email="WebAlek@yandex.ru",
    url="https://github.com/Aleksandr-Nevs/alice-py-ycf",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    install_requires=[],
    keywords="Alice dialog, Python, Yandex",
    python_requires='>=3.8',
)