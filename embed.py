from sentence_transformers import SentenceTransformer
import chromadb
from collections import defaultdict
from splitter import get_chunks
from langchain_community.document_loaders import TextLoader
import uuid

# =============================
# 모델 로드
# =============================
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# =============================
# 문서 로드 + 청크 분리
# =============================
loader = TextLoader("data.txt", encoding="utf-8")
documents = loader.load()

chunks = get_chunks(documents) #, strategy="basic"

print("총 청크 수:", len(chunks))

# =============================
# ID & 메타데이터 정리
# =============================
ids = []
contents = []
metadatas = []
anchor_map = defaultdict(list)

for i, chunk in enumerate(chunks):

    # 앵커는 기존 anchor_id 사용
    if "id" in chunk.metadata:
        chunk_id = chunk.metadata["id"]
    else:
        chunk_id = f"chunk_{i}"

    ids.append(chunk_id)

    contents.append(chunk.page_content)

    # parent_id가 metadata에 있으면 child
    parent_id = chunk.metadata.get("parent_id")

    if parent_id:
        metadatas.append({
            "type": "child",
            "parent_id": parent_id
        })
        anchor_map[parent_id].append(chunk_id)
    else:
        metadatas.append({
            "type": "anchor"
        })

# =============================
# 임베딩
# =============================
embeddings = model.encode(contents, normalize_embeddings=True)

# =============================
# Chroma 저장
# =============================
client = chromadb.Client()

try:
    client.delete_collection("chunks_docs")
except:
    pass

collection = client.create_collection(name="chunks_docs")
collection.add(
    documents=contents,
    embeddings=embeddings.tolist(),
    ids=ids,
    metadatas=metadatas
)

print("DB 문서 수:", collection.count())


# =============================
# 검색 함수
# =============================
def search(query: str, k_anchor: int = 1, k_chunk: int = 5):

    query_embedding = model.encode([query], normalize_embeddings=True)

    # 1️⃣ 앵커 검색
    anchor_results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=k_anchor,
        where={"type": "anchor"}
    )

    if not anchor_results["ids"][0]:
        return []

    anchor_id = anchor_results["ids"][0][0]
    best_distance = anchor_results["distances"][0][0]

    print("Top Anchor:", anchor_id)
    print("Distance:", best_distance)

    # 2️⃣ 해당 앵커의 child 찾기
    child_ids = anchor_map.get(anchor_id, [])

    if best_distance <= 0.8 and child_ids:
        chunk_results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=k_chunk,
            ids=child_ids
        )
        return chunk_results["documents"][0]

    # 3️⃣ fallback
    fallback_results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3,
        where={"type": "child"}
    )
    return fallback_results["documents"][0]


# 테스트
if __name__ == "__main__":
    print(search("RAG란 무엇인가요?"))
