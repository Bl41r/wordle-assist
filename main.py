"""Wordle assist.

In the same directory as this script, place a file called 'wordlist.txt' which contains a word on each line.
"""
import random


def find_best_words(words: list) -> list:
    """Return the best words to try next based on how popular the letters are in the list."""
    letter_to_usage_count = {}
    for word in words:
        for letter in set(word):
            letter_to_usage_count[letter] = letter_to_usage_count.get(letter, 0) + 1

    word_to_letter_usage_count = {}
    for word in words:
        sum_of_letter_usages = 0
        for letter in set(word):
            sum_of_letter_usages += letter_to_usage_count[letter]

        word_to_letter_usage_count[word] = sum_of_letter_usages

    max_usage_count_value = max(word_to_letter_usage_count.values())

    return [k for k, v in word_to_letter_usage_count.items() if v == max_usage_count_value]


def check_word(exacts: str, includes: str, excludes: str, word: str) -> bool:
    """Return True if a word meets the given criteria."""
    # check if green letters align with word
    for i in range(0, 5):
        if word[i] != exacts[i] and exacts[i] != '*':
            return False

    # check if yellow letters are in a valid spot
    included_letters = list(includes)
    for i, letter in enumerate(included_letters):
        if letter != '*' and (letter not in word or included_letters[i] == word[i]):
            return False

    # check if the grey letters are not in non-green spaces
    starred_exacts_indices = [i for i, letter in enumerate(exacts) if letter == '*']
    excluded_letters = list(excludes)
    for i in starred_exacts_indices:
        if word[i] in excluded_letters:
            return False

    return True


def get_matching_words(exacts: str, includes: str, excludes: str, wordlist: [str]) -> list:
    """Return a list of words meeting the given criteria."""
    matching_words = []

    for word in wordlist:
        if check_word(exacts, includes, excludes, word):
            matching_words.append(word)

    return matching_words


def load_words(filename: str) -> list:
    """Return a list of five-letter lower-case words after reading a file with a word on each line."""
    with open(filename, 'r') as f:
        words = [line.rstrip() for line in f]
    return [word.lower() for word in words if len(word) == 5]


def main() -> None:
    """Main."""
    five_letter_words = load_words('wordlist.txt')

    print("\n*** Welcome to the Wordle(tm) Assistant ***\nPress Ctrl+D at any time to exit.")

    while True:
        exacts = input("\nWhat letters match in their positions? (Green letters) \nexample: *oi*g\n").lower()
        if len(exacts) != 5:
            print('word must be 5 letters long--restarting')
            continue

        includes = input("Which letters appear in the word somewhere else? (Yellow letters)\nexample: ***n*\n").lower()
        if len(includes) != 5:
            print('word can only be 5 letters long--restarting')
            continue

        excludes = input("What letters are excluded?  (All grey letters)\nexample: xyz\n").lower()

        matching_words = get_matching_words(exacts, includes, excludes, five_letter_words)
        best_guesses = find_best_words(matching_words)
        random.shuffle(matching_words)

        print("Here are some matching words to try:\n", matching_words)
        if len(matching_words) > len(best_guesses):
            print('suggestions:', best_guesses, '\n')


if __name__ == '__main__':
    main()
