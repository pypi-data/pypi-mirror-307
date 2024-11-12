"""
Dog class
"""


class Dog:
    """
    Class for specifying dog breeds
    """

    attr1 = "mammals"
    attr2 = "dog"
    is_good = True

    # A sample method
    def what_am_i(self):
        """
        Descriobe the dog attributes
        """
        return f"I am a {self.attr2} first but also a {self.attr1}"

    def am_i_good(self):
        """
        Am I a good dog
        """
        return self.is_good


# slippers = Dog()
# print(slippers.attr1)
# print(slippers.what_am_i())
