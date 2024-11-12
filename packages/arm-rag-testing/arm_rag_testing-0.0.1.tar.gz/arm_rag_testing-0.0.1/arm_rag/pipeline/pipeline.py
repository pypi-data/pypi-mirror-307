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
                 max_tokens=None,
                 stream=False):
        """
        Initialize the ArmRAG pipeline with the given parameters.
        """
        logger.info("Initializing ArmRAG pipeline with provided parameters.")
        
        if db_type == 'weaviate' and not wcd_url and not wcd_api_key:
            logger.error("wcd_url and wcd_api_key are required for 'weaviate' db_type.")
            raise ValueError("wcd_url and wcd_api_key are required when db_type is 'weaviate'.")
        
        self.model_type = model_type or CONFIG['pipeline']['model_type']
        if not db_type:
            self.db_type = db_type or CONFIG['pipeline']['vectorstore_type']
        else:
            self.db_type = db_type
        
        logger.debug(f"Model type set to: {self.model_type}")
        logger.debug(f"Vector store type set to: {self.db_type}")

        self.parser = Document_parser()
        self.chunker = Chunker(chunking_size, chunking_type)
        self.embedder = Embedding()
        self.db = get_vectorstore(self.db_type, wcd_url, wcd_api_key, db_name, k, search_type, weight, distance_metric)
        self.llm = get_model(self.model_type, api_key, llm_model, max_tokens, stream)

        logger.info("ArmRAG pipeline initialized successfully.")

    def file_in_db(self, filename):
        """
        Check if a file exists in the database.
        """
        logger.info(f"Checking if file '{filename}' exists in the database.")
        
        try:
            self.db.open_db()
            exists = self.db.check_existence(filename)
            logger.info(f"File existence check completed for '{filename}': {exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking file in database: {e}")
            raise
        finally:
            self.db.close_db()
            logger.debug("Database connection closed after file existence check.")

    def process_file(self, file_path):
        """
        Process a file by parsing, chunking, embedding, and storing it in the database.
        """
        logger.info(f"Processing file: {file_path}")
        
        content_dict, table_dict = self.parser.parse(file_path)
        logger.debug(f"Parsed content and table data from '{file_path}'.")

        chunks = []
        for filename, content in content_dict.items():
            logger.debug(f"Chunking content for file: {filename}")
            chunks_per_file = self.chunker.splitter(content)
            chunks.extend([(filename, chunk) for chunk in chunks_per_file])

            if table_dict.get(f"{filename}_table"):
                logger.debug(f"Adding table chunks for file: {filename}")
                chunks.extend([(filename, table_dict[f"{filename}_table"][i]) for i in range(len(table_dict[f"{filename}_table"]))])
        print("CHUNKS: ", chunks)
        content_only = [chunk[1] for chunk in chunks]
        print("CONTENT ONLY: ", content_only)
        logger.info(f"Generating embeddings for {len(content_only)} chunks.")
        embeddings = self.embedder.encode(content_only)

        metadatas = [{'chunk': i, 'filename': chunk[0]} for i, chunk in enumerate(chunks)]
        
        try:
            logger.info("Opening database connection for storing processed document.")
            self.db.open_db()
            self.db.add_objects(content_only, embeddings, metadatas)
            logger.info("Document has been successfully processed and stored.")
            return {"message": "Document has been successfully processed."}
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise
        finally:
            self.db.close_db()
            logger.debug("Database connection closed after processing file.")

    def answer_question(self, question):
        """
        Answer a question using the LLM model and the vector store.
        """
        logger.info(f"Answering question: {question}")
        
        try:
            logger.info("Encoding question for similarity search.")
            question_embedding = self.embedder.encode([question])[0]
            logger.info("Opening database connection for similarity search.")
            self.db.open_db()
            
            logger.debug("Searching for similar content in the vector store.")
            similar_contents = self.db.search(question_embedding, question)
            logger.info(f"Retrieved {len(similar_contents)} similar contents for context.")

            context = ' '.join(similar_contents)
            logger.debug(f"Generated context for question: {context[:200]}...")  # Log only the first 200 characters
            answer = self.llm.generate_response(question, context)
            logger.info("Answer generated successfully.")
            return answer
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
        finally:
            self.db.close_db()
            logger.debug("Database connection closed after answering question.")
