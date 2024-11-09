from setuptools import find_packages, setup

setup(
    name='ct-redis-cache-lib',
    packages=find_packages(),
    version='0.0.1',  # Increment version
    description='A specialized library developed by Credenti for efficient Redis caching in Flask applications.',
    author='credenti',
    install_requires=["redis==5.2.0", "Flask>=3.0.3"],
)
