from ultralytics import YOLO

# Carrega o modelo que VOCÊ treinou agora
modelo = YOLO("best.pt") 

# No seu loop de detecção, use um threshold (confiança) baixo no início para testar
resultados = modelo.predict(frame, conf=0.5)