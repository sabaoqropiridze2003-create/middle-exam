import random


def load_words(filname):

    try:
        with open(filname, "r") as file:
            words = [line.strip().lower() for line in file if line.strip()]
            return words
    except FileNotFoundError:
        print(f"Error: The file '{filname}' was not found.")
        return []


def choose_dificulty():

    print("\nChoose a difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        choice = input("Enter your choice(1, 2 or 3): ").strip().lower()
        if choice == "1":
            return "hangman/modes/easy.txt"
        elif choice == "2":
            return "hangman/modes/medium.txt"
        elif choice == "3":
            return "hangman/modes/hard.txt"
        else:
            print("\nInvalid choice. Please enter 1, 2 or 3.")


def play_game(stats):
    print("\nWelcome to the Word Guessing Game!")
    filename = choose_dificulty()
    words = load_words(filename)

    if not words:
        print("\nNo words available to play. Exiting the game.")
        return

    stats["games_played"] += 1
    secret_word = random.choice(words)
    guessed_letters = set()
    wrong_attempts = 0
    max_attempts = 6

    print("\nthe word has been chosen. Start guessing letters!")
    print("note: to exit the game, type 'exit'.")

    while wrong_attempts < max_attempts:
        display_word = ' '.join(
            [letter if letter in guessed_letters else '_' for letter in secret_word])
        print(f"\nWord: {display_word}")
        print(f"Atempts left: {max_attempts - wrong_attempts}")

        if guessed_letters:
            used_letters = ', '.join(sorted(guessed_letters))
            print(f"Used letters: [{used_letters}]")
        else:
            print("Used letters: []")

        if '_' not in display_word:
            print(f"\nCongratulations! You've guessed the word: {secret_word}")
            stats["wins"] += 1
            break

        guess = input(
            "guess a letter (or type 'exit' to quit): ").strip().lower()

        if guess == 'exit':
            print(f"\nThanks for playing! The secret word was: {secret_word}")
            stats["losses"] += 1
            break

        if len(guess) != 1 or not guess.isalpha():
            print("\nInvalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(
                f"\nYou've already guessed the letter '{guess}'. Try a different letter.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"\nGood job! The letter '{guess}' is in the word.")
        else:
            print(f"\nSorry, the letter '{guess}' is not in the word.")
            wrong_attempts += 1

    if wrong_attempts == max_attempts:
        print(
            f"\nGame over! You've used all your attempts. The secret word was: {secret_word}")
        stats["losses"] += 1


def main():

    stats = {"wins": 0, "losses": 0, "games_played": 0}

    while True:
        play_game(stats)

        print("\nGame Statistics:")
        print(f"Games Played: {stats['games_played']}")
        print(f"Wins: {stats['wins']}")
        print(f"Losses: {stats['losses']}")

        play_again = input(
            "Do you want to play again? (yes/no): ").strip().lower()

        if play_again != 'yes':
            print(f"\nThanks for playing! Goodbye!")
            break


main()
