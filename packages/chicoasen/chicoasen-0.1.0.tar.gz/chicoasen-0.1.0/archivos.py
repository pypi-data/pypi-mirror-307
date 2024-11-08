import json
import os
import pandas as pd

class archivos:
    @staticmethod
    def config():
        with open('chicoasen/conf/fileaccess1.json', 'r') as fileaccess1:
            conf = json.load(fileaccess1)[0]
        return conf
    
    @staticmethod
    def obtener_path():
        path = input("Ingrese la dirección del archivo: ")
        return path
    
    @staticmethod
    def obtener_extension(file_path):
        file_extension = file_path.split('.')[-1]
        return file_extension
    
    @staticmethod
    def validar_formato(file_extension):
        config = archivos.config()
        if file_extension not in config['validFormats']:
            print(f"Formato {file_extension} no es válido.") 
            print(f"Los formatos permitidos son: {config['validFormats']} \n")
            return

    @staticmethod
    def mostrar_columnas(df):
        if isinstance(df, pd.DataFrame):
            print("\n=== Nombres de las Columnas ===")
            for i, columna in enumerate(df.columns, 1):
                print(f"{i}. {columna}")
        else:
            print("El objeto no es un DataFrame válido")

    @staticmethod
    def mostrar_atributos_completos(df):
        if isinstance(df, pd.DataFrame):
            print("\n=== Atributos del DataFrame ===")
            print(f"Número de filas: {df.shape[0]}")
            print(f"Número de columnas: {df.shape[1]}")
            print("\n=== Primeras 5 filas del DataFrame ===")
            print(df.head())
            print("\nTipos de datos:")
            for columna, tipo in df.dtypes.items():
                print(f"{columna}: {tipo}")
            print("\nEstadísticas básicas:")
            print(df.describe().round(2))
            print("\nValores nulos por columna:")
            for columna, nulos in df.isnull().sum().items():
                print(f"{columna}: {nulos}")
        else:
            print("El objeto no es un DataFrame válido")

    @staticmethod
    def carga_json_chiko(file_path):
        df = pd.read_json(file_path)
        archivos.mostrar_columnas(df)
        archivos.mostrar_atributos_completos(df)
        return df

    @staticmethod
    def carga_csv_chiko(file_path):
        df = pd.read_csv(file_path)
        archivos.mostrar_columnas(df)
        archivos.mostrar_atributos_completos(df)
        return df

    @staticmethod
    def procesar_chunk(chunk, chunk_actual, total_filas, filas_procesadas):
        filas_chunk = len(chunk)
        filas_restantes = total_filas - (filas_procesadas + filas_chunk)
        
        nulos_chunk = chunk.isnull().sum().sum()
        
        print("\n" + "="*50)
        if nulos_chunk > 0:
            print(f"En este chunk hay {nulos_chunk} valores nulos")
        else:
            print("En este chunk no hay valores nulos")
        print("="*50)
        print(f"Procesando Chunk {chunk_actual}")
        print(f"Filas en este chunk: {filas_chunk}")
        print(f"Filas procesadas hasta ahora: {filas_procesadas}")
        print(f"Filas restantes: {filas_restantes}")
        print(f"Progreso: {((filas_procesadas + filas_chunk) / total_filas * 100):.2f}%")
        print("="*50)
        print("\nMuestra de datos en este chunk:")
        print(chunk.head())
        print("="*50)
        
        return filas_chunk

    @staticmethod
    def validar_carga_muestra(file_path, config):
        file_extension = archivos.obtener_extension(file_path)
        archivos.validar_formato(file_extension)
        
        if not os.path.exists(file_path):
            print(f"Archivo {file_path} no encontrado.")
            return

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"Tamaño del archivo: {file_size_mb:.2f} MB")

        file_config = next(f for f in config['files'] if f['type'] == file_extension)

        if file_size_mb > file_config['max_size_mb']:
            if file_extension == 'csv':
                total_filas = sum(1 for _ in open(file_path)) - 1
                filas_procesadas = 0
                chunk_counter = 0
                df_acumulado = pd.DataFrame()
                
                print(f"\nProcesando archivo en chunks de {file_config['chunk_size']} filas")
                print(f"Total de filas a procesar: {total_filas}")
                
                for chunk in pd.read_csv(file_path, chunksize=file_config['chunk_size']):
                    chunk_counter += 1
                    filas_chunk = archivos.procesar_chunk(
                        chunk=chunk,
                        chunk_actual=chunk_counter,
                        total_filas=total_filas,
                        filas_procesadas=filas_procesadas
                    )
                    df_acumulado = pd.concat([df_acumulado, chunk])
                    filas_procesadas += filas_chunk
                
                print("\n=== Atributos Completos después de procesar todos los chunks ===")
                archivos.mostrar_atributos_completos(df_acumulado)
                    
            elif file_extension == 'json':
                with open(file_path, 'r') as fileaccess1:
                    data = json.load(fileaccess1)
                    df = pd.DataFrame(data)
                    total_filas = len(df)
                    archivos.procesar_chunk(
                        chunk=df,
                        chunk_actual=1,
                        total_filas=total_filas,
                        filas_procesadas=0
                    )
                    archivos.mostrar_atributos_completos(df)
        else:
            print(f"El archivo {file_path} se cargará de una sola vez.")
            if file_extension == 'csv':
                df = archivos.carga_csv_chiko(file_path)
                print(f"Archivo {file_path} cargado: {len(df)} filas")
            elif file_extension == 'json':
                df = archivos.carga_json_chiko(file_path)
                print(f"Archivo {file_path} cargado: {len(df)} filas")
