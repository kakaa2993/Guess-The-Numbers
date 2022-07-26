#!/usr/bin/python3
''' a small game for guessing the numbers between 1 to 100 '''
import random
import os
from art import logo

# print the first display:
os.system('clear')
print(logo)

ANSWER = random.randint(1,100)

print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
num_of_attempts = 10
difficulty = input("Choose a difficulty. Type 'easy' or 'hard'(hard = 5 attempts / easy = 10 atempts): ").lower()
if difficulty == "hard":
    num_of_attempts = 5

def guessing_the_number(attempts):
    '''gues and print the result of the guessing numbers'''
    global ANSWER
    while attempts > 0:
        print(f'You have {attempts} attempts remaining to guess the number. ')
        guess = int(input("Make a guess: "))
        if guess == ANSWER:
            print(f"You got it! The answer was {ANSWER}.😃 ")
            attempts = 0
        elif guess > ANSWER:
            print("Too high.👆\nGuess agian.")
        elif guess < ANSWER:
            print("Too low.👇\nGuess agian.")
        attempts -= 1
    if attempts == 0:
        print("You've run out of guesses, you lose.🤪")
        print(f"the right number was {ANSWER}")

guessing_the_number(attempts=num_of_attempts)



