import cv2
import os

# Cria a pasta para salvar as fotos
os.makedirs('dataset_carrinhos', exist_ok=True)

cap = cv2.VideoCapture(0)
contador = 0

print("Aperte 's' para salvar uma foto. Aperte 'q' para sair.")
print("Dica: Mova os carrinhos de lugar a cada foto!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Tirar Fotos para Treinamento", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('s'):
        # Salva a foto na pasta
        nome_arquivo = f"dataset_carrinhos/foto_{contador}.jpg"
        cv2.imwrite(nome_arquivo, frame)
        print(f"Foto {contador} salva!")
        contador += 1
    elif tecla == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()