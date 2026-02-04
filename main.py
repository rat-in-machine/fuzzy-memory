from ingest.process import create_chunks, vector_generator, ingest_db
from ingest.quijote import text


if __name__ == "__main__":
    chunks = create_chunks(text=text)

    vectors = vector_generator(chunks=chunks)

    ingest_db(vectors=vectors, chunks=chunks)