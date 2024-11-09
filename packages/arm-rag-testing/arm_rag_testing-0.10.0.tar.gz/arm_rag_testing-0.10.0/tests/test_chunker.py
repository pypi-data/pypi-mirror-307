import unittest
from arm_rag.document_processing.chunker import Chunking

# FILE: arm_rag/document_processing/test_chunking.py


class TestChunking(unittest.TestCase):

    def setUp(self):
        self.chunk_size = 5
        self.chunking = Chunking(chunk_size=self.chunk_size, type='recursive')

    def test_recursive_splitter_single_chunk(self):
        text = "This is a simple test."
        expected_chunks = ["This is a simple test."]
        chunks = self.chunking.recursive_splitter(text)
        self.assertEqual(chunks, expected_chunks)

    def test_recursive_splitter_multiple_chunks(self):
        text = "This is a simple test. This is another simple test."
        expected_chunks = ["This is a simple test.", "This is another simple test."]
        chunks = self.chunking.recursive_splitter(text)
        self.assertEqual(chunks, expected_chunks)

    def test_recursive_splitter_exact_chunk_size(self):
        text = "This is a simple test. Another test."
        expected_chunks = ["This is a simple test.", "Another test."]
        chunks = self.chunking.recursive_splitter(text)
        self.assertEqual(chunks, expected_chunks)

    def test_recursive_splitter_empty_text(self):
        text = ""
        expected_chunks = [""]
        chunks = self.chunking.recursive_splitter(text)
        self.assertEqual(chunks, expected_chunks)

if __name__ == '__main__':
    unittest.main()