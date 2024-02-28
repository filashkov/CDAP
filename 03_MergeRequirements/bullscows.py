import random
import urllib.request
from typing import Tuple

import cowsay


VOC_URL = "https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt"
COW_FILE = "cat.cow"
with open(COW_FILE) as file_cow:
    cow = cowsay.read_dot_cow(file_cow)


def read_from_url(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        vocabulary = data.split('\n')
    return [word for word in vocabulary if word]


def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    # how many letters of guess are in secret
    cows = len(set(guess) & set(secret))    
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        guess = input(cowsay.cowsay(prompt, cowfile=cow) + "\n").strip()
        if valid is None or guess in valid:
            return guess
        print("Слово отсутствует в словаре. Попробуйте ещё раз")


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    attempts = 0
    
    while True:
        guess = ask("Введите слово", words)
        attempts += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        
        if b == len(secret):
            print(f"Поздравляю! Вы отгадали секретное слово '{secret}' за {attempts} попыток!")
            return attempts


if __name__ == "__main__":
    vocabulary = read_from_url(VOC_URL)
    gameplay(ask, inform, vocabulary)
