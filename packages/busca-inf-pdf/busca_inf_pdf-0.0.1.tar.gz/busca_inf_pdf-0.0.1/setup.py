from setuptools import setup, find_packages

setup(
    name='busca_inf_pdf',                      
    version='0.0.1',
    description='Pacote desenvolvido para buscar informações em arquivos pdf',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rodrigo Schilling',
    author_email='rodrigo.schilling98@gmail.com',
    url='https://github.com/RoSchilling/busca_inf_pdf',
    packages=find_packages(),           
    install_requires=[
        'pandas',
        'numpy',
        'camelot.py [cv]'
    ],
)