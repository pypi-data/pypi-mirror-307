"""
Entry point to run the package
"""

# First Party
from mhlmk_test_project.cat import cat
from mhlmk_test_project.dog import dog


def main():
    """
    main function
    """
    print("Mammal checking ...")

    my_dog = dog.Dog()
    print(f"{my_dog.what_am_i()}")

    my_cat = cat.Cat()
    print(f"{my_cat.what_am_i()}")


if __name__ == "__main__":
    main()
