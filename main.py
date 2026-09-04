from ingest import Ingest
from rag import Rag


def main():

    while True:

        print("\n======================")
        print("       RAG SYSTEM")
        print("======================")
        print("1. Ingest / Rebuild Collection")
        print("2. Ask Question")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nStarting ingestion...")
            ingester = Ingest()
            ingester.ingest()

        elif choice == "2":
            rag = Rag()
            while True:
                query = input("\nEnter your question "
                    "(type 'exit' to return): "
                )

                if query.lower() == "exit":
                    break
                print("\nAnswer:")
                print(rag.ask(query))

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()