import chromadb
 
 
def get_chroma_client(path="chroma_db"):
    """
    ChromaDB ka persistent client banata hai -- data disk pe save hoga.
    Isse call karne wali file mein @st.cache_resource lagana chahiye.
    """
    return chromadb.PersistentClient(path=path)
 
 
def get_or_create_collection(chroma_client, name="querydoc_chunks"):
    """
    Collection (jaise ek "table") return karta hai -- agar pehle se
    hai to wahi, nahi to naya bana deta hai.
    """
    return chroma_client.get_or_create_collection(name=name)
 
 
def store_chunks(collection, chunks, embeddings):
    """
    Purana data collection se hataake, naye chunks + unke embeddings
    ko store karta hai.
    """
    existing_ids = collection.get()["ids"]
    if existing_ids:
        collection.delete(ids=existing_ids)
 
    chunk_ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(
        ids=chunk_ids,
        embeddings=embeddings.tolist(),
        documents=chunks,
    )
 
 
def retrieve_relevant_chunks(collection, query_embedding, n_results=4):
    """
    Diye gaye query_embedding ke sabse similar chunks collection
    se dhoondhke, unka text (list of strings) return karta hai.
    """
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results,
    )
    return results["documents"][0]
 
