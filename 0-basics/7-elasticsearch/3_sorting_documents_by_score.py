from elasticsearch import Elasticsearch, ElasticsearchWarning
import random
import warnings

es = Elasticsearch("http://localhost:9200")
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

# Define index mappings
indices = {
    "books": {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "author": {"type": "text"},
                "published_year": {"type": "integer"},
                "genre": {"type": "keyword"},
                "rating": {"type": "float"}
            }
        }
    },
    "reviews": {
        "mappings": {
            "properties": {
                "book_id": {"type": "keyword"},  # Links to books index
                "reviewer": {"type": "text"},
                "rating": {"type": "float"},
                "review": {"type": "text"},
                "date": {"type": "date"}
            }
        }
    }
}

# Create indices if they don't exist
for index, body in indices.items():
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=body)
        print(f"Index '{index}' created.")
    else:
        print(f"Index '{index}' already exists.")

# Sample data for 50 books
genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Biography", "History"]
authors = ["Author A", "Author B", "Author C", "Author D", "Author E"]

for i in range(1, 51):  # Inserting 50 books
    book = {
        "title": f"Book {random.randint(1000, 100000)}",
        "author": random.choice(authors),
        "published_year": random.randint(1950, 2025),
        "genre": random.choice(genres),
        "rating": round(random.uniform(1, 5), 1)
    }

    # Use PUT API with a specific ID
    es.index(index="books", id=str(i), body=book)


# Search for books with a specific title
search_title = "Book"  # Change this to your search term

query = {
    "query": {
        "match": {
            "title": search_title  # Search for books with this title
        },
    },
    "size": 10,  # Retrieve 50 books
    "sort": [
        {"_score": {"order": "desc"}}
    ]
}

response = es.search(index="books", body=query)

# Print search results
for hit in response["hits"]["hits"]:
    print(f"ID: {hit['_id']}, Title: {hit['_source']['title']}, Author: {hit['_source']['author']}")




