from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='projeto_fiap',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Marina N M',
    author_email='mah.novelli@hotmail.com',
    url='https://github.com/m-novelli/projeto_fiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
