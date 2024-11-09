import base64
import os

def convert_archive_to_base64(file_path):
    """Convierte un archivo a una cadena de texto en Base64."""
    with open(file_path, "rb") as file:
        content_bytes = file.read()

        archive_text = base64.b64encode(content_bytes).decode("utf-8")
        extension = os.path.splitext(file_path)[1]

    return f"{extension}:{archive_text}"

def base64_to_archive(base64_text, folder_path, file_name):
    """Decodifica un texto en Base64 y guarda el archivo en la carpeta especificada."""
    os.makedirs(folder_path, exist_ok=True)
    
    extension, base64_content = base64_text.split(":", 1)
    # Construye la ruta completa del archivo
    file_path = os.path.join(folder_path, f"{file_name}{extension}")
    
    # Decodifica y guarda el archivo en la ruta especificada
    content_bytes = base64.b64decode(base64_text)
    with open(file_path, "wb") as file:
        file.write(content_bytes)
    return file_path
