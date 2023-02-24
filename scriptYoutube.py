import sys
import urllib.request
import re
import csv

# Pregunta si esta el script junto con los 2 argumentos. En caso de no estar bien puesto, salta un mensaje de error.
if len(sys.argv) != 3:
    print("Algo anda mal")
    sys.exit(1)

# Variables que se definen por argumentos.
url = sys.argv[1] # Indicamos la URL. e.j: "https://www.youtube.com/channel/'codigo'/videos".
file_name = sys.argv[2] # Indicamos el fichero csv que queremos guardar.¡OJO! Hay que indicar la extension .csv. e.j: "lista.csv".

# Accedemos a la URL y leemos el contenido HTML. En caso de que no pueda acceder mostrará un mensaje de error.
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
except urllib.error.HTTPError as e:
    print(f"Error al acceder a la URL: {e}")
    sys.exit(1)

# Buscamos los enlaces de los videos usando una expresión regular
regex = r"watch\?v=(\S{11})"
matches = re.findall(regex, html)

# Buscamos los títulos de los videos correspondientes a los enlaces de video usando una expresión regular.
video_titles = [] # Se crea una lista vacia.
for match in matches: # Busca los enlaces de los videos
    video_url = f"https://www.youtube.com/watch?v={match}"
    try:
        with urllib.request.urlopen(video_url) as response:
            video_html = response.read().decode('utf-8') # Abrimos el enlace del video y leemos el contenido HTML.
    except urllib.error.HTTPError as e: # Si el video no esta disponible, saltará un error y se cerrará.
        print(f"Error al acceder al video {video_url}: {e}")
        continue
    title_regex = r"<title>(.*?) - YouTube</title>" # Una vez que accedemos, buscamos el titulo del video.
    title_match = re.search(title_regex, video_html)
    if title_match:
        video_titles.append(title_match.group(1)) # Si existe un titulo, lo añadimos a la lista creada anteriormente.
    else:
        video_titles.append("Título no encontrado") # Si no existe, mostrara un mensaje indicando que no hay titulo.

# Construimos una lista de tuplas con la siguiente estrucutura: (nombre del video, enlace del video)
videos = [(title, f"https://www.youtube.com/watch?v={match}") for title, match in zip(video_titles, matches)]

# Guardamos la lista de tuplas en un archivo CSV
with open(file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre", "Enlace"])
    writer.writerows(videos)

# Mostramos por pantalla un mensaje indicando que se han guardado los titulos y enlaces de los videos en el fichero indicado.
print(f"Se han guardado los nombres y enlaces de {len(videos)} videos del canal {url} en el archivo {file_name}")
