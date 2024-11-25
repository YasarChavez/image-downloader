import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def descargar_imagenes_paginadas(base_url, carpeta_destino, num_paginas):
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # Cargar nombres de imágenes ya existentes en la carpeta destino
    imagenes_descargadas = set(os.listdir(carpeta_destino))

    contador_imagenes = len(imagenes_descargadas)

    for pagina in range(1, num_paginas + 1):
        # Construir la URL para la página actual
        url = f"{base_url}&page={pagina}"
        print(f"Procesando página: {pagina} -> {url}")
        
        try:
            respuesta = requests.get(url, headers=headers)
            respuesta.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            continue

        # Analizar el contenido HTML
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        imagenes = soup.find_all('img')

        if not imagenes:
            print(f"No se encontraron imágenes en la página {pagina}.")
            continue

        print(f"Se encontraron {len(imagenes)} imágenes en la página {pagina}.")

        for img in imagenes:
            src = img.get('src')
            if not src:
                continue

            # Obtener el nombre de la imagen desde la URL
            url_imagen = urljoin(base_url, src)
            nombre_imagen = os.path.basename(url_imagen)

            # Verificar si la imagen ya está descargada
            if nombre_imagen in imagenes_descargadas:
                print(f"Imagen ya descargada, ignorando: {nombre_imagen}")
                continue

            headers_imagen = {
                'User-Agent': headers['User-Agent'],
                'Referer': base_url
            }

            try:
                img_respuesta = requests.get(url_imagen, headers=headers_imagen, stream=True)
                img_respuesta.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al descargar {url_imagen}: {e}")
                continue

            contador_imagenes += 1
            ruta_imagen = os.path.join(carpeta_destino, nombre_imagen)

            with open(ruta_imagen, 'wb') as archivo:
                for chunk in img_respuesta.iter_content(1024):
                    archivo.write(chunk)

            imagenes_descargadas.add(nombre_imagen)  # Añadir al conjunto para futuras verificaciones
            print(f"Imagen guardada: {ruta_imagen}")

    print(f"Descarga completada. Total de imágenes nuevas descargadas: {contador_imagenes - len(imagenes_descargadas)}")

# Ejemplo de uso
if __name__ == "__main__":
    base_url = input("Ingresa la URL base de la página web (sin el parámetro &page): ")
    num_paginas = int(input("Ingresa el número total de páginas a descargar: "))
    carpeta = "imagenes_descargadas"
    descargar_imagenes_paginadas(base_url, carpeta, num_paginas)
