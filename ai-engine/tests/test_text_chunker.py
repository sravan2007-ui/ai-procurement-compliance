import pytest

from app.services.rag.text_chunker import TextChunker


def test_short_text_returns_one_chunk():
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)

    chunks = chunker.split("GST registration must be valid.")

    assert chunks == ["GST registration must be valid."]


def test_long_text_is_split_into_multiple_chunks():
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= 10 for chunk in chunks)


def test_chunks_overlap():
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunker.split(text)

    assert chunks[0][-2:] == chunks[1][:2]


def test_empty_text_is_rejected():
    chunker = TextChunker()

    with pytest.raises(ValueError, match="Text cannot be empty."):
        chunker.split("   ")


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(
        ValueError,
        match="Chunk size must be greater than 0.",
    ):
        TextChunker(chunk_size=0)


def test_invalid_overlap_is_rejected():
    with pytest.raises(
        ValueError,
        match="Chunk overlap cannot be negative.",
    ):
        TextChunker(chunk_overlap=-1)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(
        ValueError,
        match="Chunk overlap must be smaller than chunk size.",
    ):
        TextChunker(chunk_size=10, chunk_overlap=10)