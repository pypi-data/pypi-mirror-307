from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'este paquete le permite formatear cedulas dominicanas'


# Configurando
setup(
       # el nombre debe coincidir con el nombre de la carpeta       
       #'modulomuysimple'
        name="cedula_do", 
        version=VERSION,
        author="Eduardo Tejada",
        author_email="davidtejadamoreta26@gmail.com",
        description=DESCRIPTION,
        
        packages=find_packages(),
        install_requires=['numpy', 'gc'], # añade cualquier paquete adicional que debe ser
        #instalado junto con tu paquete. Ej: 'caer'
        
        keywords=['python', 'cedulas', 'formateo'],
        
)