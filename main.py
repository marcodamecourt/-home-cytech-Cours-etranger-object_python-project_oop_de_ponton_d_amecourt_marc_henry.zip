from abc import ABC, abstractmethod  
import tkinter as tk  
from tkinter import messagebox 
import re
import math  
import os  
import json 


class Operation(ABC):  # Creating an abstract base class Operation
    def __init__(self, name):  
        self.name = name
        
    @abstractmethod
    def perform(self, *args):  # Abstract method perform() to be implemented by subclasses
        pass


class Addition(Operation):  
    def __init__(self): 
        super().__init__("Addition")  

    def perform(self, *args):  
        return sum(args)  


class Subtraction(Operation):  
    def __init__(self):  
        super().__init__("Subtraction") 

    def perform(self, *args):  
        return args[0] - sum(args[1:])  


class Multiplication(Operation):  
    def __init__(self): 
        super().__init__("Multiplication")  

    def perform(self, *args):  
        result = 1  
        for num in args: 
            result *= num  
        return result  


class Division(Operation):  
    def __init__(self): 
        super().__init__("Division")  

    def perform(self, *args):  
        if 0 in args[1:]:  
            raise ValueError("Division by zero error")  
        return args[0] / math.prod(args[1:])  
    

class Calculator:  
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}  # Dictionary to store operator precedence

    def decimal_precision_decorator(func):  # Decorator function for decimal precision
        def wrapper(*args, **kwargs):  # Wrapper function to add decimal precision
            result = func(*args, **kwargs)  # Calling the original function
            return round(result, 2)  # Rounding the result to 2 decimal places
        return wrapper

    _instance = None  # Class variable to hold a single instance of the Calculator

    def __new__(cls):  
        if cls._instance is None:  
            cls._instance = super().__new__(cls)  
            cls._instance.operations = {}  # Dictionary to store operations
            cls._instance.register_operation('+', Addition())  
            cls._instance.register_operation('-', Subtraction())  
            cls._instance.register_operation('*', Multiplication()) 
            cls._instance.register_operation('/', Division())  
        return cls._instance  

    def register_operation(self, symbol, operation):  # Method to register an operation
        self.operations[symbol] = operation  # Storing the operation in the dictionary

    @decimal_precision_decorator  # Applying decimal precision decorator to the following method
    def evaluate_expression(self, expression):  # Method to evaluate mathematical expressions
        numbers = []  
        operator_stack = []  

        tokens = re.findall(r'(\d+\.?\d*)|([+\-*/()])', expression)  # Tokenizing the expression using regular expressions

        for token in tokens:  # Iterating through tokens
            if token[0].isdigit() or '.' in token[0]:  # Checking if token is a number
                numbers.append(float(token[0]))  # Adding number to the list
            elif token[1] in self.operations:  # Checking if token is an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[token[1]]):  # Checking operator precedence
                    operator = operator_stack.pop()  # Popping operator from stack
                    num2 = numbers.pop()  # Popping second operand
                    num1 = numbers.pop()  # Popping first operand
                    result = self.operations[operator].perform(num1, num2)  # Performing operation
                    numbers.append(result)  # Appending result to numbers list
                operator_stack.append(token[1])  # Adding operator to stack
            elif token[1] == '(':  # Handling left parenthesis
                operator_stack.append(token[1])  # Adding left parenthesis to stack
            elif token[1] == ')':  # Handling right parenthesis
                while operator_stack[-1] != '(':  # Until matching left parenthesis is found
                    operator = operator_stack.pop()  # Popping operator from stack
                    num2 = numbers.pop()  # Popping second operand
                    num1 = numbers.pop()  # Popping first operand
                    result = self.operations[operator].perform(num1, num2)  # Performing operation
                    numbers.append(result)  # Appending result to numbers list
                operator_stack.pop()  # Removing left parenthesis

        while operator_stack:  # Handling remaining operators in stack
            operator = operator_stack.pop()  # Popping operator from stack
            num2 = numbers.pop()  # Popping second operand
            num1 = numbers.pop()  # Popping first operand
            result = self.operations[operator].perform(num1, num2)  # Performing operation
            numbers.append(result)  # Appending result to numbers list

        return numbers[0]  # Returning the final result


