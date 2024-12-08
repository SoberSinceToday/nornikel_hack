from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LLMProcessor:
    def __init__(self, model_path="t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    def extract_features(self, text: str):
        """Обрабатывает текст и возвращает JSON с фичами."""
        prompt = f"Extract features and values from the following text:\n{text}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(**inputs)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Пример обработки: строка -> JSON
        features = eval(result)  # Предполагается, что модель возвращает JSON-строку
        return features


llm_processor = LLMProcessor()
