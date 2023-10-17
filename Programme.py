import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Charger la vidéo
video = cv2.VideoCapture('/content/Snapinsta.app_video_317061658_859478755529507_132736734692619438_n.mp4')
frame_width, frame_height = int(video.get(3)), int(video.get(4))

# Créer un objet writer pour écrire la vidéo de sortie
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))

# Fonction pour diviser le texte en plusieurs lignes
def wrap_text(text, width, font):
    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        if font.getsize(line + word)[0] < width:
            line += (word + ' ')
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    return lines

# Charger une police TTF qui supporte les caractères spéciaux
font = ImageFont.truetype("Lato-Bold.ttf", 40)  # Ajuster la taille de la police ici

# Boucle pour lire et modifier chaque frame
while True:
    ret, frame = video.read()
    if not ret:
        break
        
    # Créer une image noire semi-transparente
    overlay = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    cv2.addWeighted(overlay, 0.4, frame, 0.4, 0, frame)
    
    # Convertir l'image BGR d'OpenCV en RGB pour Pillow
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    
    # Créer un objet draw
    draw = ImageDraw.Draw(pil_image)
    
    # Configurer et ajouter le texte au centre de la frame
    text = "La vie est comme une bicyclette, pour garder l’équilibre, il faut avancer"
    margin = 100  # Définir une marge de 100 pixels
    max_width = frame_width - 2 * margin
    lines = wrap_text(text, max_width, font)
    
    y = (frame_height - len(lines) * 40) // 2  # Position de départ y, ajuster '40' selon la hauteur de la ligne
    for line in lines:
        text_width, text_height = font.getsize(line)
        text_x, text_y = (frame_width - text_width) // 2, y
        draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255, 255))
        y += 50  # Ajuster '40' selon la hauteur de la ligne
    
    # Convertir l'image RGB de Pillow en BGR pour OpenCV
    bgr_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    # Écrire la frame dans la vidéo de sortie
    out.write(bgr_frame)

# Relâcher les objets video et out
video.release()
out.release()
