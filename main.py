#!/usr/bin/python3

''' a small game for guessing the numbers between 1 to 100 '''
import random
import os
from art import logo

numbers = [number for number in range(1, 101)]

# print the first display:
os.system('clear')
print(log)


def the_right_number():
    global numbers
    answer = random.choice(numbers)
    return answer

def display_message():
    print("""Welcome Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.""")


difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")
