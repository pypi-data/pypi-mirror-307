from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name='gemnify_sdk',
    version='0.0.20',
    author='fiorea',
    # author_email='your.email@example.com',
    description='gemnify sdk',
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["example_scripts", "*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.9',
    include_package_data=True,
    # package_data={
    #     '': ['*.json', '*.md'],
    # }
)
