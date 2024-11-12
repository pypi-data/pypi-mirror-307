class ErrHandler:
    def __init__(self):
        pass

    @staticmethod
    def handle_error(error):
        """Handles different types of errors and prints corresponding messages."""
        if isinstance(error, FileNotFoundError):
            print("Error: The file was not found.")
        elif isinstance(error, ZeroDivisionError):
            print("Error: Division by zero is not allowed.")
        elif isinstance(error, ValueError):
            print("Error: Invalid value encountered.")
        elif isinstance(error, TypeError):
            print("Error: Type mismatch encountered.")
        elif isinstance(error, IndexError):
            print("Error: Index out of range.")
        elif isinstance(error, KeyError):
            print("Error: The specified key does not exist.")
        elif isinstance(error, IOError):
            print("Error: An I/O operation failed.")
        elif isinstance(error, ConnectionError):
            print("Error: Network connection failed.")
        elif isinstance(error, ImportError):
            print("Error: Failed to import a module.")
        elif isinstance(error, AttributeError):
            print("Error: Attribute does not exist.")
        else:
            print(f"An unexpected error occurred: {str(error)}")

# Example Usage:
if __name__ == "__main__":
    error_handler = ErrHandler()

    # Example 1: FileNotFoundError
    try:
        with open('non_existent_file.txt', 'r') as file:
            content = file.read()
    except Exception as e:
        error_handler.handle_error(e)

    # Example 2: ZeroDivisionError
    try:
        result = 10 / 0
    except Exception as e:
        error_handler.handle_error(e)

    # Example 3: ValueError
    try:
        number = int("abc")
    except Exception as e:
        error_handler.handle_error(e)
