from langchain_text_splitters import RecursiveCharacterTextSplitter
 
 
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """
    Ek badi text string leta hai, aur usse chhote chunks ki list mein
    todke return karta hai.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_text(text)
 
