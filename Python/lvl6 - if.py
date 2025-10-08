age = int(input("How old are you? "))
name = ""

if age < 18:
    print("You are not old enough to use the program!")
    exit()
else:
    def sayHello(name, age):
        print("Hello " + name + ", you are " + str(age) + " years old.")

    inName = input("What is your name?\n")

    sayHello(inName, age)
