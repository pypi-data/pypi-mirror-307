# Chicoasen

Chicoasen es una librería Python para el manejo de archivos y bases de datos PostgreSQL. Proporciona utilidades para análisis de datos, manejo de archivos y operaciones de base de datos.

## Instalación

```bash
pip install chicoasen
```

## Uso

```python
from chicoasen import archivos, PostgresDB

# Ejemplo de manejo de archivos
config = archivos.config()
path = "ruta/a/tu/archivo.csv"
archivos.validar_carga_muestra(path, config)

# Ejemplo de base de datos
db = PostgresDB(
    host='localhost',
    port=5432,
    dbname='tu_base_datos',
    user='tu_usuario',
    password='tu_contraseña'
)
bases_datos = db.obtener_bases_de_datos()
print(bases_datos)
```