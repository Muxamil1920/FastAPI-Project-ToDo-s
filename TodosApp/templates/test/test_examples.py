import pytest

def test_equal_or_not():
    assert 3 == 3
    assert 3!= 1

def test_is_instance():
    assert isinstance('This is a string',str)
    assert not isinstance('10',int)

def test_boolean():
    validate = True
    assert validate is True
    assert ('Hello' == 'World') is False

def test_types():
    assert type('Hello' is str)
    assert type("10" is not int)

def test_greater_than_and_less_than():
    assert 7 > 3
    assert 4 < 8

def test_list():
    my_list = [1,2,3,4,5]
    any_list = [False, False]
    assert 1 in my_list
    assert 7 not in my_list
    assert not any(any_list)


class Student:
    def __init__(self, first_name:str, last_name:str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year

def test_person_initialization():
    p = Student('Muzamil','Bhat', 'Computer science', 3)
    assert p.first_name == 'Muzamil'
    assert p.last_name == 'Bhat'
    assert p.major == 'Computer science'
    assert p.year == 3

@pytest.fixture
def default_employee():
    return Student('Muzamil','Bhat', 'Computer science', 3)

def test_person_intialization(default_employee):
    assert default_employee.first_name == 'Muzamil'
    assert default_employee.last_name == 'Bhat'
    assert default_employee.major == 'Computer science'
    assert default_employee.year == 3




