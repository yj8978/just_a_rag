import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_collection(name="documents")

def search(query,top_k=3):                 ##two parameters: query and top_k which returns the top_k most result
    query_embedding =  embedding_model.encode(query)
    results = collection.query(
        query_embeddings = [query_embedding.tolist()],
        n_results = top_k
    )
    return results


if __name__ == "__main__":
    query = "What is Number theory?"
    results = search(query)
    for document in results["documents"][0]:
        print("=" * 50)
        print(document)