from setuptools import setup

setup(
    name="sleep_data_analysis",
    version="0.3",
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
    author_email="prithvirajtagadinamani@gmail.com",
    description="A package for analyzing health and sleep data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prithviraj-kt/sleep_data_analysis.git",  # Replace with your actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'sleep-data-analysis = sleep_data_analysis.project:main',
        ],
    },
)