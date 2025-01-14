def clean_ascii(text):
    """
    Remove Non ASCII characters from the dataset.

    Arguments:
        text: str
    """
    return "".join(i for i in text if ord(i) < 128)
