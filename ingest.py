from pathlib import Path

DOCUMENTS_PATH = Path('documents')

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



