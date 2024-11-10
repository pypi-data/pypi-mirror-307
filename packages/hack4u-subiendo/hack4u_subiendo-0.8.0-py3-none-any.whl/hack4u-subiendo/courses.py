class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self): # This is a special method for representing data, this will create a list
        return f"{self.name} [{self.duration}] hours ({self.link})"
courses = [
    Course("Introduccion a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalizacion de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introduction to Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course

    return None

