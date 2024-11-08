from setuptools import setup, find_packages

setup(
    name="kpi-formula-jun",
    version="0.1.1",
    author="Jun",
    author_email="leoren1314@gmail.com",
    description="A KPI calculation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kpi-formula",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/kpi-formula/issues",
        "Source": "https://github.com/yourusername/kpi-formula",
    },
)
