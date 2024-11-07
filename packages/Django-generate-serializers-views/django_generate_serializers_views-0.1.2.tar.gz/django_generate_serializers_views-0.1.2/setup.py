from setuptools import setup, find_packages

setup(
    name="Django_generate_serializers_views",
    version="0.1.2",  # Update the version if re-uploading
    package_dir={"": "src"},  # Specify that packages are in 'src'
    packages=find_packages(where="src"),  # Look for packages inside 'src'
    include_package_data=True,
    description="This package helps in generate the views.py and serializers.py with the auto-generated code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ramesh patil",
    author_email="rrp24999@gmail.com",
    url="",
    install_requires=[],  # add dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
