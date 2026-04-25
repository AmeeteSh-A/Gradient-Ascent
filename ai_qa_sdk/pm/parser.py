import PyPDF2
import pandas as pd
from io import BytesIO

class DocumentParser:
    """Handles data ingestion and pre-processing for the PM Agent."""

    @staticmethod
    def _extract_raw(uploaded_file) -> str:
        """Extracts raw text based on file type."""
        t = uploaded_file.type
        
        try:
            if t == "text/plain" or t == "text/markdown":
                return uploaded_file.read().decode("utf-8")
                
            if t == "application/pdf":
                reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                return "\n".join([p.extract_text() or "" for p in reader.pages])
                
            if t == "text/csv":
                df = pd.read_csv(uploaded_file)
                return df.to_markdown()
                
            raise ValueError(f"Unsupported file type: {t}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to parse file: {e}")

    @staticmethod
    def _inject_traceability_tags(raw_text: str) -> str:
        """
        Splits text into paragraphs and prepends [REF-ID] tags.
        This is the secret sauce for the UI traceability matrix.
        """
        # Split by newlines and filter out empty strings
        paragraphs = [p.strip() for p in raw_text.split('\n') if p.strip()]
        
        tagged_text = ""
        for index, paragraph in enumerate(paragraphs, start=1):
            # E.g., "[REF-1] The system must handle 5000 concurrent users."
            tagged_text += f"[REF-{index}] {paragraph}\n\n"
            
        return tagged_text

    @classmethod
    def parse_and_tag(cls, uploaded_file) -> str:
        """The main entry point for the Streamlit UI to call."""
        raw_text = cls._extract_raw(uploaded_file)
        tagged_text = cls._inject_traceability_tags(raw_text)
        return tagged_text