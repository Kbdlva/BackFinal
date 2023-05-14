import re


def extract_tags(text):
    pattern = r'#\w+'  # Regular expression pattern to match tags starting with '#'
    tags = re.findall(pattern, text)
    return tags