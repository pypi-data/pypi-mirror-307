import unittest
from unittest.mock import patch, MagicMock
from arm_rag.document_processing.parser import Document_parser

# FILE: arm_rag/document_processing/test_parser.py


class TestDocumentParser(unittest.TestCase):

    def setUp(self):
        self.parser = Document_parser()

    @patch('arm_rag.document_processing.parser.Document_parser.read_pdf')
    @patch('arm_rag.document_processing.parser.Document_parser.read_tables')
    def test_parse_file_pdf(self, mock_read_tables, mock_read_pdf):
        mock_read_pdf.return_value = "PDF content"
        mock_read_tables.return_value = ["Table content"]
        content, tables = self.parser.parse_file("test.pdf")
        self.assertEqual(content, "PDF content")
        self.assertEqual(tables, ["Table content"])
        mock_read_pdf.assert_called_once_with("test.pdf")
        mock_read_tables.assert_called_once_with("test.pdf")

    @patch('arm_rag.document_processing.parser.Document_parser.read_txt')
    def test_parse_file_txt(self, mock_read_txt):
        mock_read_txt.return_value = "TXT content"
        content = self.parser.parse_file("test.txt")
        self.assertEqual(content, "TXT content")
        mock_read_txt.assert_called_once_with("test.txt")

    @patch('arm_rag.document_processing.parser.Document_parser.read_doc')
    def test_parse_file_doc(self, mock_read_doc):
        mock_read_doc.return_value = "DOC content"
        content = self.parser.parse_file("test.doc")
        self.assertEqual(content, "DOC content")
        mock_read_doc.assert_called_once_with("test.doc")

    @patch('arm_rag.document_processing.parser.Document_parser.read_docx')
    def test_parse_file_docx(self, mock_read_docx):
        mock_read_docx.return_value = "DOCX content"
        content = self.parser.parse_file("test.docx")
        self.assertEqual(content, "DOCX content")
        mock_read_docx.assert_called_once_with("test.docx")

    def test_parse_file_unsupported(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse_file("test.unsupported")
        self.assertEqual(str(context.exception), "The file type is not supported. Please upload only .pdf, .doc, .docx, .txt.")

if __name__ == '__main__':
    unittest.main()