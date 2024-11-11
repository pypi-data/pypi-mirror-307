import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'  # Cambia la versión conforme actualices la librería
PACKAGE_NAME = 'StadisticsML'  # Asegúrate de que coincida con el nombre de la carpeta del proyecto
AUTHOR = 'Jorge Eduardo Londoño Arango'
AUTHOR_EMAIL = 'joelondonoar@unal.edu.co'
URL = 'https://github.com/Guacen/StadisticsML.git'  # Modifica con el enlace correcto de tu repositorio

LICENSE = 'MIT'
DESCRIPTION = 'Librería para obtener valores estadísticos para pruebas de distribución de signos, determinación de outliers y pruebas Durbin-Watson'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

# Dependencias necesarias para la librería
INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'scikit-learn'
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
    include_package_data=True,
)
