class MyBaseClass:
    def my_function(self):
        pass

class MyClass1(MyBaseClass):
    def my_function(self):
        print("MyClass1.my_function called")

class MyClass2(MyBaseClass):
    def my_function(self):
        print("MyClass2.my_function called")

classes = [MyClass1(), MyClass2()]

for cls in classes:
    cls.my_function()
