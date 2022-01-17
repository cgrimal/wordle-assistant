# Python standard lib
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
    frequencies = dict.fromkeys(list("ABCDEFGHIJKLMNOPQRSTUVXYZ"), 0.0)
    all_words = "".join(dictionary)
    total_letters = len(all_words)
    for letter in frequencies:
        frequencies[letter] = all_words.count(letter) / total_letters
    return frequencies


def compute_word_appearance_frequencies(dictionary: List[str]) -> Dict[str, float]:
    return compute_global_frequencies(
        list(map(lambda word: "".join(set(word)), dictionary))
    )


def pretty_print_frequencies(frequencies: Dict[str, float]) -> None:
    for letter, frequency in sorted(
        frequencies.items(), key=lambda item: item[1], reverse=True
    ):
        click.secho(f"{letter}: {round(frequency * 100, 2)}%")


@click.command()
@click.option("--dictionary-path", help="Path to the dictionary path")
@click.option("--word-length", help="Length of the word", type=int)
def main(dictionary_path: str, word_length: int) -> None:
    dictionary = read_dictionary(dictionary_path)
    click.secho(f"Total words in dictionary: {len(dictionary)}", bold=True, fg="green")
    filtered_dictionary = filter_word_length(dictionary, word_length)
    click.secho(
        f"Words of {word_length} letters in dictionary: {len(filtered_dictionary)}",
        bold=True,
        fg="green",
    )
    click.secho("Letter global frequencies:", bold=True, fg="green")
    pretty_print_frequencies(compute_global_frequencies(filtered_dictionary))
    click.secho("Letter word appearance frequencies:", bold=True, fg="green")
    pretty_print_frequencies(compute_word_appearance_frequencies(filtered_dictionary))


if __name__ == "__main__":
    main()
