from arm_rag.config import CONFIG
from sentence_transformers import SentenceTransformer


class Embedding:
    def __init__(self):
        self.model = SentenceTransformer(CONFIG['embeddings']['model'])
        
    
    def encode(self, chunks):
        embeddings = self.model.encode(chunks, normalize_embeddings=True)
        return embeddings.tolist()
    