import base64
import os

def convert_archive_to_base64(file_path):
    """Convierte un archivo a una cadena de texto en Base64, incluyendo su extensión."""
    with open(file_path, "rb") as file:
        content_bytes = file.read()
        archive_text = base64.b64encode(content_bytes).decode("utf-8")
    
    # Obtiene la extensión del archivo original
    extension = os.path.splitext(file_path)[1]
    
    # Incluye la extensión junto con el contenido en Base64
    return f"{extension}:{archive_text}"

def base64_to_archive(base64_text, folder_path, file_name):
    """Decodifica un texto en Base64 y guarda el archivo con su extensión original en la carpeta especificada."""
    os.makedirs(folder_path, exist_ok=True)
    
    # Verifica si el texto Base64 contiene el separador ":"
    if ":" not in base64_text:
        raise ValueError("El texto en Base64 no tiene el formato esperado 'extension:contenido_base64'.")
    
    # Divide el texto en Base64 para obtener la extensión y el contenido
    extension, base64_content = base64_text.split(":", 1)
    
    # Asegura que el contenido tenga un padding correcto para Base64
    missing_padding = len(base64_content) % 4
    if missing_padding:
        base64_content += '=' * (4 - missing_padding)
    
    # Agrega la extensión al nombre del archivo
    file_path = os.path.join(folder_path, f"{file_name}{extension}")
    
    # Decodifica y guarda el archivo en la ruta especificada
    content_bytes = base64.b64decode(base64_content)
    with open(file_path, "wb") as file:
        file.write(content_bytes)
    return file_path
