
import psycopg2
import pandas as pd
from IPython.display import display
import json

class PostgresDB:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def connect(self, dbname=None):
        """Conectar a PostgreSQL con la opción de especificar otra base de datos."""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=dbname if dbname else self.dbname,
            user=self.user,
            password=self.password
        )
    
    def obtener_bases_de_datos(self):
        """Obtiene las bases de datos disponibles."""
        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = """
            SELECT datname AS "Nombre de la Base de Datos", 
                   pg_catalog.pg_get_userbyid(datdba) AS "Propietario"
            FROM pg_database
            WHERE datistemplate = false;
            """
            cursor.execute(query)
            databases = cursor.fetchall()
            return pd.DataFrame(databases, columns=["Nombre de la Base de Datos", "Propietario"])
        
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            return None
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
    
    def ver_tablas_bd(self, dbname):
        """Muestra las tablas de una base de datos específica."""
        try:
            connection = self.connect(dbname=dbname)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            tablas = cursor.fetchall()
            return pd.DataFrame(tablas, columns=["Nombre de la Tabla"])
        
        except Exception as e:
            print(f"Error al conectar o consultar las tablas: {e}")
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def atributos_tabla(self, dbname, tabla):
        """Obtiene los atributos de una tabla específica."""
        try:
            connection = self.connect(dbname=dbname)
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = '{tabla}';
            """)
            atributos = cursor.fetchall()
            return pd.DataFrame(atributos, columns=["Nombre de Columna", "Tipo de Dato", "Es Nulo"])
        
        except Exception as e:
            print(f"Error al conectar o consultar los atributos: {e}")
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def leer_tabla(self, dbname, tabla):
        """Lee las inserciones de una tabla específica."""
        try:
            connection = self.connect(dbname=dbname)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {tabla};")
            datos = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(datos, columns=columnas)
        
        except Exception as e:
            print(f"Error al conectar o leer la tabla '{tabla}': {e}")
            return None
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def dividir_dataframe_en_chunks(self, df, chunk_size):
        """Divide un DataFrame en 'chunks' del tamaño especificado."""
        for i in range(0, len(df), chunk_size):
            yield df.iloc[i:i + chunk_size]