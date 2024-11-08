# textutils/utils.py

def count_words(text):
    """Count the number of words in a text string."""
    return len(text.split())

def count_characters(text):
    """Count the number of characters in a text string, excluding spaces."""
    return len(text.replace(" ", ""))

def reverse_text(text):
    """Return the reversed version of a text string."""
    return text[::-1]
