# splitter.py

from langchain_core.documents import Document
import re
import uuid


def get_chunks(documents):
    """
    Anchor-Child 구조로 분리하는 함수
    """

    text = documents[0].page_content

    # 1️⃣ 줄 단위 분리
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    chunks = []
    current_anchor_id = None
    current_anchor_title = None
    buffer = []

    for line in lines:

        # 2️⃣ 제목 판단 기준 (짧고 마침표 없는 줄)
        if len(line) < 30 and not line.endswith("."):

            # 이전 anchor 저장
            if current_anchor_title:
                anchor_doc = Document(
                    page_content=current_anchor_title,
                    metadata={
                        "id": current_anchor_id
                    }
                )
                chunks.append(anchor_doc)

                # child 저장
                for paragraph in buffer:
                    child_doc = Document(
                        page_content=paragraph,
                        metadata={
                            "parent_id": current_anchor_id
                        }
                    )
                    chunks.append(child_doc)

            # 새로운 anchor 시작
            current_anchor_id = f"anchor_{uuid.uuid4().hex[:8]}"
            current_anchor_title = line
            buffer = []

        else:
            buffer.append(line)

    # 마지막 anchor 처리
    if current_anchor_title:
        anchor_doc = Document(
            page_content=current_anchor_title,
            metadata={
                "id": current_anchor_id
            }
        )
        chunks.append(anchor_doc)

        for paragraph in buffer:
            child_doc = Document(
                page_content=paragraph,
                metadata={
                    "parent_id": current_anchor_id
                }
            )
            chunks.append(child_doc)

    return chunks
