from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np



BASE_DIR = Path(__file__).parent
DOCUMENTS_PATH = BASE_DIR / 'documents'
nltk.download("punkt_tab")  ##downloads the punkt tokenizer models for sentence splitting and tokenization. It is used by the nltk library to tokenize text into sentences and words.
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = embedding_model.tokenizer
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def load_documents():
    documents = []  ##init a list named documents
    for fp in DOCUMENTS_PATH.glob("*.txt"):  ## documents/*.txt
        text =  fp.read_text(encoding = 'utf-8')
        documents.append({'filename':fp.name,'text':text})

    return documents

# def chunk_text(text,overlap = 50 ,chunk_size=500):
#     chunks = []
#     for i in range(0,len(text),chunk_size):    ##start, stop, step
#         chunk = text [i - overlap :i + chunk_size]
#         chunks.append(chunk)

#     return chunks

def count_tokens(text):
    return len(tokenizer.encode(text,add_special_tokens = False))


def chunk_text(text,threshold=0.6,max_tokens=500):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []

    sentence_embeddings = embedding_model.encode(sentences,normalize_embeddings=True)
    chunks = []
    current_chunk = []
    current_tokens = 0

    for i, sentence in enumerate(sentences):
        sentence_tokens = count_tokens(sentence)

        # First sentence
        if not current_chunk:
            current_chunk.append(sentence)
            current_tokens = sentence_tokens
            continue

        similarity = np.dot(sentence_embeddings[i - 1],sentence_embeddings[i])

        semantic_break = similarity < threshold

        token_break = (current_tokens + sentence_tokens > max_tokens)

        if semantic_break or token_break:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def ingest():
    documents = load_documents()
    print (documents)
    for file in documents:
        chunks = chunk_text(file['text'])
        embeddings = embedding_model.encode(chunks)     ##creates embeddings for each chunk of text using the embedding model. The encode method converts the text chunks into numerical vectors that can be used for similarity search and retrieval.  
        ids = [f"{file['filename']}--{i}" for i in range(len(chunks))]
        metadatas = [{"filename":file['filename'],
                      "chunk_index":i,
                      "token_count":count_tokens(chunk) }
                      for i,chunk in enumerate(chunks)]
        print(metadatas)

        collection.add(ids=ids,documents=chunks,embeddings=embeddings.tolist(),
                       metadatas=metadatas,)

    print("Documents ingested successfully")
        # print("~"*7**2)
        # print(file['filename'])

        # for i, chunk in enumerate(chunks):
        #     print(f"`````Chunk {i}`````")
        #     print(chunk)


if __name__ == "__main__":
    ingest()
