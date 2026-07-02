from app.services.vector.vector_store import VectorStore

vector_store = VectorStore()


def get_vector_store():
    return vector_store