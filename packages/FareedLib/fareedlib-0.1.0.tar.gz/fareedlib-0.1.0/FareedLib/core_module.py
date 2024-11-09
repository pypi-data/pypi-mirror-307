# core_module.py

def format_string(input_string, case='title'):
    """
    Formats the input string to the specified case.
    
    Args:
        input_string (str): The string to format.
        case (str): The case to apply; options are 'title', 'upper', 'lower'.
        
    Returns:
        str: The formatted string.
        
    Raises:
        ValueError: If an unsupported case is provided.
    """
    if case == 'title':
        return input_string.title()
    elif case == 'upper':
        return input_string.upper()
    elif case == 'lower':
        return input_string.lower()
    else:
        raise ValueError("Supported cases are 'title', 'upper', and 'lower'.")


def filter_even_numbers(numbers):
    """
    Filters out even numbers from a list.
    
    Args:
        numbers (list): A list of integers.
        
    Returns:
        list: A list containing only even numbers.
    """
    return [num for num in numbers if num % 2 == 0]


def calculate_mean(numbers):
    """
    Calculates the mean of a list of numbers.
    
    Args:
        numbers (list): A list of numbers (int or float).
        
    Returns:
        float: The mean of the numbers.
        
    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate mean of an empty list.")
    return sum(numbers) / len(numbers)


def find_max_value(numbers):
    """
    Finds the maximum value in a list of numbers.
    
    Args:
        numbers (list): A list of numbers.
        
    Returns:
        int or float: The maximum value in the list.
        
    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot find max value of an empty list.")
    return max(numbers)
