import pandas as pd
import requests
import math


def obtener_coordenadas_csv(nombre_ciudad, nombre_pais):
    df = pd.read_csv("worldcities.csv")
    ciudad_info = df[(df['city'] == nombre_ciudad) & (df['country'] == nombre_pais)]

    if ciudad_info.empty:
        raise ValueError(f"No se encontraron coordenadas para {nombre_ciudad}, {nombre_pais} en el CSV.")

    ciudad_info = ciudad_info.iloc[0]
    latitud = ciudad_info['lat']
    longitud = ciudad_info['lng']
    return latitud, longitud


def obtener_coordenadas_api(nombre_ciudad, nombre_pais):
    url = f"https://nominatim.openstreetmap.org/search?q={nombre_ciudad},{nombre_pais}&format=json"
    print(url)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code != 200:
        raise ConnectionError(f"Error al conectar con la API: {response.status_code}")
    try:
        data = response.json()
        if data:
            latitud = float(data[0]['lat'])
            longitud = float(data[0]['lon'])
            return latitud, longitud
        else:
            raise ValueError(f"No se encontraron coordenadas para {nombre_ciudad}, {nombre_pais} en la API.")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        raise


def obtener_coordenadas_mock(nombre_ciudad, nombre_pais):
    coordenadas_fijas = {
        'ciudad1': (12.0464, -77.0428),
        'ciudad2': (-34.6037, -58.3816)
    }
    if nombre_ciudad.lower() == 'lima' and nombre_pais.lower() == 'peru':
        return coordenadas_fijas['ciudad1']
    elif nombre_ciudad.lower() == 'buenos aires' and nombre_pais.lower() == 'argentina':
        return coordenadas_fijas['ciudad2']
    else:
        raise ValueError("No se encontraron coordenadas mock para la ciudad y el país especificados.")


def calcular_distancia_haversine(coord1, coord2):
    lat1, lon1, lat2, lon2 = map(math.radians, [coord1[0], coord1[1], coord2[0], coord2[1]])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    distancia = 6371 * c
    return distancia


def obtener_coordenadas(nombre_ciudad, nombre_pais, fuente):
    if fuente == 'csv':
        return obtener_coordenadas_csv(nombre_ciudad, nombre_pais)
    elif fuente == 'api':
        return obtener_coordenadas_api(nombre_ciudad, nombre_pais)
    elif fuente == 'mock':
        return obtener_coordenadas_mock(nombre_ciudad, nombre_pais)
    else:
        raise ValueError("Fuente desconocida o archivo CSV no proporcionado.")


def tres_ciudades(c1, c2, c3):
    coord1 = obtener_coordenadas(c1[0], c1[1], "csv")
    coord2 = obtener_coordenadas(c2[0], c2[1], "csv")
    coord3 = obtener_coordenadas(c3[0], c3[1], "csv")

    respuesta = [c1, c2, calcular_distancia_haversine(coord1, coord2)]

    dist2 = calcular_distancia_haversine(coord1, coord3)
    if dist2 < respuesta[2]:
        respuesta = [c1, c3, dist2]
    dist3 = calcular_distancia_haversine(coord2, coord3)
    if dist3 < respuesta[2]:
        respuesta = [c2, c3, dist3]

    print(f'Las 2 ciudades más cercanas son {respuesta[0]} y {respuesta[1]} con una distancia de {respuesta[2]:.2f}km.')


def main():
    ciudad1 = ('Lima', 'Peru')
    ciudad2 = ('Buenos Aires', 'Argentina')

    fuente = str(input("Ingrese el modo a conseguir los datos: (mock, csv, api)"))

    try:
        coord1 = obtener_coordenadas(ciudad1[0], ciudad1[1], fuente)
        coord2 = obtener_coordenadas(ciudad2[0], ciudad2[1], fuente)

        distancia = calcular_distancia_haversine(coord1, coord2)
        print(f'La distancia entre {ciudad1[0]}, {ciudad1[1]} y {ciudad2[0]}, {ciudad2[1]} es {distancia:.2f} km.')
    except Exception as e:
        print(f"Se produjo un error: {e}")


def test():
    tres_ciudades(("Lima", "Peru"), ("Bogotá", "Colombia"), ("Buenos Aires", "Argentina"))


if __name__ == '__main__':
    main()
    test()
