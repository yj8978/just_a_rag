from rag import Rag

def main():
    rag = Rag()
    query = input("Enter your question:")
    answer = rag.ask(query)
    print("Answer:", answer)

if __name__ == "__main__":
    main()