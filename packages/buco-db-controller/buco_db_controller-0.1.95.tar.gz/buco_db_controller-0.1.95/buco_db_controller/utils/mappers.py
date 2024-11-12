import logging
from fuzzywuzzy import process
import rapidfuzz as rapid_fuzz


def find_fuzzy_item(
        input_word,
        search_array,
        threshold=80,
        msg="",
        exception=True,
        rapid=False
):
    # Use the built-in 'process' function to find the closest match
    search_array = list(set(search_array))

    if rapid:
        best_match = rapid_fuzz.process.extractOne(input_word, search_array)
    else:
        best_match = process.extractOne(input_word, search_array)
    confidence = best_match[1]

    if confidence < 70:
        logging.warning(
            f'Suspicious threshold | '
            f'Input word: {input_word} |'
            f'Closest word: {best_match[0]} | '
            f'Threshold {confidence} ~ ({threshold}) | '
            f'Options: {search_array[:20]} \n {msg}')

    if confidence <= threshold:
        if exception:
            raise ValueError(
                f'Input word: {input_word} |'
                f'Closest word: {best_match[0]} | '
                f'{confidence} was less than threshold ({threshold}) | '
                f'{input_word} not found in {search_array} \n {msg}')
        else:
            return None
    return best_match[0]
