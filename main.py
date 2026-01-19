import chromadb
import ollama
from sentence_transformers import SentenceTransformer
from pathlib import Path
import re

# 配置
PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = str(PROJECT_ROOT / "storage" / "chroma_db_smart")
EMBED_MODEL = "BAAI/bge-m3"
LLM_MODEL = "qwen3:8b"
TOP_K = 10 

class GEMBot:
    def __init__(self):
        print("⏳ 正在初始化 G.E.M. 邓紫棋...")
        self.embed_model = SentenceTransformer(EMBED_MODEL, device='cpu')
        self.db_client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.db_client.get_collection("gem_lyrics_smart")
        print("✅ 初始化完成！")

    def search_lyrics(self, query_text):
        query_vec = self.embed_model.encode([query_text]).tolist()
        results = self.collection.query(
            query_embeddings=query_vec,
            n_results=TOP_K
        )
        
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        filtered_candidates = []
        
        for i, doc in enumerate(documents):
            if len(doc) < 4: continue
            if doc.strip() == query_text.strip(): continue
            
            song_name = metadatas[i]['song']
            filtered_candidates.append(f"【选项{len(filtered_candidates)+1}】: {doc}")
            if len(filtered_candidates) >= 6: break
        
        return filtered_candidates

    def clean_output(self, text):
        """
        使用 '||' 分隔输出，并清洗标点与空白。
        """
        # 预处理：去掉换行符
        text = text.replace("\n", " ")
        
        # 按 || 切割
        if "||" in text:
            parts = text.split("||")
        else:
            # 没有 || 时，尝试按空格切（偏中文）；若像英文则返回原句
            if text.count(" ") > 3: # 英文句子空格通常很多
                return text.strip()
            parts = text.split()

        # 清洗每个部分（去标点、去首尾空格）
        cleaned_parts = []
        for p in parts:
            # 只去掉标点，保留单词间的空格
            # 注意：不能简单 replace(" ", "")，那样会把英文连在一起
            p = re.sub(r"[，。！？、…~,.!?]", " ", p).strip()
            if p:
                cleaned_parts.append(p)
        
        # 只取前两句，并用空格重新拼合
        if len(cleaned_parts) >= 2:
            return " ".join(cleaned_parts[:2])
        elif len(cleaned_parts) == 1:
            return cleaned_parts[0]
        else:
            return text # 兜底

    def generate_response(self, user_input, candidates):
        candidate_str = "\n".join(candidates)
        
        # Prompt：强制使用 || 分隔
        system_prompt = f"""
        你现在是歌手邓紫棋（G.E.M.）。
        
        【任务】
        从下方【候选歌词】中，挑选**最能回应用户**的一段内容。
        
        【严格格式要求 - 必须遵守】
        1. **只输出两句歌词**。
        2. **使用双竖线分隔**：两句歌词之间必须用 '||' 隔开。
        3. **保留原文**：如果是英文歌词，保留单词间的空格，不要截断。
        4. **去除标点**：不要输出逗号、句号等标点。
        
        【示例】
        用户：我们分手吧
        正确输出：可惜我们终于来到 || 一个句号
        
        用户：来点High的
        正确输出：Give me a G || Give me a E
        
        【候选歌词】
        {candidate_str}
        
        请直接输出最终结果：
        """

        try:
            response = ollama.chat(model=LLM_MODEL, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"用户说：{user_input}"},
            ])
            
            raw_content = response['message']['content']
            return self.clean_output(raw_content)
            
        except Exception as e:
            return "..."

    def chat(self):
        print("🎤 请开始对话 (V3.1):")
        while True:
            try:
                user_input = input("\n👤 你: ").strip()
                if user_input.lower() in ['exit', 'quit', '退出']:
                    break
                if not user_input: continue

                candidates = self.search_lyrics(user_input)
                print("Thinking...", end="\r")
                reply = self.generate_response(user_input, candidates)
                print(f"🎵 G.E.M.: {reply}")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    bot = GEMBot()
    bot.chat()
