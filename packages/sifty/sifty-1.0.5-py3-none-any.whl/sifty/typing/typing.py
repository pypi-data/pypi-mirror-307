class String:
    def __init__(self, initial = ..., /):
        if not isinstance(initial, str):
            self.value = str(initial)
        else:
            self.value = initial    

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

    def __add__(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return NotImplemented
    
    def __getitem__(self, key):
        return self.value[key]

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        return f'String({self.value!r})'

    def __call__(self, func):
        def wrapper(*args: Any, **kwargs: Any) -> 'String':
            result = func(*args, **kwargs)
            # Ensure the function returns a String instance
            if isinstance(result, String):
                return result
            return String(str(result))  # Wrap the result in String if it's not already
        return wrapper

    def __call__(self):
        return self

    def to_upper(self):
        return String(self.value.upper())

    def to_lower(self):
        return String(self.value.lower())

    def capitalize(self):
        return String(self.value.capitalize())

    def reverse(self):
        return String(self.value[::-1])

    def contains(self, substring):
        return substring in self.value

    def split(self, delimiter):
        return [String(part) for part in self.value.split(delimiter)]

    def join(self, iterable):
        return String(self.value.join(str(item) for item in iterable))

    def format(self, *args, **kwargs):
        return String(self.value.format(*args, **kwargs))

    def replace(self, old, new, count):
        return String(self.value.replace(old, new, count))

    def strip(self):
        return String(self.value.strip())

    def starts_with(self, prefix):
        return self.value.startswith(prefix)

    def ends_with(self, suffix):
        return self.value.endswith(suffix)    
