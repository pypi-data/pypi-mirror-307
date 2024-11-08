
def decremental(f):
    def wrap(*args, **kwargs):  # args and kwargs passed to f
        x = f(*args, **kwargs)  # Send them again to keep the function working normally
        return sorted(x, key=len, reverse=True)  # Do something with the result
    return wrap