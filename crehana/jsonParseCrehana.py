import json
import argparse
import requests

def update_video_names(course_id, list_file):
    base_url = "https://www.crehana.com/api/v2/graph/"

    # Payload para obtener respuesta de la API
    query_api = '''
        query CourseModulesQuery($courseId: String!) {
            course(id: $courseId) {
                id
                courseModuleSet {
                    edges {
                        node {
                            id
                            originalId
                            order
                            name
                            duration
                            videoLectureSet {
                                edges {
                                    node {
                                        id
                                        originalId
                                        order
                                        duration
                                        title
                                        videoHashedId
                                        provider
                                        isComplete
                                        videoTypeEnum
                                        uploadState
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    '''

    variables = {
        "courseId": course_id
    }

    payload = {
        "variables": json.dumps(variables),
        "query": query_api
    }

    try:
        response = requests.post(base_url, json=payload)
        if response.status_code == 200:
            data = response.json()

            # Extraer el listado de videos
            video_titles = []
            for module in data['data']['course']['courseModuleSet']['edges']:
                for video in module['node']['videoLectureSet']['edges']:
                    video_titles.append(video['node']['title'])

            # Leer el archivo de texto
            with open(list_file, 'r') as file:
                file_content = file.read()

            # Reemplazar cada 'videoName' por un nombre de la lista enumerada
            for i, title in enumerate(video_titles, start=1):
                file_content = file_content.replace(f"videoName", f"{i}. {title}", 1)

            # Escribir el contenido modificado de nuevo en el archivo
            with open(list_file, 'w') as file:
                file.write(file_content)

            print(f"Archivo {list_file} modificado con éxito.")
        else:
            print(f"Error in API request: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error in request: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo {list_file} no fue encontrado.")
    except IOError as e:
        print(f"Error reading or writing file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Extraer el listado de titulos de la API y modificar archivo de texto.')
    parser.add_argument('--id', type=str, required=True, help='ID del curso')
    parser.add_argument('--file', type=str, required=True, help='Ruta del archivo de texto que se modificará')
    args = parser.parse_args()

    update_video_names(args.id, args.file)

if __name__ == "__main__":
    main()