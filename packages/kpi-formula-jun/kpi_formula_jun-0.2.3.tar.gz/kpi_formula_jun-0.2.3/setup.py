from setuptools import setup, find_packages

setup(
    name="kpi-formula-jun",
    version="0.2.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'statistics',
    ],
    author="Jun Ren",
    author_email="leoren1314@gmail.com",
    description="A package for KPI calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kpi-formula",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
