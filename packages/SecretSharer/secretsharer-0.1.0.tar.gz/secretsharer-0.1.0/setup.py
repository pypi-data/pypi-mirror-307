from setuptools import setup, find_packages

setup(
    name="SecretSharer",
    version="0.1.0",
    description="A Python package for generating canary sequences and computing exposure and perplexity metrics.",
    author="Vanthoff007",
    author_email="jiowork951@gmail.com",
    url="https://github.com/Vanthoff007/SecretSharer.git",
    packages=find_packages(),  # Automatically finds and includes all packages
    py_modules=[
        "Generate_Canaries",
        "Compute_Exposure",
        "Compute_Perplexity",
    ],  # Specify each file as a module
    install_requires=["numpy>=1.18.0", "torch>=1.7.0"],
    entry_points={
        "console_scripts": [
            "compute_exposure=Compute_Exposure:main",  # Replace 'main' with actual function to run exposure computation
            "compute_perplexity=Compute_Perplexity:main",  # Replace 'main' with actual function to run perplexity computation
            "generate_canaries=Generate_Canaries:main",  # Replace 'main' with function to run canary dataset generation
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    long_description="A package for generating canary datasets and computing exposure and perplexity metrics.",
    long_description_content_type="text/markdown",
)
