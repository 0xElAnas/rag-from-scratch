from PyPDF2 import PdfReader

class PDFParser:        
    def parse(self, file_path: str) -> list[dict]:
        reader = PdfReader(file_path)
        text_data = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text_data.append({
                "page_number": page_num,
                "text": text
            })
        return text_data