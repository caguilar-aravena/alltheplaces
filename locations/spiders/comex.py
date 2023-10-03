import scrapy
from codigopostalMX import extractPostalCodes
from locations.dict_parser import DictParser
import pandas as pd

class ComexSpider(scrapy.Spider):
    #Definir los parametros de la marca para el proyecto
    name = "comex"
    allowed_domains = ["tienda.comex.com.mx"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    # Crear una lista para almacenar los datos
    data_list = []

    def start_requests(self):
        # Función para generar las url por cada código postal, ya que mediante el código postal se pueden obtener las coordenadas
        url = "https://tienda.comex.com.mx/public/v1/locations/address/{}"
        for postalcode in extractPostalCodes():
            yield scrapy.Request(url.format(postalcode), callback=self.parse_postalcode, meta={'postalcode': postalcode})
        
        
    def parse_postalcode(self, response):
        # Obtener el código postal de los metadatos
        postalcode = response.meta['postalcode']

        # Obtener latitud y longitud de la respuesta
        lat = response.json()['latitude']
        lon = response.json()['longitude']

        # Agregar los datos a la lista
        self.data_list.append({'Latitud': lat, 'Longitud': lon, 'Código Postal': postalcode})

        # Continuar con el proceso de extracción de tiendas
        url = 'https://tienda.comex.com.mx/public/v1/stores/location/{},{}?radius=12'
        yield scrapy.Request(url.format(lat, lon), callback=self.parse)

    def parse(self, response):
        # Itera sobre la respuesta de las coordenadas y utiliza una función que en base a la estructura del proyecto mapea automáticamente cada POI
        for store in response.json()['stores']:
            item = DictParser.parse(store)
            yield(item)
    
    def closed(self, reason):
        # Cuando el spider se cierra, crea un DataFrame y guarda este en un archivo CSV
        df = pd.DataFrame(self.data_list)
        df.to_csv('comex_data.csv', index=False)
