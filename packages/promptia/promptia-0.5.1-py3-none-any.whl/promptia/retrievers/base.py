"""取得処理系モジュール."""
from abc import abstractmethod


class Retriever:
    """リトリーバクラス."""

    @abstractmethod
    def query(self) -> list[str]:
        """クエリを実行する."""
        raise NotImplementedError()
