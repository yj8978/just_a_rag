from pathlib import Path

BASE_DIR = Path(__file__).parent
DOCUMENTS_PATH = BASE_DIR / 'documents'

def load_documents():
    documents = []  ##init a list named documents
    for fp in DOCUMENTS_PATH.glob("*.txt"):  ## documents/*.txt
        text =  fp.read_text(encoding = 'utf-8')
        documents.append({'filename':fp.name,'text':text})

    return documents

def chunk_text(text,overlap = 5 ,chunk_size=100):
    chunks = []
    for i in range(0,len(text),chunk_size):    ##start, stop, step
        chunk = text [i - overlap :i + chunk_size]
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    for file in documents:
        chunks = chunk_text(file['text'])
        print("~"*7**2)
        print(file['filename'])
        for i, chunk in enumerate(chunks):
            print(f"`````Chunk {i}`````")
            print(chunk)



