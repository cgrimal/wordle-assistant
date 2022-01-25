# Python standard lib
import re
from typing import Dict
from typing import Iterable
from typing import List

# Third party
import click


class WordleAssistant:

    CHARACTER_LIST = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    GUESS_NUMBER = 10

    word_length: int
    word_list: List[str]
    word_list_entropy: List[str]

    def __init__(self, word_list_path: str):
        with open(word_list_path, "r") as word_list_file:
            self.word_list = word_list_file.read().splitlines()
        self.word_list_entropy = self.word_list

    def play(self):
        click.secho(f"Words count: {len(self.word_list)}", bold=True, fg="green")
        self.word_length = click.prompt("Number of letters in your game", type=int)
        self.word_list = self._filter_by_word_length(self.word_list, self.word_length)

        while len(self.word_list) > 1:
            click.secho(f"Words count: {len(self.word_list)}", bold=True, fg="green")
            click.secho("Your best guesses are:", bold=True, fg="green")
            self._best_guesses(self.word_list, self.GUESS_NUMBER)
            if (
                len(self.word_list_entropy) > 0
                and self.word_list != self.word_list_entropy
            ):
                click.secho("You can also try new letters:", bold=True, fg="green")
                self._best_guesses(self.word_list_entropy, 3)
            guess = click.prompt("Enter your guess          ", type=str)
            evaluation = click.prompt("Enter its evaluation (.!?)", type=str)
            self.word_list_entropy = self._remove_absent_letters(
                self.word_list_entropy, set(guess)
            )
            evaluation_tuples = list(zip(guess, evaluation))
            for index, (letter, evaluation) in enumerate(evaluation_tuples):
                if evaluation == ".":
                    if (letter, "!") not in evaluation_tuples:
                        self.word_list = self._remove_absent_letters(
                            self.word_list, letter
                        )
                    else:
                        self.word_list = self._filter_misplaced_letters(
                            self.word_list, letter, index
                        )
                elif evaluation == "!":
                    pattern_list = ["."] * self.word_length
                    pattern_list[index] = letter
                    pattern = "".join(pattern_list)
                    self.word_list = self._keep_placed_letters(
                        self.word_list, rf"^{pattern}$"
                    )
                elif evaluation == "?":
                    self.word_list = self._filter_misplaced_letters(
                        self.word_list, letter, index
                    )
        try:
            click.secho(f"THE SOLUTION: {self.word_list[0]}", bold=True, fg="red")
        except IndexError:
            click.secho(
                "404 Solution not found (maybe you mistyped an evaluation?)", fg="red"
            )

    def _best_guesses(self, word_list: List[str], guess_number: int = 5):
        word_scores = self._score_words(word_list)
        self._pretty_print_frequencies(word_scores, guess_number)

    def _score_words(self, word_list: List[str]) -> Dict[str, float]:
        scores = dict.fromkeys(word_list, 0.0)
        word_appearance_frequencies = self._compute_word_appearance_frequencies(
            word_list
        )
        for word in word_list:
            score = sum(
                map(lambda letter: word_appearance_frequencies[letter], set(word))
            )
            scores[word] = score
        return scores

    def _compute_global_frequencies(self, word_list: List[str]) -> Dict[str, float]:
        if len(word_list) == 0:
            return {}
        frequencies = dict.fromkeys(self.CHARACTER_LIST, 0.0)
        all_words = "".join(word_list)
        total_letters = len(all_words)
        for letter in frequencies:
            frequencies[letter] = all_words.count(letter) / total_letters
        return frequencies

    def _compute_word_appearance_frequencies(
        self, word_list: List[str]
    ) -> Dict[str, float]:
        return self._compute_global_frequencies(
            list(map(lambda word: "".join(set(word)), word_list))
        )

    @staticmethod
    def _pretty_print_frequencies(
        frequencies: Dict[str, float], limit: int = 5
    ) -> None:
        for word, frequency in sorted(
            frequencies.items(), key=lambda item: item[1], reverse=True
        )[:limit]:
            click.secho(f"{word}: {round(frequency * 100, 2)}%")

    @staticmethod
    def _filter_by_word_length(word_list: List[str], word_length: int) -> List[str]:
        return list(filter(lambda word: (len(word) == word_length), word_list))

    @staticmethod
    def _remove_absent_letters(
        word_list: List[str], absent_letters: Iterable[str]
    ) -> List[str]:
        def word_does_not_contain_blacklist_letters(word: str) -> bool:
            for absent_letter in absent_letters:
                if absent_letter in word:
                    return False
            return True

        return list(filter(word_does_not_contain_blacklist_letters, word_list))

    @staticmethod
    def _keep_placed_letters(
        word_list: List[str], regular_expression: str
    ) -> List[str]:
        return list(filter(lambda word: re.match(regular_expression, word), word_list))

    @staticmethod
    def _filter_misplaced_letters(
        word_list: List[str], letter: str, index: int
    ) -> List[str]:
        def word_contains_misplaced_letter(word: str) -> bool:
            # letter must be in the word...
            if letter not in word:
                return False
            # ...but not at the index
            for m in re.finditer(letter, word):
                if m.start() == index:
                    return False
            return True

        return list(
            filter(
                word_contains_misplaced_letter,
                word_list,
            )
        )
