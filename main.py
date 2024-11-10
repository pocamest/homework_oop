BALL_SYSTEM = 10


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.average_grade}\n'
            f'Курсы в процессе изучения: {self.courses_in_progress}\n'
            f'Завершенные курсы: {self.finished_courses}\n'
        )

    def __eq__(self, other):
        return self.average_grade == other.average_grade

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.average_grade < other.average_grade

    def __le__(self, other):
        return self.average_grade <= other.average_grade

    def __gt__(self, other):
        return self.average_grade > other.average_grade

    def __ge__(self, other):
        return self.average_grade >= other.average_grade

    @property
    def average_grade(self):
        return calculate_average(self.grades.values())

    def add_courses(self, name_cours):
        self.finished_courses.append(name_cours)

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress
                and grade in range(BALL_SYSTEM+1)):
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
        )


class Lecturer(Mentor):
    def __init__(self, name, surname):
        self.grades = {}
        return super().__init__(name, surname)

    def __str__(self):
        return (
            f'{super().__str__()}'
            f'Средняя оценка за лекции: {self.average_grade}\n'
        )

    def __eq__(self, other):
        return self.average_grade == other.average_grade

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.average_grade < other.average_grade

    def __le__(self, other):
        return self.average_grade <= other.average_grade

    def __gt__(self, other):
        return self.average_grade > other.average_grade

    def __ge__(self, other):
        return self.average_grade >= other.average_grade

    @property
    def average_grade(self):
        return calculate_average(self.grades.values())


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress
                and grade in range(BALL_SYSTEM+1)):
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'


def calculate_average(nested_grades):
    all_grades = [
        grade for grades in nested_grades
        for grade in grades
    ]
    return sum(all_grades) / len(all_grades)


def get_average_hw(students, course):
    nested_grades = (student.grades.get(course, []) for student in students)
    return calculate_average(nested_grades)


def get_average_lecturers(lecturers, course):
    nested_grades = (lecturer.grades.get(course, []) for lecturer in lecturers)
    return calculate_average(nested_grades)


best_student = Student('Anna', 'Eman', 'female')
best_student.courses_in_progress.append('Python')

cool_student = Student('Oliver', 'Giroud', 'male')
cool_student.courses_in_progress.append('Python')


best_lecturer = Lecturer('Santi', 'Cazorla')
best_lecturer.courses_attached.append('Python')

cool_lecturer = Lecturer('Inigo', 'Martinez')
cool_lecturer.courses_attached.append('Python')


python_reviewer = Reviewer('Piter', 'Crouch')
python_reviewer.courses_attached.append('Python')

git_reviewer = Reviewer('John', 'Showcross')
git_reviewer.courses_attached.append('Git')


python_reviewer.rate_hw(best_student, 'Python', 10)
python_reviewer.rate_hw(cool_student, 'Python', 7)

python_reviewer.rate_hw(best_student, 'Python', 9)
python_reviewer.rate_hw(cool_student, 'Python', 8)


best_student.rate_lecturer(best_lecturer, 'Python', 8)
best_student.rate_lecturer(cool_lecturer, 'Python', 6)

cool_student.rate_lecturer(best_lecturer, 'Python', 9)
cool_student.rate_lecturer(cool_lecturer, 'Python', 7)

print(best_student, best_student.grades, sep='\n', end='\n\n')
print(cool_student, cool_student.grades, sep='\n', end='\n\n')
print(best_lecturer, best_lecturer.grades, sep='\n', end='\n\n')
print(cool_lecturer, cool_lecturer.grades, sep='\n', end='\n\n')
print(python_reviewer, git_reviewer, sep='\n')
print(f'best_student == cool_student {best_student == cool_student}')
print(f'best_student > cool_student {best_student > cool_student}')
print(f'cool_lecturer >= best_lecturer {cool_lecturer >= best_lecturer}')
print(f'cool_lecturer < best_lecturer {cool_lecturer < best_lecturer}')
pattern_hw = (
    f'Средняя оценка за д/з по всем студентам курса Python'
    f' {get_average_hw([best_student, cool_student], "Python")}'
)
print(pattern_hw)
pattern_lecturers = (
    f'Средняя оценка за лекции всех лекторов курса Python'
    f' {get_average_lecturers([best_lecturer, cool_lecturer], "Python")}'
)
print(pattern_lecturers)
