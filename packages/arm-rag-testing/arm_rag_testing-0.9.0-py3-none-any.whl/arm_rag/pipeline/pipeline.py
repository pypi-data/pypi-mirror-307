import logging
from arm_rag.llm import get_model
from arm_rag.config import CONFIG
from arm_rag.embeddings import Embedding
from arm_rag.vectorstore import get_vectorstore
from arm_rag.document_processing import Document_parser, Chunker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArmRAG:
    def __init__(self, 
                 api_key,
                 wcd_url=None, 
                 wcd_api_key=None,
                 chunking_type=None, 
                 chunking_size=None, 
                 db_type=None, 
                 db_name=None, 
                 k=None, 
                 search_type=None, 
                 weight=None, 
                 distance_metric=None,
                 model_type=None, 
                 llm_model=None,
                 max_tokens=None):
        """
        Initialize the ArmRAG pipeline with the given parameters.
        """
        if db_type == 'weaviate' and not wcd_url and not wcd_api_key:
            raise ValueError("wcd_url and wcd_api_key are required when db_type is 'weaviate'.")
        
        self.model_type = model_type or CONFIG['pipeline']['model_type']
        self.db_type = db_type or CONFIG['pipeline']['vectorstore_type']
        
        self.parser = Document_parser()
        self.chunker = Chunker(chunking_size, chunking_type)
        self.embedder = Embedding()
        self.db = get_vectorstore(self.db_type, wcd_url, wcd_api_key, db_name, k, search_type, weight, distance_metric)
        self.llm = get_model(self.model_type, api_key, llm_model, max_tokens)

    def file_in_db(self, filename):
        """
        Check if a file exists in the database.
        """
        try:
            self.db.open_db()
            return self.db.check_existence(filename)
        except Exception as e:
            logger.error(f"Error checking file in database: {e}")
            raise
        finally:
            self.db.close_db()

    def process_file(self, file_path):
        """
        Process a file by parsing, chunking, embedding, and storing it in the database.
        """
        content_dict, table_dict = self.parser.parse(file_path)
        chunks = []
        for filename, content in content_dict.items():
            chunks_per_file = self.chunker.splitter(content)
            chunks.extend([(filename, chunk) for chunk in chunks_per_file])
            if table_dict.get(f"{filename}_table"):
                chunks.extend([(filename, table_dict[f"{filename}_table"][i]) for i in range(len(table_dict[f"{filename}_table"]))])

        content_only = [chunk[1] for chunk in chunks]
        embeddings = self.embedder.encode(content_only)
        metadatas = [{'chunk': i, 'filename': chunk[0]} for i, chunk in enumerate(chunks)]
            
        try:
            self.db.open_db()
            self.db.add_objects(content_only, embeddings, metadatas)
            logger.info("Document has been successfully processed.")
            return {"message": "Document has been successfully processed."}
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            # raise
        finally:
            self.db.close_db()

    def answer_question(self, question):
        """
        Answer a question using the LLM model and the vector store.
        """

        try:
            self.db.open_db()
            question_embedding = self.embedder.encode([question])[0]
            similar_contents = self.db.search(question_embedding, question)
            
            context = ' '.join(similar_contents)
            answer = self.llm.generate_response(question, context)
            return answer
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
        finally:
            self.db.close_db()