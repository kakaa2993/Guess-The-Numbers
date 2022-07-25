#!/usr/bin/python3

''' a small game for guessing the numbers between 1 to 100 '''
import random
import os
from art import logo


# print the first display:
os.system('clear')
print(logo)


answer = random.randint(1,100)

print("Welcome Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
print(answer)
num_of_attempts = 10
difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
if difficulty == "hard":
    num_of_attempts = 5

def guessing_the_number(attempts):
    global answer
    while attempts > 0:
        print(f'You have {attempts} attempts remaining to guess the number. ')
        guess = int(input("Make a guess: "))
        if guess == answer:
            print(f"You got it! The answer was {answer}.😃 ")
            attempts = 0
        elif guess > answer:
            print("Too high.\nGuess agian.")
        elif guess < answer:
            print("Too low.\nGuess agian.")
        attempts -= 1
    if attempts == 0:
        print("You've run out of guesses, you lose.🤪")

guessing_the_number(attempts=num_of_attempts)



