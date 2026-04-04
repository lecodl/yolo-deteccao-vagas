import cv2
import json
import numpy as np
from ultralytics import YOLO

# 1. Carrega as coordenadas das vagas que você salvou
with open('config/coordenadas.json', 'r') as f:
    vagas_salvas = json.load(f)

# Converte as vagas para o formato matemático do OpenCV
vagas = [np.array(vaga, np.int32) for vaga in vagas_salvas]

# 2. Carrega o modelo de IA YOLOv8 Nano (leve e rápido para tempo real)
print("Carregando IA...")
modelo = YOLO("best.pt") 

# 3. Liga a câmera (Mude o número se sua câmera externa for 1 ou 2)
cap = cv2.VideoCapture(0)

print("Sistema rodando! Aperte 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 4. A MÁGICA: O YOLO analisa o frame e acha os objetos
    resultados = modelo(frame, verbose=False)
    caixas = resultados[0].boxes

    # Lista para guardar onde estão os carros
    centros_carros = []

    # 5. Filtra apenas os carros/caminhões/ônibus
    for caixa in caixas:
        classe = int(caixa.cls[0])
        # Classes COCO: 2 = carro, 5 = ônibus, 7 = caminhão
        if classe == 0: 
            # Pega as coordenadas da caixa do carro
            x1, y1, x2, y2 = map(int, caixa.xyxy[0])
            
            # Calcula o meio do carro
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            centros_carros.append((cx, cy))
            
            # (Opcional) Desenha um pontinho azul no meio do carro detectado
            cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

    # 6. Verifica se o meio do carro está dentro de alguma vaga
    for vaga in vagas:
        ocupada = False
        
        for cx, cy in centros_carros:
            # pointPolygonTest checa se o ponto (cx, cy) está dentro do polígono da vaga
            dentro = cv2.pointPolygonTest(vaga, (cx, cy), False)
            if dentro >= 0:
                ocupada = True
                break # Achou um carro aqui, não precisa olhar os outros

        # 7. Pinta a vaga de vermelho (Ocupada) ou Verde (Livre)
        cor = (0, 0, 255) if ocupada else (0, 255, 0)
        texto = "Ocupada" if ocupada else "Livre"
        
        # Desenha a linha da vaga e o texto
        cv2.polylines(frame, [vaga], True, cor, 2)
        cv2.putText(frame, texto, (vaga[0][0], vaga[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)

    # Mostra a imagem final na tela
    cv2.imshow("Monitoramento Inteligente", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()