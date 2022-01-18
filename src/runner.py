# Third party
import click

# Local
from wordle_assistant import WordleAssistant


@click.command()
@click.option("-w", "--word-list-path", help="Path to the word list")
def main(word_list_path: str):
    assistant = WordleAssistant(word_list_path)
    assistant.play()


if __name__ == "__main__":
    main()
