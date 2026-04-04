import cv2
import json
import os
import numpy as np

# Garante que a pasta config existe
os.makedirs('config', exist_ok=True)

vagas = []
pontos_atuais = []

def desenhar_vaga(event, x, y, flags, param):
    global pontos_atuais, vagas
    
    # Se o botão esquerdo do mouse for clicado
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_atuais.append((x, y))
        
        # Quando clicar 4 vezes, fecha o polígono da vaga
        if len(pontos_atuais) == 4:
            vagas.append(pontos_atuais)
            pontos_atuais = [] # Reseta para a próxima vaga

# 1. Inicia a câmera (0 é a webcam padrão, mude para 1 ou 2 se for câmera USB)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Posicione a câmera. Aperte 'c' para CAPTURAR a imagem do estacionamento.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler a câmera.")
        break
        
    cv2.imshow("Camera Ao Vivo - Aperte C para capturar", frame)
    
    # Se apertar 'c', congela o frame e sai deste loop
    if cv2.waitKey(1) & 0xFF == ord('c'):
        frame_congelado = frame.copy()
        break

cap.release()
cv2.destroyAllWindows()

# 2. Abre a tela para desenhar as vagas no frame congelado
cv2.namedWindow("Mapeamento (Clique 4 vezes por vaga. Aperte Q para salvar)")
cv2.setMouseCallback("Mapeamento (Clique 4 vezes por vaga. Aperte Q para salvar)", desenhar_vaga)

while True:
    frame_desenho = frame_congelado.copy()
    
    # Desenha as vagas já concluídas em verde
    for vaga in vagas:
        cv2.polylines(frame_desenho, [np.array(vaga)], isClosed=True, color=(0, 255, 0), thickness=2)   

    # Desenha os pontos que você está clicando agora em vermelho
    for ponto in pontos_atuais:
        cv2.circle(frame_desenho, ponto, 5, (0, 0, 255), -1)

    cv2.imshow("Mapeamento (Clique 4 vezes por vaga. Aperte Q para salvar)", frame_desenho)
    
    # Aperte 'q' para salvar e sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# 3. Salva as coordenadas no arquivo JSON
with open('config/coordenadas.json', 'w') as f:
    json.dump(vagas, f)

print(f"Sucesso! {len(vagas)} vagas foram salvas no arquivo config/coordenadas.json")