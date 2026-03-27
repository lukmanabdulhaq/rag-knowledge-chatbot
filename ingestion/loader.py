# ingestion/loader.py
import os
from pathlib import Path
from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document


def load_documents(source_dir: str, recursive: bool = True) -> List[Document]:
    """
    Load PDF, DOCX, TXT, and MD files from a directory.
    Returns a list of LlamaIndex Document objects.
    """
    source_path = Path(source_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    reader = SimpleDirectoryReader(
        input_dir=str(source_path),
        recursive=recursive,
        required_exts=[".pdf", ".docx", ".txt", ".md"],
        filename_as_id=True,
    )

    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} document(s) from {source_dir}")
    return documents


def load_from_files(file_paths: List[str]) -> List[Document]:
    """
    Load specific files by path.
    """
    reader = SimpleDirectoryReader(
        input_files=file_paths,
        filename_as_id=True,
    )
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} document(s) from file list")
    return documents
