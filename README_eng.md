# GEM_model (Launch Version)

This launch version includes only runtime code and a prebuilt ChromaDB index.
Training/build scripts and raw lyric files are intentionally excluded.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

## Configuration

Edit `main.py` to change:

- `DB_PATH` (default `storage/chroma_db_smart`)
- `EMBED_MODEL` (default `BAAI/bge-m3`)
- `LLM_MODEL` (default `qwen3:8b` via Ollama)
- `TOP_K` (retrieval candidates)

The default collection name is `gem_lyrics_smart`.

## Folder structure

- `main.py` Core logic
- `storage/` Prebuilt ChromaDB index
