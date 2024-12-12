class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        return f"Name: {self.name}, Age: {self.age}"

class Student(Person):
    def __init__(self, name, age, group, avg_grade):
        super().__init__(name, age)
        self.group = group
        self.avg_grade = avg_grade

    def scholarship(self):
        if self.avg_grade == 5:
            return 6000
        elif self.avg_grade < 5:
            return 4000
        else:
            return 0

    def compare_scholarship(self, other):
        if self.scholarship() > other.scholarship():
            return "more"
        elif self.scholarship() < other.scholarship():
            return "less"
        else:
            return "equal"

class Graduate(Student):
    def __init__(self, name, age, group, avg_grade, research_title):
        super().__init__(name, age, group, avg_grade)
        self.research_title = research_title

    def scholarship(self):
        if self.avg_grade == 5:
            return 8000
        elif self.avg_grade < 5:
            return 6000
        else:
            return 0

# Test
student = Student("Peter", 20, "CS101", 4.5)
graduate = Graduate("Alibet", 25, "CS102", 5, "AI Research")

print(student.info(), "Scholarship:", student.scholarship())
print(graduate.info(), "Scholarship:", graduate.scholarship())

# Compare scholarships
comparison = student.compare_scholarship(graduate)
print(f"The student's scholarship is {comparison} than the graduate's scholarship.")
