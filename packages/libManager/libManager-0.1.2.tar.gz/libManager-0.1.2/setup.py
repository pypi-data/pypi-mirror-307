from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    description = file.read()

setup(
    name='libManager',
    version='0.1.2',
    description='A class providing more control over libraries using pip',
    author='Kirill Sedykh',
    author_email='kirill-10c@mail.ru',
    license='MIT',
    packages=find_packages(),
    long_description=description,
    long_description_content_type="text/markdown"
)