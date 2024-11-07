from setuptools import setup, find_packages

setup(
    name="Django_generate_serializers_views",
    version="0.1.0",
    description="This package helps in generate the views.py and serializers.py with the auto-generated code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ramesh patil",
    author_email="rrp24999@gmail.com",
    url="",
    packages=find_packages(),
    install_requires=[],  # add dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
