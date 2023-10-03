import requests
from loguru import logger
import os
import zipfile
import pandas as pd

# TODO: chequear los parametros de la solicitud para el archivo

class DownloadPostalCode():  
    # Denicion de rutas y nombre de archivo
    filename = 'CPdescargaxls.zip'
    zipfile_path = f"{os.getcwd()}/{filename}"
    csv_file_path = f"{os.getcwd()}/locations/mexico"

    def download(self): 
        #Url sitio de codigos postales mexico
        url = "https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx"

        #Parametros de solicitud
        payload = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUINzcwOTQyOTgPZBYCAgEPZBYCAgEPZBYGAgMPDxYCHgRUZXh0BT3Dmmx0aW1hIEFjdHVhbGl6YWNpw7NuIGRlIEluZm9ybWFjacOzbjogU2VwdGllbWJyZSAyOSBkZSAyMDIzZGQCBw8QDxYGHg1EYXRhVGV4dEZpZWxkBQNFZG8eDkRhdGFWYWx1ZUZpZWxkBQVJZEVkbx4LXyFEYXRhQm91bmRnZBAVISMtLS0tLS0tLS0tIFQgIG8gIGQgIG8gIHMgLS0tLS0tLS0tLQ5BZ3Vhc2NhbGllbnRlcw9CYWphIENhbGlmb3JuaWETQmFqYSBDYWxpZm9ybmlhIFN1cghDYW1wZWNoZRRDb2FodWlsYSBkZSBaYXJhZ296YQZDb2xpbWEHQ2hpYXBhcwlDaGlodWFodWERQ2l1ZGFkIGRlIE3DqXhpY28HRHVyYW5nbwpHdWFuYWp1YXRvCEd1ZXJyZXJvB0hpZGFsZ28HSmFsaXNjbwdNw6l4aWNvFE1pY2hvYWPDoW4gZGUgT2NhbXBvB01vcmVsb3MHTmF5YXJpdAtOdWV2byBMZcOzbgZPYXhhY2EGUHVlYmxhClF1ZXLDqXRhcm8MUXVpbnRhbmEgUm9vEFNhbiBMdWlzIFBvdG9zw60HU2luYWxvYQZTb25vcmEHVGFiYXNjbwpUYW1hdWxpcGFzCFRsYXhjYWxhH1ZlcmFjcnV6IGRlIElnbmFjaW8gZGUgbGEgTGxhdmUIWXVjYXTDoW4JWmFjYXRlY2FzFSECMDACMDECMDICMDMCMDQCMDUCMDYCMDcCMDgCMDkCMTACMTECMTICMTMCMTQCMTUCMTYCMTcCMTgCMTkCMjACMjECMjICMjMCMjQCMjUCMjYCMjcCMjgCMjkCMzACMzECMzIUKwMhZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCHQ88KwALAGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFC2J0bkRlc2NhcmdhpvxGcmcI9N43lP0rKq8PnxyXNEw%3D&__VIEWSTATEGENERATOR=BE1A6D2E&__EVENTVALIDATION=%2FwEWKALinN2%2BBQLG%2FOLvBgLWk4iCCgLWk4SCCgLWk4CCCgLWk7yCCgLWk7iCCgLWk7SCCgLWk7CCCgLWk6yCCgLWk%2BiBCgLWk%2BSBCgLJk4iCCgLJk4SCCgLJk4CCCgLJk7yCCgLJk7iCCgLJk7SCCgLJk7CCCgLJk6yCCgLJk%2BiBCgLJk%2BSBCgLIk4iCCgLIk4SCCgLIk4CCCgLIk7yCCgLIk7iCCgLIk7SCCgLIk7CCCgLIk6yCCgLIk%2BiBCgLIk%2BSBCgLLk4iCCgLLk4SCCgLLk4CCCgLL%2BuTWBALa4Za4AgK%2BqOyRAQLI56b6CwL1%2FKjtBS7H6z3%2Fz30UyylIlKEozvBNXCk6&cboEdo=00&rblTipo=xls&btnDescarga.x=62&btnDescarga.y=12'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            # Si el estado de conexion es 200 es porque se ejecuto correctamente el proceso
            if response.status_code == 200:
                with open(self.filename, 'wb') as archivo_zip:
                    archivo_zip.write(response.content)
                logger.info(f'Archivo ZIP "{self.filename}" se ha descargado exitosamente')
        except:
            logger.exception('Error en la solicitud POST.')
    
    def extract_file(self): 
        self.download()
        try:
            # Extraer zip descargado
            if os.path.exists(self.zipfile_path):
                with zipfile.ZipFile(self.zipfile_path, 'r') as zip_ref:
                    # Nombre del archivo XLS que deseas extraer
                    zip_ref.extractall(os.getcwd())
                    logger.info('Se extrajo el archivo ZIP correctamente')
        except:
            logger.error(f'No se puedo extraer el archivo ZIP')

    def check_xls(self):
        self.extract_file()
        extension = '.xls'
        try:
            # Iterar a través de los archivos en el directorio actual
            for root, _, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith(extension):
                        file_xls = os.path.join(root, file)
                        logger.info(f'Archivo XLS encontrado: {file_xls}')
                        return file_xls  # Retorna el primer archivo XLS encontrado
        except:
            logger.exception('No se encuentra el archivo xls')

    def tocsv(self):
        file_xls = self.check_xls()
        try: 
            # Cargar el archivo XLS en un objeto ExcelFile de pandas
            xls = pd.ExcelFile(file_xls)
            # Iterar a través de cada hoja en el archivo XLS
            for sheet_name in xls.sheet_names:
                if sheet_name != 'Nota':
                    # Cargar la hoja en un DataFrame
                    df = xls.parse(sheet_name)
                    # Crear el nombre del archivo CSV utilizando el nombre de la hoja
                    file_csv = f'{self.csv_file_path}/{sheet_name}.csv'
                    # Guardar el DataFrame en un archivo CSV
                    df.to_csv(file_csv, index=False)
                    logger.info(f'Se ha convertido la hoja "{sheet_name}" a CSV: "{file_csv}"')
            # Remover los archivos generados en el proceso, zip descargado y xls
            for file in [self.zipfile_path, file_xls]:
                if os.path.exists(file):
                    os.remove(file)
                    logger.info(f'El archivo {file} fue removido existosamente')
        except:
            logger.exception(f'El archivo no pudo ser guardado')

# Para ejecutar la descarga 
# download = DownloadPostalCode()
# download.tocsv()

def extractPostalCodes():
    mexico_csvs = f'{os.getcwd()}/locations/mexico'
    
    # Lista para almacenar los valores de "d_codigo" de todos los archivos CSV
    d_codes = []

    if mexico_csvs:
        try:
            # Iterar a través de todos los archivos en el directorio
            for file in os.listdir(mexico_csvs):
                total_path = os.path.join(mexico_csvs, file)
                
                # Cargar el archivo CSV en un DataFrame de pandas
                df = pd.read_csv(total_path)
                
                # Verificar si la columna "d_codigo" existe en el DataFrame
                if 'd_codigo' in df.columns:
                    # Extraer los valores de la columna "d_codigo" y agregarlos a la lista
                    d_codes.extend(df['d_codigo'].tolist())

            print(len(d_codes))        
            return d_codes  # Devolver la lista completa de códigos postales
        except:
            logger.exception('No se pudieron obtener los códigos postales')
    else:
        logger.exception(f'No existe el directorio {mexico_csvs}')

# Para ejecutar la extraccion de codigos postales
postal = extractPostalCodes()