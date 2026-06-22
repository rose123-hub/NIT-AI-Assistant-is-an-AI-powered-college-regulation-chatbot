import asyncio
from sqlalchemy import text

from app.ingestion.ingestor import ingest_pdf
from app.ingestion.embedder import RuleEmbedder
from app.db.session import engine, SessionLocal
from app.db.models import Base
from app.dependencies import get_chroma_collection


Base.metadata.create_all(bind=engine)


async def run_test():

    db = SessionLocal()
    collection = get_chroma_collection()

    pdf_path = "data/uploads/ordinances-and-regulations-2023.pdf"

    await ingest_pdf(
        pdf_path=pdf_path,
        document_name="Test Document",
        effective_date="2023-01-01",
        version="v1",
        db=db,
        chroma_collection=collection
    )

    print("\n✅ INGESTION DONE")

    docs = db.execute(text("SELECT COUNT(*) FROM documents")).fetchone()
    rules = db.execute(text("SELECT COUNT(*) FROM rules")).fetchone()

    print("Documents:", docs[0])
    print("Rules:", rules[0])

    embedder = RuleEmbedder()
    q_emb = embedder.embed("attendance")

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    print("\n🔎 CHROMA RESULTS:")
    print(results["documents"][0])


if __name__ == "__main__":
    asyncio.run(run_test())