import numbers

def check_number(question):
    while True:
        value = input(question).strip()
        if not value:
            print("Input cannot be blank. Please try again.")
            continue

        try:
            # Automatically detect integer or float
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def check_blank(question):
    while True:
        answer = input(question).strip()
        if answer:
            return answer
        print("Input cannot be blank. Please try again.")
