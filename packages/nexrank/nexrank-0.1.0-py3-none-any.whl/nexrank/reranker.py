from dataclasses import dataclass
from typing import Dict, List, Union

import spacy
import torch
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder, SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm


@dataclass
class RerankResult:
    title: str
    text: str
    score: float
    lexical_score: float
    semantic_score: float

    def to_dict(self) -> Dict:
        """Convert result to dictionary format."""
        return {"title": self.title, "text": self.text}


class StructuredReranker:
    def __init__(
        self,
        cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
        bi_encoder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.cross_encoder = CrossEncoder(cross_encoder_model, device=self.device)
        self.bi_encoder = SentenceTransformer(bi_encoder_model, device=self.device)

        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        self.scaler = MinMaxScaler()

    def compute_scores(self, query: str, doc: Dict[str, str]) -> tuple[float, float]:
        """Compute both lexical and semantic scores."""
        full_text = f"{doc['title']} {doc['text']}"

        # Compute lexical score
        processed_query = self.preprocess_text(query)
        processed_text = self.preprocess_text(full_text)
        query_tokens = processed_query.split()
        text_tokens = processed_text.split()
        bm25 = BM25Okapi([text_tokens])
        lexical_score = bm25.get_scores(query_tokens)[0]

        # Compute semantic score
        cross_score = self.cross_encoder.predict([(query, full_text)])
        query_embedding = self.bi_encoder.encode(query, convert_to_tensor=True)
        text_embedding = self.bi_encoder.encode(full_text, convert_to_tensor=True)
        bi_score = torch.nn.functional.cosine_similarity(
            query_embedding.unsqueeze(0), text_embedding.unsqueeze(0)
        ).item()

        semantic_score = 0.7 * float(cross_score) + 0.3 * bi_score
        return lexical_score, semantic_score

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text."""
        doc = self.nlp(text)
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct
        ]
        return " ".join(tokens)

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, str]],
        top_k: int = None,
        return_scores: bool = False,
    ) -> Union[List[Dict[str, str]], List[RerankResult]]:
        """
        Rerank documents and return in the same format as input.

        Args:
            query: Search query
            documents: List of dicts with 'title' and 'text' keys
            top_k: Number of top results to return
            return_scores: If True, return RerankResult objects with scores

        Returns:
            List of dicts in same format as input, or RerankResult objects if return_scores=True
        """
        if not documents:
            return []

        results = []
        for doc in tqdm(documents, desc="Reranking"):
            lexical_score, semantic_score = self.compute_scores(query, doc)
            final_score = 0.4 * lexical_score + 0.6 * semantic_score

            results.append(
                RerankResult(
                    title=doc["title"],
                    text=doc["text"],
                    score=final_score,
                    lexical_score=lexical_score,
                    semantic_score=semantic_score,
                )
            )

        # Sort by score
        results.sort(key=lambda x: x.score, reverse=True)

        # Scale scores
        scores = [[r.score] for r in results]
        scaled_scores = self.scaler.fit_transform(scores).flatten()
        for result, scaled_score in zip(results, scaled_scores):
            result.score = float(scaled_score)

        # Apply top_k
        if top_k:
            results = results[:top_k]

        # Return in requested format
        if return_scores:
            return results
        else:
            return [result.to_dict() for result in results]
