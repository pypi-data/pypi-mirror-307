import abc
import os.path
from collections import defaultdict
from pathlib import Path

from .consts import DATA_DIR, ECODING
from .utils import split_text_by_words, make_moving_windows


class Document:
    pass


class SearchResult:
    pass


class SimilarTextsByExactWordsMatch(SearchResult):
    def __init__(self, plagiarism_percentage: float, docs_similarity: list[tuple[int, float]]):
        self.plagiarism_percentage: float = plagiarism_percentage
        self.docs_similarity: list[tuple[int, float]] = docs_similarity


class ABCDatabase(abc.ABC):
    @abc.abstractmethod
    def add_text(self, text: str) -> int:
        pass

    @abc.abstractmethod
    def search_similar_texts_by_distance(self, id, threshold: float = 0.9) -> list[SearchResult]:
        """
        Cosine similarity (Bag of words)
        """
        pass

    @abc.abstractmethod
    def search_similar_texts_by_exact_words_match(self, id, threshold: float = 0.9) -> list[SearchResult]:
        """
        Cosine similarity (Bag of words)
        """
        pass


class InMemoryDocument:
    def __init__(self, _id: int, text: str):
        self.text = text
        self.id = _id

        self.words = split_text_by_words(text)
        self.words_in_moving_window = make_moving_windows(self.words)
        self.plagiarized_words = [[w, False, set()] for w in self.words]


def save_document_to_folder(document: InMemoryDocument):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{document.id}.txt")

    with open(file_path, "w", encoding=ECODING) as f:
        f.write(document.text)

    return file_path


class InMemoryDatabase(ABCDatabase):
    def __init__(self, datadir=DATA_DIR):
        self.current_index = 0
        self.data: dict[int, str] = {}

        self.window_words: dict[tuple[str]: list[InMemoryDocument]] = defaultdict(list)
        if datadir is not None:
            initialize_database(self, datadir)

    def add_text(self, text: str, save_document=True, custom_index=None) -> InMemoryDocument:
        if custom_index is None:
            index = self.current_index
            self.current_index += 1
        else:
            index = custom_index
            self.current_index = max(custom_index + 1, self.current_index + 1)

        document = InMemoryDocument(index, text)
        if save_document:
            save_document_to_folder(document)

        if index in self.data:
            raise ValueError("This index was already used")
        self.data[index] = InMemoryDocument(index, text)

        for window in document.words_in_moving_window:
            key = self.get_key_from_window(window)
            self.window_words[key].append(document)

        return document

    @staticmethod
    def get_key_from_window(window):
        key = [w.lower() for w, s, e in window]
        key = tuple(key)
        return key

    def search_similar_texts_by_distance(self, id, threshold: float = 0.9) -> list[SearchResult]:
        pass

    def search_similar_texts_by_exact_words_match(self, id, threshold: float = 0.9) -> list[
        SimilarTextsByExactWordsMatch]:
        document: InMemoryDocument = self.data[id]

        # шукаємо подібні
        similar_ids: set[int] = set()
        for index, window in enumerate(document.words_in_moving_window):
            key = self.get_key_from_window(window)
            list_of_documents = self.window_words[key]
            list_of_documents_ids: set = {doc.id for doc in list_of_documents}
            list_of_documents_ids -= {document.id}

            similar_ids |= set(list_of_documents_ids)

            if not list_of_documents_ids:
                continue

            # TODO: add document mutation
            for word_index, word in enumerate(window):
                document.plagiarized_words[index + word_index][1] = True
                document.plagiarized_words[index + word_index][2] |= list_of_documents_ids

        all_words = len(document.words)
        plagiarized_words = len([word_info[1] for word_info in document.plagiarized_words if word_info[1]])
        plagiarized_metric = plagiarized_words / all_words

        return plagiarized_metric


def initialize_database(db: InMemoryDatabase, datadir: str):
    file_path: Path = None
    for file_path in Path(datadir).iterdir():
        index = int(file_path.stem)

        with open(file_path, 'r', encoding=ECODING) as f:
            info = f.read()

            db.add_text(info, save_document=False, custom_index=index)


if __name__ == '__main__':
    dataset = [
        "aa bb cc dd ee",
        "tt yy uu ii this is not plagiarized text qq ww ee"
    ]

    db = InMemoryDatabase()
    for text in dataset:
        db.add_text(text)

    text_for_check = "This  iS  nOt  PlaGiaRized text pp ll qq aa bb cc dd =)"
    document = db.add_text(text_for_check)

    result = db.search_similar_texts_by_exact_words_match(document.id)
    print(result)
