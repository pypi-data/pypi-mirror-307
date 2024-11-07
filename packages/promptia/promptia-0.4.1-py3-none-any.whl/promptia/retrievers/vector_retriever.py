"""RAG処理を行うモジュール."""
import json
import os

from .base import Retriever


class LocalVectorProcessor:
    """ベクトルデータから対象データを抽出処理を行うクラス."""

    def __init__(self, model, distance=60) -> None:
        """コンストラクタ."""
        self.model = model
        self.distance = distance
        import faiss
        import numpy
        self.faiss = faiss
        self.np = numpy

    def query(self, query: str, max_result: int) -> list[dict[str, str]]:
        """RAGクエリを実行する."""
        embed = self.np.array([self.model.encode(query)])
        D, idx = self.index.search(embed, max_result)
        results = [{
            'Q': self.map[i]['Q'],
            'A': self.map[i]['A'],
            'distance': str(d)
        } for i, d in zip(idx[0], D[0]) if d < self.distance]
        return results

    def load_index(self, home: str, name: str) -> bool:
        """インデックスをロードする."""
        index_file = f'{home}/{name}.db'
        if not os.path.exists(index_file):
            return False
        self.index = self.faiss.read_index(index_file)
        with open(f'{home}/{name}.map', 'r') as f:
            self.map = json.load(f)
        return True

    def make_index(self, home: str, dataset: str) -> None:
        """インデックスを作成する."""
        inp = f'{home}/{dataset}'
        with open(inp, 'r') as f:
            self.map = json.load(f)

        embeds = self.np.array([self.model.encode(d['Q']) for d in self.map])
        self.index = self.faiss.IndexFlatL2(embeds.shape[1], )
        self.index.add(embeds)

    def save_index(self, home: str, name: str) -> None:
        """インデックスを保存する."""
        index_file = f'{home}/{name}.db'
        self.faiss.write_index(self.index, index_file)
        with open(f'{home}/{name}.map', 'w') as f:
            json.dump(self.map, f)


class VectorQuery(Retriever):
    """RAGクエリークラス."""

    def __init__(self, processor: LocalVectorProcessor, query: str, max_results: int = 5) -> None:
        """コンストラクタ."""
        self.processor = processor
        self.query_str = query
        self.max_results = max_results

    def query(self) -> list[str]:
        """クエリを実行する."""
        results = self.processor.query(self.query_str, self.max_results)
        return [r['A'] for r in results]