class LoginApp(tk.Tk):  # Creating a login application window
    def __init__(self): 
        super().__init__()  
        self.title("Login Interface") 
        self.geometry("300x200")  

        self.load_users()  

        self.username_label = tk.Label(self, text="Username:")  
        self.username_label.pack(pady=10)  
        self.username_entry = tk.Entry(self)  
        self.username_entry.pack(pady=5)  

        self.password_label = tk.Label(self, text="Password:")  
        self.password_label.pack()  
        self.password_entry = tk.Entry(self, show="*")  
        self.password_entry.pack(pady=5) 

        self.login_button = tk.Button(self, text="Login", command=self.login)  
        self.login_button.pack(pady=5)  

        self.create_account_button = tk.Button(self, text="Create Account", command=self.create_account)  
        self.create_account_button.pack(pady=5)  

    def load_users(self):  # Method to load user data
        if not os.path.exists("users.json"):  
            self.users = {}  
        else:
            with open("users.json", "r") as file: 
                self.users = json.load(file)  

    def save_users(self):  # Method to save user data
        with open("users.json", "w") as file:  
            json.dump(self.users, file)  # Writing user data to the file

    def login(self):  # Method to handle login functionality
        username = self.username_entry.get()  
        password = self.password_entry.get()  

        if username in self.users and self.users[username] == password:  # Checking if username and password match
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")  
            self.destroy()  
            CalculatorApp(username)  # Launching the calculator app with the username
        else:
            messagebox.showerror("Login Error", "Incorrect username or password.")  

    def create_account(self):  # Method to handle account creation
        create_account_window = tk.Toplevel(self)  
        create_account_window.title("Create Account")  
        create_account_window.geometry("300x200")  

        new_username_label = tk.Label(create_account_window, text="New Username:")  
        new_username_label.pack(pady=5) 
        new_username_entry = tk.Entry(create_account_window)  
        new_username_entry.pack(pady=5) 

        new_password_label = tk.Label(create_account_window, text="New Password:")  
        new_password_label.pack()  
        new_password_entry = tk.Entry(create_account_window, show="*")  
        new_password_entry.pack(pady=5) 

        confirm_button = tk.Button(create_account_window, text="Confirm", command=lambda: self.add_user(new_username_entry.get(), new_password_entry.get(), create_account_window))  
        confirm_button.pack(pady=5)  

    def add_user(self, username, password, window):  # Method to add a new user
        if username in self.users:  # Checking if username already exists
            messagebox.showerror("Error", "This username already exists.")  
        else:
            self.users[username] = password  # Adding new user to the dictionary
            self.save_users()  
            messagebox.showinfo("Account Created", "New account created successfully.") 
            window.destroy()  

class CalculatorApp(tk.Tk):  # Creating a calculator application window
    def __init__(self, username):  
        super().__init__()  
        self.title(f"Calculator - User: {username}")  
        self.geometry("800x300")  

        self.calculator = Calculator()  
        
        self.username = username  
        self.calculations_filename = f"{username}_calculations.txt"  # Creating a filename for saving calculations

        self.calculator_label = tk.Label(self, text="Enter your calculation:")  
        self.calculator_label.pack(pady=10)  
        
        self.calculator_entry = tk.Entry(self, font=("Helvetica", 14))  
        self.calculator_entry.pack(pady=5)  

        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate_and_display_result)  
        self.calculate_button.pack(pady=10)  

        self.save_button = tk.Button(self, text="Save", command=self.save_data)  
        self.save_button.pack(side=tk.LEFT, padx=10)  

        self.append_button = tk.Button(self, text="Append to File", command=self.append_data)  
        self.append_button.pack(side=tk.LEFT, padx=10)  

        self.display_button = tk.Button(self, text="Display Results", command=self.display_results)  
        self.display_button.pack(side=tk.LEFT, pady=10)  

        self.logout_button = tk.Button(self, text="Logout", command=self.logout)  
        self.logout_button.pack(pady=5)  

        self.result_label = tk.Label(self, text="", font=("Helvetica", 18), fg="blue")  
        self.result_label.pack(pady=20)  

    def logout(self):  # Method to handle logout functionality
        self.destroy()  
        login_app = LoginApp()  # Launching the login window
        login_app.mainloop()

    def save_data(self):  # Method to save data to a file
        expression = self.calculator_entry.get() 
        result = self.result_label.cget("text")  

        with open(self.calculations_filename, "w") as file:  # Opening the file for writing 
            file.write(f"Expression: {expression}\n")  
            file.write(f"{result}\n\n") 
        messagebox.showinfo("Save", "Data saved successfully.")  

    def append_data(self):  # Method to append data to a file
        expression = self.calculator_entry.get()  
        result = self.result_label.cget("text") 

        with open(self.calculations_filename, "a") as file:  # Opening the file for appending
            file.write(f"Expression: {expression}\n")  
            file.write(f"{result}\n\n")  
        messagebox.showinfo("Append", "Data appended successfully.")  
            
    def display_results(self):  # Method to display results from a file
        try:
            with open(self.calculations_filename, "r") as file:  # Opening the file for reading
                content = file.read()  
                if content.strip():  
                    messagebox.showinfo("Results", content)  
                else:
                    messagebox.showinfo("Results", "File is empty.")  
        except FileNotFoundError:
            messagebox.showerror("Load", "The file does not exist.")  

    def calculate_and_display_result(self):  # Method to calculate the result
        expression = self.calculator_entry.get()  
        try:
            result = self.calculator.evaluate_expression(expression)  
            self.result_label.config(text=f"Result : {result}")  
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))  

if __name__ == "__main__":  
    login_app = LoginApp()  
    login_app.mainloop()  
