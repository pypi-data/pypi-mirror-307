"""
Cat class
"""


class Cat:
    """
    Class for specifying docatg breeds
    """

    attr1 = "mammal"
    attr2 = "cat"
    is_good = False

    # A sample method
    def what_am_i(self):
        """
        Descriobe the cat attributes
        """
        return f"I am a {self.attr2} first but also a {self.attr1}"

    def am_i_good(self):
        """
        Am I a cat dog
        """
        return self.is_good


# whiskers = Cat()
# print(whiskers.attr1)
# print(whiskers.what_am_i())
