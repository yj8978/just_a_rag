from pathlib import Path

BASE_DIR = Path(__file__).parent
DOCUMENTS_PATH = BASE_DIR / 'documents'

def load_documents():
    documents = []  ##init a list named documents
    for fp in DOCUMENTS_PATH.glob("*.txt"):  ## documents/*.txt
        text =  fp.read_text(encoding = 'utf-8')
        documents.append({'filename':fp.name,'text':text})

    return documents


if __name__ == "__main__":
    documents = load_documents()
    for file in documents:
        print("~"*7**2)
        print(file['filename'])
        print(file['text'])



