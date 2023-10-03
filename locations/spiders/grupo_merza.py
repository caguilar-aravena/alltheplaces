import scrapy
import re
from locations.items import Feature

class GrupoMerzaSpider(scrapy.Spider):
    #Definición de elementos del spider
    name = "grupo_merza"
    allowed_domains = ["www.grupomerza.com"]
    start_urls = ["http://www.grupomerza.com/contactos/sucursales.aspx"]
    # Se usa esto, ya que el proyecto incluye una revisión de duplicados que lo realiza por el elemento ref, que corresponde a los Ids y esta estructura no posee Id
    no_refs = True

    def parse(self, response):
        # Para obtener el contenido del script JavaScript que contiene la información
        script = response.xpath("//script[6]/text()").get()
        # Utilizar una expresión regular para encontrar las llamadas a la función placeMarker
        place_marker_calls = re.findall(r'placeMarker\((.*?)\);', script)

        #Iterar sobre la llamada
        for call in place_marker_calls:
            args = [arg.strip(' "\'') for arg in call.split(',')]

            #Definir el objeto y mapear sus atributos
            item = Feature()
            item['lat'] = args[0]
            item['lon'] = args[1]
            item['name'] = args[2]
            info = args[3]
            info_parts = info.split('<br />')

            # Verificar que existan suficientes partes antes de intentar acceder a ellas
            if len(info_parts) >= 4:
                item['street_address'] = info_parts[0].replace('Calle: ', '').strip()
                item['city'] = info_parts[2].replace('Ciudad: ', '').strip()
                item['state'] = info_parts[3].replace('Estado: ', '').strip()

            # Extrae el teléfono si está presente
            item['phone'] = ""
            for part in info_parts:
                if "Tel." in part:
                    item['phone'] = re.search(r'Tel\.\s*([^<]*)', part).group(1).strip()
            
            yield item

