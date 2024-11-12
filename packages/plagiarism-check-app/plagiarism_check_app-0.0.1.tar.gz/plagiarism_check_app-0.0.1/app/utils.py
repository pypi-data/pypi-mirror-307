import nltk

from .consts import SIZE_OF_WINDOW

nltk.download('punkt')


def split_text_by_words(text: str) -> list[tuple[str, int, int]]:
    """
    >>> split_text_by_words("aaa bbb ccc, ddd. ")
    [('aaa', 0, 3), ('bbb', 4, 7), ('ccc', 8, 11), (',', 11, 12), ('ddd', 13, 16), ('.', 16, 17)]

    :param text:
    :return:
    """
    words = nltk.word_tokenize(text)
    result = []
    start_index = 0

    for word in words:
        start_index = text.find(word, start_index)
        end_index = start_index + len(word)
        result.append((word, start_index, end_index))
        start_index = end_index  # Update start_index to continue searching

    return result


def make_moving_windows(words: list[tuple[str, int, int]], size_of_window: int = SIZE_OF_WINDOW) -> list[tuple]:
    result = []

    # Create the moving windows
    for i in range(len(words) - size_of_window + 1):
        window = tuple(words[i:i + size_of_window])
        result.append(window)

    return result


if __name__ == '__main__':
    text = "This is a sample text, and we like it."
    # print(split_text_by_words(text))
    output1 = split_text_by_words("aaa bbb ccc, ddd. ")
    print(output1)
    output2 = make_moving_windows(output1, SIZE_OF_WINDOW)
    print(output2)
