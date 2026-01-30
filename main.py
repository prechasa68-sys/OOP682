class Dog:
    def __init__(self , name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"{self.name} is {self.age} year old.")

    def __str__(self):
        return f"{self.name} is {self.age} year."


def main():
    my_dog = Dog("luchifer", 3)
    my_dog.info()
    print(my_dog)


if __name__ == "__main__":
    main()
