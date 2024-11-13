from setuptools import setup, find_packages

setup(
    name="wabtec-hackathon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if not line.startswith("#")
    ],
    author="Team VIT Bhopal",
    author_email="your.email@example.com",
    description="Wabtec Hackathon Project",
    python_requires=">=3.8",
)