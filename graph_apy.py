#EV_2 PROGRAMACION Y REDES VIRTUALIZADAS (SDN NFV)_001D
#GRUPO 10: MATÍAS ALFARO, MARTÍN CUADROS, JOSÉ PADILLA
#FECHA 28-05-2024

import requests

# Reemplaza 'your_valid_api_key' con tu token de GraphHopper
API_KEY = 'cb4985ef-be87-4485-a812-804ab6f3f5c6'
GEOCODE_URL = 'https://graphhopper.com/api/1/geocode'
ROUTE_URL = 'https://graphhopper.com/api/1/route'

def get_coordinates(city):
    response = requests.get(GEOCODE_URL, params={'q': city, 'locale': 'es', 'key': API_KEY})
    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            return data['hits'][0]['point']['lat'], data['hits'][0]['point']['lng']
    print(f"No se encontraron coordenadas para la ciudad: {city}")
    return None

def get_route_info(origin_coords, destination_coords):
    response = requests.get(ROUTE_URL, params={
        'point': [f"{origin_coords[0]},{origin_coords[1]}", f"{destination_coords[0]},{destination_coords[1]}"],
        'vehicle': 'car',
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true',
        'key': API_KEY
    })
    if response.status_code == 200:
        return response.json()
    print("Error al obtener la ruta.")
    return None

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

def main():
    while True:
        origen = input("Ingrese la Ciudad de Origen (o 's'/'salir' para terminar): ").strip()
        if origen.lower() in ['s', 'salir']:
            break

        destino = input("Ingrese la Ciudad de Destino: ").strip()
        if destino.lower() in ['s', 'salir']:
            break

        origin_coords = get_coordinates(origen)
        destination_coords = get_coordinates(destino)

        if not origin_coords or not destination_coords:
            continue

        route_info = get_route_info(origin_coords, destination_coords)
        if not route_info or 'paths' not in route_info:
            continue

        path = route_info['paths'][0]
        distance_km = path['distance'] / 1000
        time_seconds = path['time'] / 1000
        formatted_time = format_duration(time_seconds)

        print(f"\nDistancia entre {origen} y {destino}: {distance_km:.2f} km")
        print(f"Duración del viaje: {formatted_time} (HH:MM:SS)\n")
        print("Narrativa del viaje:")
        for instr in path['instructions']:
            print(f"{instr['distance']/1000:.2f} km - {instr['text']}")

if __name__ == "__main__":
    main()

