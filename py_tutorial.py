# pylint: disable=missing-module-docstring, disable=missing-function-docstring, disable=missing-class-docstring

from math import ceil
from logger import Logging


def brand_name_generator():
    Logging("Welcome to the Band Name Generator")
    city = input("What's name of the city you grew up in?\n")
    Logging(f'City: {city}')
    pet = input("What's your pet's name?\n")
    Logging(f'Pet: {pet}')
    band_name = city + " " + pet
    Logging(f'Band Name: {band_name}')
    Logging(f'Your band name could be: {band_name}')
    Logging("Thank you for using the Band Name Generator!")


def number_practice():
    Logging("Welcome to the Number Practice")
    Logging(123_367_234)
    Logging(True)
    Logging(False)
    Logging(None)

    Logging("Welcome to the Number Practice" +
            str(True) + str(1228_3454) + str(None))

    Logging(round(123_367_234.12200282, 4))


def bill_splitter():
    Logging("Welcome to the Bill Splitter")
    total_bill = float(input("What was the total bill? $\n"))
    Logging(f"Total bill: {total_bill}")
    tip_percentage = int(
        input("What percentage tip would you like to give? 10, 12, or 15?\n"))

    if tip_percentage not in [10, 12, 15]:
        Logging("Invalid tip percentage. Please choose 10, 12, or 15.")
        return

    total_amount = ceil(total_bill + (total_bill * tip_percentage)) / 100

    num_of_people = int(input("How many people to split the bill?\n"))
    Logging(f"Number of people: {num_of_people}")

    if num_of_people <= 0:
        Logging("Invalid number of people. Please enter a positive integer.")
        return

    amount_per_person = total_amount / num_of_people
    Logging(f"Total amount (including tip): {total_amount:.2f}")
    Logging(f"Each person should pay: {amount_per_person:.2f}")


def input_print(type_str: str):
    Logging(f"Input type {type_str}: ")


def main():
    # brand_name_generator()
    # number_practice()
    # bill_splitter()

    # Logging(f"Number {199.0018222} is {199.0018222: .2f}")
    # Logging(str((not 5) == 5))
    input_print(input("What is your name? \n"))


if __name__ == "__main__":
    main()
