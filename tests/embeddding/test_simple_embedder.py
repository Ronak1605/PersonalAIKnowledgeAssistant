from embedding.simple_embedder import SimpleEmbedder


def test_simple_embedder_returns_vectors():
    embedder = SimpleEmbedder()

    texts = ["hello", "world"]
    vectors = embedder.embed(texts)

    assert len(vectors) == 2
    assert all(isinstance(v, list) for v in vectors)
    assert all(isinstance(x, float) for v in vectors for x in v)