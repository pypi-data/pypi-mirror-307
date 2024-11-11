from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='curso-fiap',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Matheus Carrillo',
    author_email='matheus_carrillo@hotmail.com',
    url='https://github.com/matheuscarrillo/cursofiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
