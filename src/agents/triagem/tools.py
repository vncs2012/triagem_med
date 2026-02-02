import numpy as np
from PIL import Image
from pathlib import Path
from tensorflow import keras
from src.config import Settings

class ToolTriagem():
    def __init__(self):
        self.settings = Settings()
        self.model = None

    def _load_model(self):
        if self.model is None:
            self.model = keras.models.load_model(self.settings.model_path)
        return self.model

    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """Pré-processa a imagem para o modelo CNN.
        
        Aplica as mesmas transformações usadas no treinamento:
        - Redimensionamento para 224x224
        """
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))

        img_array = np.array(img, dtype=np.float32)
        img_array = img_array - np.mean(img_array)
        
        std = np.std(img_array)
        if std > 0:
            img_array = img_array / std
        
        img_batch = np.expand_dims(img_array, axis=0)
        
        return img_batch

    def analisar_imagem(self, image_path: str) -> dict:
        """Analisa uma imagem de raio-X e retorna o diagnóstico.
        
        Args:
            image_path: Caminho completo para o arquivo de imagem
            
        Returns:
            Dicionário com status, mensagem e diagnóstico
        """
        try:
            if not Path(image_path).exists():
                return {
                    "status": "erro", 
                    "mensagem": f"Arquivo não encontrado: {image_path}"
                }
            
            model = self._load_model()
            
            img_batch = self._preprocess_image(image_path)
            
            prediction = model.predict(img_batch, verbose=0)
            confidence = float(prediction[0][0])
            
            class_name = "PNEUMONIA" if confidence >= 0.5 else "NORMAL"
            
            priority = "BAIXA"
            notes = "Exame dentro da normalidade. Acompanhamento de rotina se sintomas persistirem."
            if 0.45 <= confidence < 0.5:
                priority = "MÉDIA"
                notes = "Sinais suspeitos detectados. Recomenda-se acompanhamento médico em 24-48h."
            elif 0.5 <= confidence < 0.7:
                priority = "ALTA"
                notes = "Pneumonia detectada. Tratamento urgente recomendado. Avaliação médica no mesmo dia."
            elif confidence >= 0.7: 
                priority = "CRÍTICA"
                notes = "Caso grave detectado. ATENÇÃO MÉDICA IMEDIATA OBRIGATÓRIA"
           
            diagnosis = {
                "classification": class_name,
                "confidence": f"{100 - confidence:.2%}",
                "priority": priority,
                "notes": notes
            }
            
            return {
                "status": "sucesso", 
                "mensagem": "Imagem analisada com sucesso",
                "diagnostico": diagnosis
            }

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return {
                "status": "erro", 
                "mensagem": f"Falha ao analisar imagem: {str(e)}"
            }