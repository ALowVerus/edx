GREY = '\033[39m'
RED = '\033[31m'
GREEN = '\033[34m'


# TESTS
class Test:

    def describe(self, name):
        print("SET:", name)

    def it(self, name):
        print("Testing", name)

    def assert_equals(self, a, b, error_message=""):
        if a == b:
            print(GREEN, "Okay!", a, "equals", b)
        else:
            print(RED, "Bad!", a, "!=", b, ".", error_message)
        print(GREY)

    def expect(self, tf):
        if tf:
            print(GREEN, "Passed!")
        else:
            print(RED, "Failed!")

    def expect_error(self, *kwargs):
        pass


test = Test()
