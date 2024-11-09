from docketpy.core import Person, Student, School

def test_person():
    p = Person('John Doe', 25)
    print("testing name")
    assert p.name == 'John Doe'
    print("testing age")
    assert p.age == 25

def test_student():
    s = Student('John Doe', 25, 'MIT')
    assert s.name == 'John Doe'
    assert s.age == 25
    assert s.get_school() == 'MIT'

def test_school():
    h = School("Harvard University", "Boston MA")
    assert h.location == "Boston MA"