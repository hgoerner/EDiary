from setuptools import setup, find_packages

setup(
    name="pydiary",
    version="1.0.1",
    author="Hendrik Görner",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "pytest",
        "folium",
        "pandas",
        "numpy",
        "matplotlib",
        "scipy",
        "scikit-learn",
    ],
)
