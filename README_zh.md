# GEM_model 启动版

此启动版仅包含运行所需代码与已构建的 ChromaDB 向量库，训练/建库脚本和原始歌词数据已移除。

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

## 配置

在 `main.py` 中可修改：

- `DB_PATH`（默认 `storage/chroma_db_smart`）
- `EMBED_MODEL`（默认 `BAAI/bge-m3`）
- `LLM_MODEL`（默认 `qwen3:8b`，通过 Ollama）
- `TOP_K`（检索候选数量）

默认集合名为 `gem_lyrics_smart`。

## 目录结构

- `main.py` 核心逻辑
- `storage/` 预构建的 ChromaDB 向量库
