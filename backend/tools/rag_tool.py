import os
from langchain.tools import tool

VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), "../vectorstore")
MANUALS_PATH = os.path.join(os.path.dirname(__file__), "../data/manuals")

# ── Lazy singletons (heavy imports deferred to first use) ─────────────────────
_embedder = None
_chroma_client = None
_collection = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def _get_collection():
    global _chroma_client, _collection
    if _collection is None:
        import chromadb  # noqa: PLC0415
        os.makedirs(VECTORSTORE_PATH, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=VECTORSTORE_PATH)
        _collection = _chroma_client.get_or_create_collection("vehicle_manuals")
    return _collection


# ── Manual ingestion ──────────────────────────────────────────────────────────

def ingest_manual(pdf_path: str, vehicle_name: str):
    """Ingest a single PDF manual into ChromaDB vector store."""
    import fitz  # PyMuPDF  # noqa: PLC0415

    embedder = _get_embedder()
    collection = _get_collection()

    doc = fitz.open(pdf_path)
    chunks, ids, metadatas = [], [], []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < 50:
            continue
        # Chunk with slight overlap for better context
        for i in range(0, len(text), 450):
            chunk = text[i : i + 500].strip()
            if len(chunk) > 50:
                chunk_id = f"{vehicle_name}_p{page_num}_c{i}"
                chunks.append(chunk)
                ids.append(chunk_id)
                metadatas.append({"vehicle": vehicle_name, "page": page_num + 1})

    if chunks:
        embeddings = embedder.encode(chunks).tolist()
        collection.upsert(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )
        print(f"✅ Ingested {len(chunks)} chunks from '{vehicle_name}'")
    doc.close()


def ingest_all_manuals():
    """Scan manuals/ directory and ingest any new PDFs."""
    os.makedirs(MANUALS_PATH, exist_ok=True)
    pdfs = [f for f in os.listdir(MANUALS_PATH) if f.lower().endswith(".pdf")]
    if not pdfs:
        print("ℹ️  No PDFs found in data/manuals/ — RAG will use LLM knowledge only.")
        return
    for filename in pdfs:
        vehicle_name = os.path.splitext(filename)[0]
        ingest_manual(os.path.join(MANUALS_PATH, filename), vehicle_name)


# ── LangChain Tool ────────────────────────────────────────────────────────────

@tool
def vehicle_manual_rag(query: str) -> str:
    """
    Search indexed vehicle service manuals for repair steps, torque specs,
    fluid capacities, and technical procedures. Returns top relevant passages.
    """
    try:
        embedder = _get_embedder()
        collection = _get_collection()

        query_embedding = embedder.encode([query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            return (
                "📚 No relevant information found in indexed manuals. "
                "Drop PDF service manuals into backend/data/manuals/ and restart the server to enable this feature."
            )

        response = "📖 From Vehicle Service Manuals:\n\n"
        for doc, meta in zip(docs, metas):
            vehicle = meta.get("vehicle", "Unknown Vehicle")
            page = meta.get("page", "?")
            response += f"[{vehicle} — Page {page}]\n{doc}\n\n"

        return response.strip()

    except Exception as e:
        return f"📚 Manual search unavailable: {str(e)}. The RAG tool will use LLM knowledge instead."
