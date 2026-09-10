from sentence_transformers import SentenceTransformer
 
 
def load_embedding_model():
    """
    Embedding model load karke return karta hai. Isse call karne wali
    file mein @st.cache_resource lagana chahiye, taaki model baar-baar
    reload na ho.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")
 
 
def get_embeddings(embedding_model, texts):
    """
    Text ki list leta hai (chunks ya ek question), aur unke
    embeddings (numbers) return karta hai.
    """
    return embedding_model.encode(texts)
 
