
from setuptools import setup, find_packages

setup(
    name="robust_vmaf",
    version="0.1.0-dev1",
    packages=find_packages(),
    package_data={
        'robust_vmaf': ['models/*.pkl'],
    },
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'scikit_learn',
        'scipy',
        'torch',
        'tqdm'
    ],
    author="Mg_det",
    author_email="hrebtovmaksim1@gmail.com",
    description="robust modification of VMAF",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hrebtovmaksim1/robust_vmaf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
