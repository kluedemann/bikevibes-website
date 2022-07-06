from setuptools import find_packages, setup

setup(
    name='bikemonitor',
    version='1.1.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)