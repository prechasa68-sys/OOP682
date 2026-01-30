class student(person):
    def __init(self, pid, name, age, student_id):
        super().__init__(pid,name,age)
        self.student_id = student_id

    def __str__(self):
        return f"student[{self.pid}, {self.name}, {self.age}]"