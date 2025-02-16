from elasticsearch import Elasticsearch, ElasticsearchWarning
from elasticsearch.exceptions import ConflictError
import warnings

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

# Sample document to be indexed
doc = {
    "title": "Optimistic Concurrency Control in Elasticsearch",
    "author": "John Doe",
    "published_year": 2025,
    "rating": 4.5
}

# Index the document (if it doesn't exist)
es.index(index="books", id=str(1), body=doc)

##################################################

# Fetch the current document to get the version
doc_id = str(1)
current_doc = es.get(index="books", id=doc_id)
current_seq_no = current_doc['_seq_no']
current_primary_term = current_doc['_primary_term']

# Define the update body
update_doc = {
    "doc": {
        "rating": 5.0  # New rating
    }
}

try:
    # Update document using seq_no and primary_term for version control
    es.update(index="books", id=doc_id, body=update_doc, if_seq_no=current_seq_no, if_primary_term=current_primary_term)
    print(f"Document {doc_id} updated successfully!")
except ConflictError as e:
    print(f"Version conflict occurred for document {doc_id}. It has been modified by someone else.")
except Exception as e:
    print(f"Error updating document: {e}")

# Simulate another update attempt (which should cause a conflict)

# Fetch the updated document to get the latest seq_no and primary_term
current_doc = es.get(index="books", id=doc_id)
updated_seq_no = current_doc['_seq_no']
updated_primary_term = current_doc['_primary_term']

try:
    # Update document again using the latest seq_no and primary_term for version control
    es.update(index="books", id=doc_id, body=update_doc, if_seq_no=updated_seq_no, if_primary_term=updated_primary_term)
    print(f"Document {doc_id} updated successfully!")
except ConflictError as e:
    print(f"Version conflict occurred for document {doc_id}. It has been modified by someone else.")
except Exception as e:
    print(f"Error updating document: {e}")
