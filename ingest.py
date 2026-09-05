import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

from config import (
    DOCUMENTS_PATH,
    CHROMA_PATH,
    EMBEDDING_MODEL,
    COLLECTION_NAME,
    CHUNK_THRESHOLD,
    MAX_TOKENS
)


class Ingest:
    def __init__(self):
        # Embedding model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        # Tokenizer
        self.tokenizer = self.embedding_model.tokenizer
        # ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    def load_documents(self):
        documents = []
        for fp in DOCUMENTS_PATH.glob("*.txt"):
            text = fp.read_text(encoding="utf-8")
            documents.append({
                "filename": fp.name,
                "text": text
            })
        return documents

    def count_tokens(self, text):
        return len(self.tokenizer.encode(text,add_special_tokens=False))

    def chunk_text(self,text,threshold=CHUNK_THRESHOLD,max_tokens=MAX_TOKENS):
        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return []

        sentence_embeddings = self.embedding_model.encode(sentences,normalize_embeddings=True)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for i, sentence in enumerate(sentences):
            sentence_tokens = self.count_tokens(sentence)

            # First sentence
            if not current_chunk:
                current_chunk.append(sentence)
                current_tokens = sentence_tokens
                continue

            similarity = cosine_similarity([sentence_embeddings[i - 1]],[sentence_embeddings[i]])[0][0]
            semantic_break = similarity < threshold
            token_break = (current_tokens + sentence_tokens> max_tokens)

            if semantic_break or token_break:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens

            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens

        # Add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def reset_collection(self):
        try:
            self.chroma_client.delete_collection(COLLECTION_NAME)
            print(f"Collection '{COLLECTION_NAME}' deleted successfully.")
        except Exception:
            print(f"Collection '{COLLECTION_NAME}' does not exist or could not be deleted.")

        self.collection = self.chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    def ingest(self):
        self.reset_collection()
        documents = self.load_documents()
        print(f"Found {len(documents)} documents.")
        for file in documents:
            print(f"\nProcessing: {file['filename']}")
            chunks = self.chunk_text(file["text"])
            print(f"Created {len(chunks)} chunks.")
            embeddings = self.embedding_model.encode(chunks)
            ids = [f"{file['filename']}--{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "filename": file["filename"],
                    "chunk_index": i,
                    "token_count": self.count_tokens(
                        chunk
                    )
                }
                for i, chunk in enumerate(chunks)
            ]

            self.collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )

        print(f"\nDocuments ingested successfully.")
        print(f"Total chunks in database: {self.collection.count()}")

if __name__ == "__main__":
    nltk.download("punkt_tab")
    ingester = Ingest()
    ingester.ingest()