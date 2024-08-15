from nltk_utils import tokenize, stem

def test_nltk_utils():
    test_sentence = "Hello, how are you doing today?"
    tokens = tokenize(test_sentence)
    print("Tokens:", tokens)

    test_words = ["hello", "how", "are", "you", "doing", "today"]
    stemmed_words = [stem(word) for word in test_words]
    print("Stemmed words:", stemmed_words)

if __name__ == "__main__":
    test_nltk_utils()
