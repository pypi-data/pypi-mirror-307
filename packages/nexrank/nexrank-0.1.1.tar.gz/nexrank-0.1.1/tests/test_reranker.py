from unittest.mock import Mock, patch

import pytest

from nexrank.reranker import RerankResult, StructuredReranker


@pytest.fixture
def sample_documents():
    return [
        {
            "title": "Human Rights",
            "text": "Human rights are basic rights and freedoms.",
        },
        {
            "title": "Property Rights",
            "text": "Property rights are fundamental to ownership.",
        },
    ]


@pytest.fixture
def sample_query():
    return "What are human rights?"


@pytest.fixture
def reranker():
    return StructuredReranker()


def test_initialization():
    """Test reranker initialization with default values"""
    with patch("spacy.load") as mock_spacy_load:
        mock_nlp = Mock()
        mock_spacy_load.return_value = mock_nlp

        reranker = StructuredReranker()

        assert (
            reranker.cross_encoder.model_name == "cross-encoder/ms-marco-MiniLM-L-12-v2"
        )
        assert (
            reranker.bi_encoder.model_name == "sentence-transformers/all-MiniLM-L6-v2"
        )
        assert reranker.device in ["cuda", "cpu"]


def test_preprocess_text(reranker):
    """Test text preprocessing"""
    text = "This is a TEST sentence! With punctuation?"
    processed = reranker.preprocess_text(text)

    # Check if text is lowercase and punctuation is removed
    assert "!" not in processed
    assert "?" not in processed
    assert "TEST" not in processed
    assert all(c.islower() for c in processed if c.isalpha())


def test_rerank_empty_documents(reranker, sample_query):
    """Test reranking with empty document list"""
    result = reranker.rerank(sample_query, [])
    assert result == []


def test_compute_scores(reranker):
    """Test score computation for a document"""
    query = "human rights"
    doc = {"title": "Human Rights", "text": "Basic human rights and freedoms"}

    lexical_score, semantic_score = reranker.compute_scores(query, doc)

    # Check if scores are within expected range
    assert isinstance(lexical_score, float)
    assert isinstance(semantic_score, float)
    assert lexical_score >= 0
    assert semantic_score <= 1


def test_rerank_with_scores(reranker, sample_query, sample_documents):
    """Test reranking with score return"""
    results = reranker.rerank(sample_query, sample_documents, return_scores=True)

    assert isinstance(results, list)
    assert isinstance(results[0], RerankResult)

    # Check if results are sorted by score
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_rerank_top_k(reranker, sample_query, sample_documents):
    """Test top_k parameter in reranking"""
    top_k = 1
    results = reranker.rerank(sample_query, sample_documents, top_k=top_k)

    assert len(results) == top_k


def test_rerank_result_format(reranker, sample_query, sample_documents):
    """Test the format of reranking results"""
    results = reranker.rerank(sample_query, sample_documents)

    assert isinstance(results, list)
    assert isinstance(results[0], dict)
    assert "title" in results[0]
    assert "text" in results[0]


def test_score_scaling(reranker, sample_query, sample_documents):
    """Test if scores are properly scaled"""
    results = reranker.rerank(sample_query, sample_documents, return_scores=True)

    scores = [r.score for r in results]
    # Check if scores are scaled between 0 and 1
    assert min(scores) >= 0
    assert max(scores) <= 1


def test_rerank_with_invalid_input(reranker):
    """Test handling of invalid input"""
    with pytest.raises(TypeError):
        reranker.rerank(None, [{"title": "test", "text": "test"}])

    with pytest.raises(KeyError):
        reranker.rerank("query", [{"invalid_key": "test"}])


@pytest.mark.parametrize(
    "top_k,expected_length",
    [
        (1, 1),
        (2, 2),
        (5, 2),  # Should return all documents if top_k > len(documents)
    ],
)
def test_rerank_different_top_k(
    reranker, sample_query, sample_documents, top_k, expected_length
):
    """Test reranking with different top_k values"""
    results = reranker.rerank(sample_query, sample_documents, top_k=top_k)
    assert len(results) == expected_length


def test_rerank_result_dataclass(reranker, sample_query, sample_documents):
    """Test the RerankResult dataclass functionality"""
    results = reranker.rerank(sample_query, sample_documents, return_scores=True)
    result = results[0]

    # Test all fields are present
    assert hasattr(result, "title")
    assert hasattr(result, "text")
    assert hasattr(result, "score")
    assert hasattr(result, "lexical_score")
    assert hasattr(result, "semantic_score")

    # Test to_dict method
    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)
    assert "title" in result_dict
    assert "text" in result_dict
