from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).parent
DOCUMENTS_PATH = BASE_DIR / 'documents'
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def load_documents():
    documents = []  ##init a list named documents
    for fp in DOCUMENTS_PATH.glob("*.txt"):  ## documents/*.txt
        text =  fp.read_text(encoding = 'utf-8')
        documents.append({'filename':fp.name,'text':text})

    return documents

def chunk_text(text,overlap = 50 ,chunk_size=500):
    chunks = []
    for i in range(0,len(text),chunk_size):    ##start, stop, step
        chunk = text [i - overlap :i + chunk_size]
        chunks.append(chunk)

    return chunks


def ingest():
    documents = load_documents()
    for file in documents:
        chunks = chunk_text(file['text'])
        embeddings = embedding_model.encode(chunks)     ##creates embeddings for each chunk of text using the embedding model. The encode method converts the text chunks into numerical vectors that can be used for similarity search and retrieval.  
        ids = [f"{file['filename']}--{i}" for i in range(len(chunks))]
        collection.add(ids=ids,documents=chunks,embeddings=embeddings.tolist(),
                       metadatas=[{"filename":file['filename']} for _ in chunks],)

    print("Documents ingested successfully")
        # print("~"*7**2)
        # print(file['filename'])

        # for i, chunk in enumerate(chunks):
        #     print(f"`````Chunk {i}`````")
        #     print(chunk)


if __name__ == "__main__":
    ingest()
