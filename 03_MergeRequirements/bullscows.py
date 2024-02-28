import random

def bullscows(guess: str, secret: str) -> (int, int):
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(min(guess.count(char), secret.count(char)) for char in set(guess)) - bulls
    return bulls, cows

def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        guess = input(prompt).strip()
        if valid is None or guess in valid:
            return guess
        print("Слово отсутствует в словаре. Попробуйте ещё раз")

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    attempts = 0
    
    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        
        if b == len(secret):
            print(f"Поздравляю! Вы отгадали секретное слово '{secret}' за {attempts} попыток!")
            return attempts

if __name__ == "__main__":
    words = ["ропот", "полип", "малина", "киви", "коктель"]
    gameplay(ask, inform, words)
