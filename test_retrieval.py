import chromadb
from app.ingestion.embedder import RuleEmbedder

c = chromadb.PersistentClient(path='data/chroma')
col = c.get_or_create_collection('college_rules')

embedder = RuleEmbedder()
q = embedder.embed('minimum attendance required end semester exam')

results = col.query(
    query_embeddings=[q],
    n_results=3,
    include=['documents', 'metadatas', 'distances']
)

for i, doc in enumerate(results['documents'][0]):
    print('---')
    print('distance:', results['distances'][0][i])
    print('similarity:', 1 - results['distances'][0][i])
    print('text:', doc[:150])