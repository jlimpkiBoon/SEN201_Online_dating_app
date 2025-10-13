import numbers

def is_number(value):
        return isinstance(value, numbers.Number)

def check_blank(question):
    while True:
        answer = input(question).strip()
        if answer:
            return answer
        print("Input cannot be blank. Please try again.")