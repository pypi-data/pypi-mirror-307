# chroma_helper.py

import chromadb

class ChromaHelper:
    def __init__(self, collection_name: str):
        """
        Initializes a Chroma client and creates or retrieves a collection.

        Parameters:
            collection_name (str): The name of the collection to work with.
        """
        self.client = chromadb.Client()
        self.collection = self._get_or_create_collection(collection_name)
    
    def _get_or_create_collection(self, name: str):
        """
        Creates or retrieves a collection based on the name.

        Parameters:
            name (str): The name of the collection.

        Returns:
            Collection: The Chroma collection instance.
        """
        try:
            return self.client.create_collection(name=name)
        except Exception:  # Fallback error handling
            return self.client.get_collection(name=name)
    
    def upsert_documents(self, documents: list):
        """
        Upserts a list of documents into the collection.

        Parameters:
            documents (list): List of dictionaries, each with 'id' and 'text' keys.
        """
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        self.collection.upsert(ids=ids, documents=texts)
    
    def query_similar(self, query_text: str, n_results: int = 5):
        """
        Queries the collection for similar documents based on the input text.

        Parameters:
            query_text (str): The text to query.
            n_results (int): The number of similar documents to retrieve.

        Returns:
            list: The results containing similar documents, IDs, and distances.
        """
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return [
            {
                "query": query_text,
                "similar_document": document,
                "id": results["ids"][0][idx],
                "distance": results["distances"][0][idx]
            }
            for idx, document in enumerate(results["documents"][0])
        ]

# Example usage
if __name__ == "__main__":
    chroma_helper = ChromaHelper()
    # documents = [
    #     {"id": "doc1", "text": "hello, world!"},
    #     {"id": "doc2", "text": "how are you today"},
    #     {"id": "doc3", "text": "Good bye, see you later"}
    # ]
    # chroma_helper.upsert_documents(documents)
    
    # query_text = "Hello, Amitav swain!"
    # results = chroma_helper.query_similar(query_text)
    # for result in results:
    #     print(f"For the query: {result['query']},")
    #     print(f"Found similar document: {result['similar_document']} (ID: {result['id']}, Distance: {result['distance']})")
