# test_chroma_helper.py

from chroma_helper_module import ChromaHelper

def test_chroma_helper():
    # Step 1: Initialize ChromaHelper with a test collection name
    chroma_helper = ChromaHelper("test_collection")

    # Step 2: Define sample documents to upsert
    documents = [
        {"id": "doc1", "text": "hello, world!"},
        {"id": "doc2", "text": "how are you today"},
        {"id": "doc3", "text": "Good bye, see you later"}
    ]

    # Step 3: Upsert documents into the collection
    chroma_helper.upsert_documents(documents)
    print("Documents upserted successfully.")

    # Step 4: Define a query text to find similar documents
    query_text = "Hello, Amitav!"
    
    # Step 5: Perform the query and get results
    results = chroma_helper.query_similar(query_text)
    
    # Step 6: Display the query results
    print("Query results:")
    for result in results:
        print(
            f"For the query: '{result['query']}', "
            f"found similar document: '{result['similar_document']}' "
            f"(ID: {result['id']}, Distance: {result['distance']})"
        )

if __name__ == "__main__":
    test_chroma_helper()
