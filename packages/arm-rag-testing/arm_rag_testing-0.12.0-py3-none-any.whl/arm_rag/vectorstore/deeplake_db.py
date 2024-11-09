from tabulate import tabulate
from deeplake import VectorStore
from arm_rag.config import CONFIG


class Deeplake_DB:
    def __init__(self, name=None, k=None, distance_metric=None):
        if name:
            self.name = name
        else:
            self.name = CONFIG['vectorstore_deeplake']['path']
        if k:
            self.K = k
        else:
            self.K = CONFIG['vectorstore_deeplake']['K']
        if distance_metric:
            self.distance_metric = distance_metric
        else:
            self.distance_metric = CONFIG['vectorstore_deeplake']['distance_metric']
        self.collection = None


    def open_db(self):
        self.collection = VectorStore(self.name)


    def close_db(self):
        pass


    def add_objects(self, texts, vectors, metadatas):
        self.collection.add(
            text=texts,
            embedding=vectors,
            metadata=metadatas
        )
        self.collection.commit()


    def search(self, vector, query=None):
        """
        Finds most similar K vectors to the given vector and returns corresponding texts.
        
        Args:
            vector (list): embedding vector for which function finds similar vectors.
            
        Returns:
            List['str']: Corresponding texts of the K most similar vectors.
        """
        output = self.collection.search(
            embedding=vector,
            k=self.K,
            distance_metric=self.distance_metric)
        return output['text']
    

    def check_existence(self, filename):
        """Checks whether filname already exists in DB or not"""
        existing_filenames = []
        for metadata in self.collection.tensors()['metadata'].data()['value']:
            existing_filenames.append(metadata['filename'])
        existing_filenames = set(existing_filenames)
        if filename in existing_filenames:
            return True
        return False

    def clear_all(self):
        self.collection.delete(delete_all=True)


    def display_collection_contents(self, limit):
        """Displays the contents of a collection in a formatted table"""
        try:
            headers = ["Text (truncated)", "Metadata"]
            table_data = []
            for txt, metadata in zip(
                self.collection.tensors()['text'].data()['value'][:limit], 
                self.collection.tensors()['metadata'].data()['value'][:limit]):
                truncated_text = (
                    txt[:100] + "..."
                    if len(txt) > 100
                    else txt
                )
                table_data.append(
                    [
                        truncated_text,
                        str(metadata),
                    ]
                )
            print(f"\nCollection path: {self.path}")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(f"Error displaying collection contents: {e}")
            
