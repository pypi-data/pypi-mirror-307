
class ErrHandling:
    def __init__(self, numbers, divisor):
        self.numbers = numbers
        self.divisor = divisor

    def divide_numbers(self):
        """Method to demonstrate basic error handling for division."""
        results = []
        try:
            for number in self.numbers:
                result = number / self.divisor
                results.append(result)
        except ZeroDivisionError as e:
            print(f"Error: Division by zero is not allowed. Details: {e}")
        except TypeError as e:
            print(f"Error: Unsupported operand types. Details: {e}")
        else:
            print("Division performed successfully.")
        finally:
            print("Completed division operation.")
        return results

    def access_list(self, index):
        """Method to demonstrate error handling for list index access."""
        try:
            return self.numbers[index]
        except IndexError as e:
            print(f"Error: Index out of range. Details: {e}")
        except TypeError as e:
            print(f"Error: Invalid index type. Details: {e}")
        finally:
            print("Completed list access operation.")

    def custom_exception_example(self, value):
        """Method to demonstrate raising and handling a custom exception."""
        try:
            if value < 0:
                raise NegativeValueError("Negative value provided is not allowed.")
            print(f"The value is: {value}")
        except NegativeValueError as e:
            print(f"Custom Error: {e}")
        finally:
            print("Completed custom exception operation.")

    def file_handling_example(self, filename):
        """Method to demonstrate file handling and associated errors."""
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(content)
        except FileNotFoundError as e:
            print(f"Error: File not found. Details: {e}")
        except IOError as e:
            print(f"Error: IO error occurred. Details: {e}")
        finally:
            print("Completed file handling operation.")

    def input_validation_example(self, user_input):
        """Method to demonstrate input validation with error handling."""
        try:
            number = int(user_input)
            print(f"Valid integer entered: {number}")
        except ValueError as e:
            print(f"Error: Invalid input. Expected an integer. Details: {e}")
        finally:
            print("Completed input validation operation.")

class NegativeValueError(Exception):
    """Custom exception for handling negative values."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    # Test data
    numbers = [10, 20, 30, 40]
    divisor = 0  # This will cause a ZeroDivisionError

    # Create an instance of the ErrorHandlingExample class
    handler = ErrHandling(numbers, divisor)

    # Example 1: Handling division by zero and other errors
    print("Example 1: Division Error Handling")
    results = handler.divide_numbers()
    print("Results:", results)
    print("\n")

    # Example 2: Handling list index access errors
    print("Example 2: List Index Error Handling")
    item = handler.access_list(5)  # This will cause an IndexError
    print("Accessed Item:", item)
    print("\n")

    # Example 3: Handling custom exceptions
    print("Example 3: Custom Exception Handling")
    handler.custom_exception_example(-10)  # This will raise a NegativeValueError
    print("\n")

    # Example 4: Handling file-related errors
    print("Example 4: File Handling Error Handling")
    handler.file_handling_example("non_existent_file.txt")  # This will cause a FileNotFoundError
    print("\n")

    # Example 5: Handling input validation errors
    print("Example 5: Input Validation Error Handling")
    handler.input_validation_example("abc")  # This will cause a ValueError
    print("\n")


"""
    Explanation:
    ErrorHandlingExample Class: This class encapsulates all the error-handling examples, demonstrating how to handle various types of errors using OOP.
    
    divide_numbers Method: Demonstrates handling ZeroDivisionError and TypeError during division operations.
    
    access_list Method: Demonstrates handling IndexError and TypeError when accessing list elements.
    
    custom_exception_example Method: Demonstrates how to define and raise a custom exception (NegativeValueError).
    
    file_handling_example Method: Demonstrates file handling and catching FileNotFoundError and IOError.
    
    input_validation_example Method: Demonstrates input validation and handling ValueError when converting input to an integer.
    
    NegativeValueError Class: A custom exception class that inherits from the base Exception class, used to handle cases where a negative value is not acceptable.
    
    if __name__ == "__main__": Block: This block is used to test the different methods, triggering different exceptions to show how they are handled.
    
    Running the Program
    Save the code in a file, e.g., errHandling.py.
    Run the script with Python: python error_handling_example.py.
    Observe how different types of errors are handled and how the program continues to execute even after encountering errors.
    Concepts Covered:
    Standard Exceptions: Handling common exceptions like ZeroDivisionError, IndexError, FileNotFoundError, TypeError, etc.
    Custom Exceptions: How to create and use custom exceptions.
    try-except-else-finally: Demonstrates the complete error-handling structure.
    Error Handling in Functions: Encapsulating error-handling logic within methods of a class.
    This example provides a solid foundation for understanding error handling in Python using OOP principles. You can expand this by adding more specific error-handling cases or integrating it into larger applications.
"""