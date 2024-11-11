class Stack():
    def __init__(self, default_value: list = []) -> None :
        self.value = default_value
    
    def push(self, value) -> None:
        return self.value.append(value)
    
    def pop(self) :
        if not self.isempty():
            return self.value.pop()
        raise IndexError("stack is empty")
    
    def peek(self) :
        if not self.isempty():
            return self.value[-1]
        raise IndexError("stack is empty")
    
    def isempty(self) :
        return len(self.value) == 0
    
    def size(self) :
        return len(self.value)
    
    def __str__(self) -> str:
        return " ".join(str(item) for item in self.value)
