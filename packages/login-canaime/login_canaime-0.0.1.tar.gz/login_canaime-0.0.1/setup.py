from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="login_canaime",
    version="0.0.1",
    license='MIT License',
    author='Anderson Assunção',
    long_description=readme,
    long_description_content_type="text/markdown",
    description="Pacote para login no Sistema Canaimé",
    author_email='andersongomesrr@hotmail.com',
    packages=['login_canaime'],
    install_requires=[
        "playwright",
        "pandas",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
