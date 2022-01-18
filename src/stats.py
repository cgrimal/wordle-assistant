# Python standard lib
import re
from typing import Dict
from typing import List

# Third party
import click


def read_dictionary(filepath: str) -> List[str]:
    with open(filepath, "r") as dictionary_file:
        dictionary = dictionary_file.read().splitlines()
    return dictionary


def filter_word_length(dictionary: List[str], word_length: int) -> List[str]:
    return list(filter(lambda word: (len(word) == word_length), dictionary))


def compute_global_frequencies(dictionary: List[str]) -> Dict[str, float]:
    frequencies = dict.fromkeys(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 0.0)
    all_words = "".join(dictionary)
    total_letters = len(all_words)
    for letter in frequencies:
        frequencies[letter] = all_words.count(letter) / total_letters
    return frequencies


def compute_word_appearance_frequencies(dictionary: List[str]) -> Dict[str, float]:
    return compute_global_frequencies(
        list(map(lambda word: "".join(set(word)), dictionary))
    )


def pretty_print_frequencies(frequencies: Dict[str, float], limit: int = 26) -> None:
    for letter, frequency in sorted(
        frequencies.items(), key=lambda item: item[1], reverse=True
    )[:limit]:
        click.secho(f"{letter}: {round(frequency * 100, 2)}%")


def remove_absent_letters(dictionary: List[str], absent_letters: List[str]) -> List[str]:
    def foo(word: str) -> bool:
        for absent_letter in absent_letters:
            if absent_letter in word:
                return False
        return True
    return list(filter(foo, dictionary))


def keep_placed_letters(dictionary: List[str], reg: re) -> List[str]:
    return list(filter(lambda word: re.match(reg, word), dictionary))


def score_words(dictionary: List[str]) -> Dict[str, float]:
    scores = dict.fromkeys(dictionary, 0.0)
    word_appearance_frequencies = compute_word_appearance_frequencies(dictionary)
    for word in dictionary:
        score = sum(map(lambda letter: word_appearance_frequencies[letter], set(word)))
        scores[word] = score
    return scores


def filter_misplaced_letters(dictionary: List[str], letter: str, index: int) -> List[str]:
    return list(filter(lambda word: word.find(letter) > 0 and word.find(letter) != index, dictionary))


@click.command()
@click.option("--dictionary-path", help="Path to the dictionary path")
@click.option("--word-length", help="Length of the word", type=int)
def main(dictionary_path: str, word_length: int) -> None:
    dictionary = read_dictionary(dictionary_path)
    click.secho(f"Total words in dictionary: {len(dictionary)}", bold=True, fg="green")
    filtered_dictionary = filter_word_length(dictionary, word_length)
    click.secho(
        f"Words of {word_length} letters: {len(filtered_dictionary)}",
        bold=True,
        fg="green",
    )

    blacklist_letters = "AIRSLNDP"
    reg_sub = ".E.OT"
    misplaced_letters = [("E", 3), ("T", 3), ("O", 4)]

    reg = rf"^{reg_sub}$"

    filtered_dictionary_2 = remove_absent_letters(filtered_dictionary, list(blacklist_letters))
    click.secho(
        f"Removing words with {'-'.join(list(blacklist_letters))}: {len(filtered_dictionary_2)}",
        bold=True,
        fg="green",
    )

    filtered_dictionary_3 = keep_placed_letters(filtered_dictionary_2, reg)
    click.secho(
        f"Keeping words matching {reg_sub}: {len(filtered_dictionary_3)}",
        bold=True,
        fg="green",
    )

    filtered_dictionary_4 = filtered_dictionary_3
    for letter, index in misplaced_letters:
        filtered_dictionary_4 = filter_misplaced_letters(filtered_dictionary_4, letter, index)
        click.secho(
            f"Keeping words with misplaced {letter} as letter {index+1}: {len(filtered_dictionary_4)}",
            bold=True,
            fg="green",
        )

    scores = score_words(filtered_dictionary_4)
    pretty_print_frequencies(scores, 10)


if __name__ == "__main__":
    main()
