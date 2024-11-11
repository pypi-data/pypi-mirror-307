import os
import sqlite3
import numpy as np
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class VectorNest:
    def __init__(self) -> None:
        """
        Initializes the VectorNest class, creating a pandas DataFrame csv file if it doesn't exist.
        """
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.db_connection = None
        self.db_cursor = None
        self.db_name = None
        self.db_path = None
        
    def create_database(self, db_name: str, mode: str = 'append') -> None:
        """
        Creates a SQLite database file.

        :param db_name: The name of the database file (without extension).
        :param mode: 'overwrite' to replace an existing database or 'append' to keep it.
        """
        db_path = self.get_database_path(db_name)
        
        if mode == 'overwrite' and os.path.exists(db_path):
            os.remove(db_path)
            print(f"Database '{db_name}' has been overwritten.")
        
        if not os.path.exists("nests"):
            os.mkdir("nests")
        
        # Create or connect to the database
        with sqlite3.connect(db_path) as conn:
            print(f"Created or opened database: {db_name}")
        
        self.db_path = db_path
        self.db_name = db_name

    def get_database_path(self, db_name: str) -> str:
        # Ensure .db extension is added
        return f"nests/{db_name}.db"

    def use_database(self, db_name: str) -> None:
        """
        Connects to the SQLite database.
        """
        self.db_connection = sqlite3.connect(self.get_database_path(db_name))
        self.db_cursor = self.db_connection.cursor()

    def create_collection(self, collection: str, mode: str = 'append') -> str:
        """
        Creates a collection in the SQLite database.

        :param collection: The name of the collection.
        :param mode: 'overwrite' to delete an existing collection or 'append' to keep it if it exists.
        :return: The name of the collection.
        :raises ValueError: If the collection already exists and mode is 'append'.
        """
        collection_table = self.get_collection_table(collection)
        
        if mode == 'overwrite':
            self.db_cursor.execute(f"DROP TABLE IF EXISTS {collection_table}")
            print(f"Old collection '{collection}' has been deleted.")
        
        # Create a table for the collection if it doesn't exist
        self.db_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {collection_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                metadata TEXT,
                embedding BLOB
            )
        """)
        self.db_connection.commit()
        print(f"Collection '{collection}' has been created.")
        
        return collection

    def get_collection_table(self, collection: str) -> str:
        return f"collection_{collection}"

    def collection_exists(self, collection: str) -> bool:
        collection_table = self.get_collection_table(collection)
        self.db_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{collection_table}';")
        return self.db_cursor.fetchone() is not None

    def generate_embeddings(self, text: str) -> np.ndarray:
        """
        Generates embeddings from text using sentence transformers.

        :param text: The input text to generate embeddings for.
        :return: The embeddings as a NumPy array.
        """
        return self.model.encode(text, convert_to_numpy=True)

    def add_to_collection(self, collection: str, text: str, metadata: Dict[str, str]) -> None:
        """
        Adds a row to the collection with a unique ID, text, and metadata.
        If new metadata keys are introduced, new columns are created.

        :param collection: The name of the collection.
        :param text: The input text to store.
        :param metadata: The metadata as a dictionary.
        :raises ValueError: If the collection does not exist.
        """
        collection_table = self.get_collection_table(collection)
        
        if not self.collection_exists(collection):
            raise ValueError(f"Collection '{collection}' does not exist.")
        
        # Generate embeddings for the text
        embedding = self.generate_embeddings(text)
        
        # Store metadata as a string (JSON format or simple string)
        metadata_str = str(metadata)
        
        # Insert data into the collection table
        self.db_cursor.execute(f"""
            INSERT INTO {collection_table} (text, metadata, embedding)
            VALUES (?, ?, ?)
        """, (text, metadata_str, embedding.tobytes()))
        self.db_connection.commit()

    def calculate_cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculates cosine similarity between two vectors.

        :param vec1: First vector.
        :param vec2: Second vector.
        :return: Cosine similarity score between 0 and 1.
        """
        similarity = cosine_similarity([vec1], [vec2])[0][0]
        return float(similarity)  # Ensuring the result is a float

    def retrieve_from_collection(self, collection: str, query_text: str, filters: Optional[Dict[str, str]] = None, top_n: int = 5, threshold: float = 0.5) -> List[Dict[str, str]]:
        """
        Retrieves entries from a specified collection based on cosine similarity, optional filters, and an optional similarity threshold.

        :param collection: The name of the collection to query.
        :param query_text: The input text for comparison.
        :param filters: Dictionary of filter conditions (metadata fields and values).
        :param top_n: Number of top similar entries to retrieve.
        :param threshold: Similarity score threshold. Entries below this score will be excluded.
        :return: List of dictionaries where each dictionary contains 'text', 'metadata', and 'similarity' for matching entries.
        :raises ValueError: If the collection does not exist.
        """
        collection_table = self.get_collection_table(collection)
        
        if not self.collection_exists(collection):
            raise ValueError(f"Collection '{collection}' does not exist.")
        
        # Generate embedding for the query
        query_embedding = self.generate_embeddings(query_text)
        
        # Prepare the SQL query with filters
        filter_conditions = []
        filter_values = []
        if filters:
            for key, value in filters.items():
                filter_conditions.append(f"metadata LIKE ?")
                filter_values.append(f"%{value}%")
        
        filter_sql = " AND ".join(filter_conditions) if filter_conditions else "1"  # '1' is a placeholder that always evaluates to True
        sql_query = f"SELECT id, text, metadata, embedding FROM {collection_table} WHERE {filter_sql}"

        # Query the collection
        self.db_cursor.execute(sql_query, filter_values)
        rows = self.db_cursor.fetchall()
        
        # Calculate cosine similarity for each entry
        similarities = []
        for row in rows:
            embedding = np.frombuffer(row[3], dtype=np.float32)  # Convert binary back to NumPy array
            similarity = self.calculate_cosine_similarity(query_embedding, embedding)
            
            # Only include entries above the threshold
            if similarity >= threshold:
                similarities.append((row[1], row[2], similarity))  # text, metadata, similarity
        
        # Sort by similarity and get top_n results
        similarities.sort(key=lambda x: x[2], reverse=True)
        top_results = similarities[:top_n]
        
        # Format the result as a list of dictionaries
        retrieved = [{"text": text, "metadata": metadata, "similarity": similarity} for text, metadata, similarity in top_results]
        
        return retrieved

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        if self.db_connection:
            self.db_connection.close()