def process_data(data, operations=None):
    """
    Processes data based on a sequence of operations.

    Args:
    data: The data to be processed. This could be of any type depending on the operations.
    operations (list of tuple): Each tuple contains the processing function and its arguments.
                                Format: [(function, arg1, arg2, ...), ...]

    Returns:
    Processed data.
    """
    if operations:
        for operation in operations:
            function = operation[0]
            args = operation[1:]
            data = function(data, *args)
    return data

def filter_data(data, condition):
    """
    Filters the data based on a provided condition function.

    Args:
    data (list): The data to be filtered.
    condition (function): A function that returns True if the item should be included.

    Returns:
    list: The filtered data.
    """
    return [item for item in data if condition(item)]

def map_data(data, transformation):
    """
    Applies a transformation function to each item in the data.

    Args:
    data (list): The data to be transformed.
    transformation (function): A function that returns the transformed item.

    Returns:
    list: The transformed data.
    """
    return [transformation(item) for item in data]

def aggregate_data(data, aggregator, initial_value):
    """
    Aggregates the data using a provided aggregation function.

    Args:
    data (list): The data to be aggregated.
    aggregator (function): A function that takes two arguments - the running total and the current item, and returns the updated total.
    initial_value: The initial value for the aggregation.

    Returns:
    The aggregated result.
    """
    result = initial_value
    for item in data:
        result = aggregator(result, item)
    return result
