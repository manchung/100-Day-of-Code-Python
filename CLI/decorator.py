
def logging_decorator(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        print(f'You called {func.__name__}{args}')
        print(f'It returned: {value}') 
        return value
    return wrapper

@logging_decorator
def a_function(*args):
    return sum(args)

a_function(1, 2, 3, 4, 5)