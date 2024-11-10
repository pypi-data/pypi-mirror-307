from setuptools import setup

setup(
    name="health_sleep_analysis",
    version="0.1",
    py_modules=["health_sleep_analysis"],
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "scipy"
    ],
    author="Prithviraj K Tagadinamani",
    author_email="t.prithviraj@iitg.ac.in",
    description="A package for analyzing health and sleep data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/health_sleep_analysis",  # Replace with your actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)