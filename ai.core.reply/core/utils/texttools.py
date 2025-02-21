
from typing import List

def filter_non_printable_symbols(text: str = "") -> str:
    # Remove auxiliary characters in case input is not purely Latin
    # - Control Characters: U+0000 to U+001F, U+007F to U+009F
    # - Private Use Area: U+E000 to U+F8FF
    # - Supplementary Private Use Area-A: U+F0000 to U+FFFFD
    # - Supplementary Private Use Area-B: U+100000 to U+10FFFD
    # - Tags Block: U+E0000 to U+E007F
    # - Specials Block: U+FFF0 to U+FFFF
    # - Combining Diacritical Marks: U+0300 to U+036F

    try:
        # There can be some problems with utf-8
        text = text.encode('utf-16', 'surrogatepass').decode('utf-16')
        if text.startswith('\ufeff'):
            text = text.lstrip('\ufeff')

        non_printable_pattern = re.compile(
            r'[\U00000000-\U0000001F'
            r'\U0000007F-\U0000009F'
            r'\U0000E000-\U0000F8FF'
            r'\U000F0000-\U000FFFFD'
            r'\U00100000-\U0010FFFD'
            r'\U000E0000-\U000E007F'
            r'\U0000FFF0-\U0000FFFF'
            r'\U00000300-\U0000036F'
            r']'
        )

        # Remove or replace these characters with an empty string
        return non_printable_pattern.sub('', text)
    except UnicodeEncodeError as e:
        return ""
    except UnicodeDecodeError as e:
        return ""


def retrieve_non_empty_response(generated_texts: List[str]):
    """ The function outputs either the list with chosen answer or None if all the answers are empty strings
        The function is needed in order to regenerate the responses"""
    if len(generated_texts) > 0:
        generated_text = generated_texts[0]
        return [generated_text]
    else:
        return None