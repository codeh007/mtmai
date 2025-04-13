from datetime import datetime
from typing import Any, Iterable, Optional, Tuple
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from sqlmodel import Session, select

from mtmai.models.doc import DocumentIndex

DEFAULT_K = 4  # Number of Documents to return.
DEFAULT_FETCH_K = 20  # Number of Documents to initially fetch during MMR search.


class MtmDocStore(VectorStore):
    def __init__(
        self,
        session: Session,
        embedding: Embeddings,
    ):
        self.session = session
        self.embedding = embedding

    def search(self, query: str, category: str = None, expired_at: datetime = None):
        pass

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> list[str]:
        _texts = list(texts)
        _ids = ids or [str(uuid4()) for _ in _texts]
        _metadatas = metadatas or [{}] * len(_texts)

        # pgvector 存储
        added_ids = []
        for text, id, metadata in zip(_texts, _ids, _metadatas):
            if not text.strip():  # 跳过空文本
                continue
            try:
                embedding = self.embedding.embed_query(text)
                if isinstance(embedding, list) and len(embedding) > 0:
                    self.session.add(
                        DocumentIndex(
                            id=id,
                            embedding=embedding,
                            meta=metadata,
                            emb_model=self.embedding.__class__.__name__,
                        )
                    )
                    added_ids.append(id)
                else:
                    print(f"Warning: Empty embedding for text: {text[:50]}...")
            except Exception as e:
                print(f"Error embedding text: {text[:50]}... Error: {str(e)}")

        try:
            self.session.commit()
        except Exception as e:
            print(f"Error committing to database: {str(e)}")
            self.session.rollback()

        return added_ids

    @classmethod
    def from_texts(
        cls,
        texts: list[str],
        embedding: Embeddings,
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None,
        persist_path: Optional[str] = None,
        **kwargs: Any,
    ) -> "MtmDocStore":
        vs = MtmDocStore(embedding, persist_path=persist_path, **kwargs)
        vs.add_texts(texts, metadatas=metadatas, ids=ids)
        return vs

    def similarity_search_with_score(
        self, query: str, *, k: int = DEFAULT_K, **kwargs: Any
    ) -> list[Tuple[Document, float]]:
        query_embedding = self.embedding.embed_query(query)

        # Use pgvector's cosine similarity search
        results = self.session.exec(
            select(DocumentIndex)
            .order_by(DocumentIndex.embedding.cosine_distance(query_embedding))
            .limit(k)
        ).all()

        return [
            (
                Document(
                    page_content=result.meta.get(
                        "content", ""
                    ),  # Assuming content is stored in meta
                    metadata={"id": str(result.id), **result.meta},
                ),
                1
                - result.embedding.cosine_distance(
                    query_embedding
                ),  # Convert distance to similarity score
            )
            for result in results
        ]

    def similarity_search(
        self, query: str, k: int = DEFAULT_K, **kwargs: Any
    ) -> list[Document]:
        docs_scores = self.similarity_search_with_score(query, k=k, **kwargs)
        return [doc for doc, _ in docs_scores]
