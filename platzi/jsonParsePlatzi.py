import argparse
import requests

# Argumentos para el comando
parser = argparse.ArgumentParser(description='Extraer materiales de la API y modificar archivo de texto.')
parser.add_argument('--id', type=str, required=True, help='ID que se añadirá a la URL')
parser.add_argument('--file', type=str, required=True, help='Ruta del archivo de texto que se modificará')

# Parsear los argumentos
args = parser.parse_args()

# Definir la base URL y añadir el ID de los argumentos
base_url = 'https://platzi.com/api/v4/material/syllabus-course/'  # Reemplaza con la URL base de tu API
url = base_url + args.id

# Hacer la solicitud a la API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Lista enumerada para los nombres de materiales
    enumerated_list = []
    
    counter = 1
    for section in data:
        for material in section['materials']:
            enumerated_list.append(f"{counter}. {material['name']}")
            counter += 1

    # Leer el archivo de texto
    try:
        with open(args.file, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Reemplazar cada 'videoName' por un nombre de la lista enumerada
        new_content = []
        name_index = 0

        for line in content:
            if 'videoName' in line and name_index < len(enumerated_list):
                line = line.replace('videoName', enumerated_list[name_index], 1)
                name_index += 1
            new_content.append(line)

        with open(args.file, 'w', encoding='utf-8') as file:
            file.writelines(new_content)

        print(f"Archivo {args.file} modificado con éxito.")
    except FileNotFoundError:
        print(f"Error: El archivo {args.file} no fue encontrado.")
else:
    print(f"Error al hacer la solicitud, código de estado: {response.status_code}")
