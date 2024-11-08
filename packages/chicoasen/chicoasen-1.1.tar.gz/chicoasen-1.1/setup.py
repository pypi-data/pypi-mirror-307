import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.1'
PACKAGE_NAME = 'Chicoasen' 
AUTHOR = 'Equipo SS' 
AUTHOR_EMAIL = 'mhernandezg2204@alumno.ipn.mx' 
URL = 'https://github.com/CIDETECSI/chicoasen' 

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para cargar archivos csv & json y conectar a una base de datos' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'pymupdf'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True)