# import os
import weaviate
from tabulate import tabulate
# from dotenv import load_dotenv
from arm_rag.config import CONFIG
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery


# load_dotenv()
# wcd_url = os.getenv("WEAVIATE_URL")
# wcd_api_key = os.getenv("WEAVIATE_API_KEY")


class Weaviate_DB:
    def __init__(self, wcd_url, wcd_api_key, name=None, k=None, search_type=None, weight=None):
        if name:
            self.name = name
        else:
            self.name = CONFIG["vectorstore_weaviate"]["name"]
        if k:
            self.K = k
        else:
            self.K = CONFIG["vectorstore_weaviate"]["K"]
        if search_type:
            self.search_type = search_type
        else:
            self.search_type = CONFIG["vectorstore_weaviate"]["search_type"]
        if weight:
            self.weight = weight
        else:
            self.weight = CONFIG["vectorstore_weaviate"]["hybrid_weight"]
        self.wcd_url = wcd_url
        self.wcd_api_key = wcd_api_key
        self.client = None
        self.collection = None


    def open_db(self):
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self.wcd_url,
            auth_credentials=Auth.api_key(self.wcd_api_key),
        )
        try:
            self.collection = self.client.collections.get(self.name)
        except weaviate.exceptions.WeaviateEntityNotFoundException:
            # TODO: specify exactly what we will keep in the db (not just the name)
            self.collection = self.client.collections.create(name=self.name)


    def close_db(self):
        self.client.close()


    def check_existence(self, filename: str):
        try:
            existing_files = set(
                [
                    item.properties["metadata"]["filename"]
                    for item in self.collection.iterator()
                ]
            )
        except:
            existing_files = set()

        if filename in existing_files:
            return True
        return False


    def add_batch_objects(self, text, embedding, metadata):
        with self.collection.batch.dynamic() as batch:
            batch.add_object(
                properties={"text": text, "metadata": metadata}, 
                vector=embedding
            )


    def add_objects(self, texts, embeddings, metadatas):
        for text, embedding, metadata in zip(texts, embeddings, metadatas):
            self.collection.data.insert(properties={"text": text, "metadata": metadata}, 
                                        vector=embedding)
        

    def semantic_search(self, query_vector):
        responses = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=self.K,
            return_metadata=MetadataQuery(distance=True),
            
        )
        output = []
        for response in responses.objects:
            output.append(response.properties['text'])
        return output



    def keyword_search(self, query):
        responses = self.collection.generate.near_text(
            query=query,
            limit=self.K,
        )
        output = []
        for response in responses.objects:
            output.append(response.properties['text'])
        return output



    def hybrid_search(self, vector, query):
        responses = self.collection.query.hybrid(
            query=query,
            limit=self.K,
            alpha=self.weight,
            vector=vector
        )
        output = []
        # print(responses)
        for response in responses.objects:
            output.append(response.properties['text'])
        return output


    def search(self, vector, text):
        if self.search_type == "semantic":
            return self.semantic_search(vector)
        elif  self.search_type == "keyword":
            return self.keyword_search(text)
        elif self.search_type == "hybrid":
            return self.hybrid_search(vector=vector, query=text)


    def clear_all(self):
        """Clear all documents from the store"""
        self.client.collections.delete(self.name)


    def display_collection_contents(self, limit):
        """Display the contents of a collection in a formatted table"""
        try:
            response = self.collection.query.fetch_objects(limit=limit, include_vector=True)
            # Prepare table data
            headers = ["Text (truncated)", "Metadata"]
            table_data = []

            for obj in response.objects:
                # Truncate text if it's too long
                truncated_text = (
                    obj.properties["text"][:100] + "..."
                    if len(obj.properties["text"]) > 100
                    else obj.properties["text"]
                )
                table_data.append(
                    [
                        truncated_text,
                        str(obj.properties.get("metadata", {})),
                    ]
                )

            # Print the table
            print(f"\nCollection: {self.name}")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(f"Error displaying collection contents: {e}")
            raise
