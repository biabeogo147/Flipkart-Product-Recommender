from flipkart.config import *
from langchain_astradb import AstraDBVectorStore
from flipkart.data_converter import DataConverter
from langchain_huggingface import HuggingFaceEndpointEmbeddings


class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(
            repo_id=EMBEDDING_MODEL_NAME,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )

        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name=COLLECTION_NAME,
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )

    def ingest(self, load_existing=True):
        if load_existing:
            return self.vstore
        
        docs = DataConverter("data/flipkart_product_review.csv").convert()

        self.vstore.add_documents(docs)

        return self.vstore

