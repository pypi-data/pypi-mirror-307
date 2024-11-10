from setuptools import setup, find_packages

setup(
    name='terminal-menu-interface',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        *open('requirements.txt').read().split("\n")
    ],
    description='Esse pacote tem como função, democratizar a criação de menu em seus fluxos de código',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Augusto-cmk/Menu',  # URL do repositório
    author='Augusto-cmk',
    author_email='pedroaugustoms14@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
)
