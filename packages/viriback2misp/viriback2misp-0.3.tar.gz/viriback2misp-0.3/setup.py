from setuptools import find_packages, setup

def readme():
    with open('README.md', 'r') as f:
        README = f.read()
    return README

setup(
    name="viriback2misp",
    version="0.3",
    author="Camila Santiago",
    description="Upload Viriback C2 Track data to MISP events",
    url="https://github.com/santiag02/viriback2misp",
    packages=find_packages(exclude="media"),
    include_package_data=True,    
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=["pandas", "requests", "pymisp", "python-dateutil"],
    keywords= ['C2', 'command and control', 'C2 Tracker', 'command & control', 'feed c2', 'infostealer', 'bot', 'malware'],
    entry_points={
        "console_scripts": [ "viriback2misp = viriback2misp.main:main"],
    }
)