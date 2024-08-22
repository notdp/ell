import ell
import numpy as np

from ell.stores.sql import PostgresStore


class MyPrompt:
    x : int

def get_random_length():
    return int(np.random.beta(2, 6) * 1500)

@ell.text(model="gpt-4o-mini")
def hello(world : str):
    """Your goal is to be really meant to the other guy whiel say hello"""
    name = world.capitalize()
    number_of_chars_in_name = get_random_length()

    return f"Say hello to {name} in {number_of_chars_in_name} characters or more!"


if __name__ == "__main__":
    ell.config.verbose = True
    ell.set_store(PostgresStore('postgresql://postgres:postgres@localhost:5432/ell'), autocommit=True)

    greeting = hello("sam altman") # > "hello sama! ... "



    # F_Theta: X -> Y

    # my_prompt_omega:  Z -> X

