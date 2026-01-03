from PIL import Image
from PIL.ExifTags import TAGS
import io

def get_detailed_exif(image):
    """
    Extrai metadados EXIF detalhados de um objeto de imagem PIL.
    Focado em capturar dados técnicos para análise de fotografia (Canon e iPhone).
    """
    exif_data = {}
    
    # Tenta obter os dados EXIF da imagem
    try:
        info = image._getexif()
    except Exception:
        return {}

    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            
            # 1. Tratamento da Velocidade do Obturador (Shutter Speed)
            # O Shutter Speed pode vir como 'ExposureTime' ou 'ShutterSpeedValue'
            if decoded in ['ExposureTime', 'ShutterSpeedValue']:
                if isinstance(value, tuple):
                    # Transforma frações (ex: 1/125) em string legível
                    exif_data['Shutter Speed'] = f"{value[0]}/{value[1]}s"
                elif isinstance(value, float):
                    # Caso venha como float, tenta converter para fração comum ou mantém decimal
                    if value < 1:
                        den = int(1/value)
                        exif_data['Shutter Speed'] = f"1/{den}s"
                    else:
                        exif_data['Shutter Speed'] = f"{value}s"
                else:
                    exif_data['Shutter Speed'] = str(value)

            # 2. Tratamento da Abertura (Aperture/F-Number)
            elif decoded == 'FNumber':
                exif_data['Aperture'] = f"f/{float(value)}"

            # 3. Tratamento do ISO
            elif decoded == 'ISOSpeedRatings':
                exif_data['ISO'] = value

            # 4. Tratamento da Distância Focal (Focal Length)
            elif decoded == 'FocalLength':
                exif_data['Focal Length'] = f"{float(value)}mm"

            # 5. Outros metadados relevantes
            elif decoded in ['Make', 'Model', 'LensModel', 'DateTimeOriginal']:
                exif_data[decoded] = value
                    
    return exif_data

def format_mentor_prompt(device_name, exif):
    """
    Cria uma string estruturada para o Gemini, combinando os dados técnicos
    e reforçando a necessidade de seguir o template de resposta.
    """
    if exif:
        exif_str = ", ".join([f"{k}: {v}" for k, v in exif.items()])
    else:
        exif_str = "No EXIF metadata found."
    
    prompt = (
        f"The user is submitting a photo captured with a {device_name}. "
        f"Technical Metadata found: [{exif_str}]. "
        "Please analyze this image and provide your feedback using the MANDATORY RESPONSE TEMPLATE "
        "defined in your system instructions, including the Lightroom Recipe."
    )
    return prompt