from __future__ import annotations

import os
import sys
from typing import Optional, List

import click
from dotenv import load_dotenv

from data_loader import load_folder, load_brief
from rag_pipeline import VectorStoreManager, SEORagGenerator


@click.group()
def cli() -> None:
	"""RAG SEO Generator CLI."""
	pass


@cli.command()
@click.option("--references-dir", "references_dir", type=click.Path(exists=True, file_okay=False), required=False, help="Folder with reference SEO texts")
@click.option("--embedding-model", "embedding_model", type=str, required=False, help="HuggingFace embedding model name")
@click.option("--persist-dir", "persist_dir", type=click.Path(file_okay=False), required=False, help="ChromaDB persist directory")
def ingest(references_dir: Optional[str], embedding_model: Optional[str], persist_dir: Optional[str]) -> None:
	"""Ingest reference documents into ChromaDB."""
	load_dotenv()
	ref_dir = references_dir or os.getenv("REFERENCES_DIR", "./data/references")
	click.echo(f"Loading references from: {ref_dir}")
	refs = load_folder(ref_dir, doc_type="reference")
	click.echo(f"Found {len(refs)} reference docs")
	manager = VectorStoreManager(persist_dir=persist_dir, embedding_model=embedding_model or "sentence-transformers/all-MiniLM-L6-v2")
	count = manager.ingest(refs)
	click.echo(f"Ingested {count} documents into Chroma at {manager.persist_dir}")


@cli.command()
@click.option("--brief", "brief_path", type=click.Path(exists=True, dir_okay=False), required=True, help="Path to a brief (TZ) file")
@click.option("--top-k", "top_k", type=int, default=6, show_default=True, help="Number of similar references to retrieve")
@click.option("--temperature", "temperature", type=float, default=0.3, show_default=True, help="LLM temperature")
@click.option("--max-tokens", "max_tokens", type=int, default=3000, show_default=True, help="Max tokens for generation")
@click.option("--model", "model", type=str, required=False, help="Claude model override")
@click.option("--out", "out_path", type=click.Path(dir_okay=False), required=False, help="Optional output file path")
@click.option("--persist-dir", "persist_dir", type=click.Path(file_okay=False), required=False, help="ChromaDB persist directory")
@click.option("--embedding-model", "embedding_model", type=str, required=False, help="HuggingFace embedding model name")
def generate(brief_path: str, top_k: int, temperature: float, max_tokens: int, model: Optional[str], out_path: Optional[str], persist_dir: Optional[str], embedding_model: Optional[str]) -> None:
	"""Generate an SEO article based on a brief using retrieved similar references."""
	load_dotenv()
	brief_doc = load_brief(brief_path)
	query_text = brief_doc.page_content[:3000]

	manager = VectorStoreManager(persist_dir=persist_dir, embedding_model=embedding_model or "sentence-transformers/all-MiniLM-L6-v2")
	retrieved = manager.retrieve(query_text, top_k=top_k)
	click.echo(f"Retrieved {len(retrieved)} similar references")

	generator = SEORagGenerator(model=model)
	output = generator.generate(brief=brief_doc.page_content, references=retrieved, temperature=temperature, max_tokens=max_tokens)

	if out_path is None:
		base, _ = os.path.splitext(brief_path)
		out_path = f"{base}.seo.md"
	with open(out_path, "w", encoding="utf-8") as f:
		f.write(output)
	click.echo(f"Generated SEO article -> {out_path}")


if __name__ == "__main__":
	cli()



