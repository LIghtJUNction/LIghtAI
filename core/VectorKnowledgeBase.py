import pandas as pd
import numpy as np
import faiss
import ollama
from . import EmbeddingModel

class VectorKnowledgeBase:
    def __init__(self, data=None):
        self.data = data if data is not None else pd.DataFrame(columns=['id', 'text'])
        self.embeddings = None
        self.index = None
    
    def add_data(self, data):
        """添加新数据到知识库"""
        self.data = pd.concat([self.data, data], ignore_index=True)
    
    def generate_embeddings(self):
        """生成文档嵌入向量"""
        if not self.data.empty:
            texts = self.data['text'].tolist()
            embeddings = []
            for text in texts:
                # 假设 ollama.embeddings 返回 {'text': [embedding]}
                result = ollama.embeddings(model=self.model_name, prompt=text)
                embeddings.append(result['text'])
            self.embeddings = np.array(embeddings)
        else:
            raise ValueError("数据为空，请添加数据后再生成嵌入")
    
    def create_index(self):
        """创建向量索引"""
        if self.embeddings is not None:
            d = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(d)
            self.index.add(np.array(self.embeddings))
        else:
            raise ValueError("嵌入为空，请生成嵌入后再创建索引")
    
    def save_index(self, filepath):
        """保存向量索引到文件"""
        if self.index is not None:
            faiss.write_index(self.index, filepath)
        else:
            raise ValueError("索引为空，请创建索引后再保存")
    
    def load_index(self, filepath):
        """从文件加载向量索引"""
        self.index = faiss.read_index(filepath)
    
    def query(self, query_text, k=3):
        """查询最相似的文本"""
        if self.index is not None:
            query_embedding = ollama.embeddings(EmbeddingModel,[query_text])[0]
            D, I = self.index.search(np.array([query_embedding]), k)
            results = self.data.iloc[I[0]]['text'].tolist()
            return results
        else:
            raise ValueError("索引为空，请创建或加载索引后再查询")

# 使用示例
if __name__ == "__main__":
    # 示例数据
    data = pd.DataFrame({
        'id': [1, 2, 3],
        'text': ["This is the first document.", "This document is the second document.", "And this is the third one."]
    })

    # 创建知识库对象
    kb = VectorKnowledgeBase(data)

    # 生成嵌入并创建索引
    kb.generate_embeddings()
    kb.create_index()

    # 保存索引
    kb.save_index("vector_database.index")

    # 加载索引
    kb.load_index("vector_database.index")

    # 查询
    query_results = kb.query("This is a new document to query.")
    print("Query Results:", query_results)
