class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
    # @property
    # def age(self):
    #     """This is Persons Age"""
    #     return self.age
    
    # @age.setter
    # def age(self, val):
    #     self.age = val


class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def say_hello(self):
        super().say_hello()
        print(f"I am a student at  {self.school}.")  
        
    def get_school(self):
        return self.school

    def set_school(self, school):
        self.school = school

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age
        

class School:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def location(self):
        return self.location

if __name__ == "__main__":
    person = Person("John", 30)
    person.say_hello()

    student = Student("Jane", 25, "MIT")
    student.say_hello()
    
    harvard = School("Harvard University", "Boston MA")
    
