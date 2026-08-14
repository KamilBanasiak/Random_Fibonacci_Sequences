from random import choice

def generate_random_Fibonacci_sequence(n: int, sampling_with_replacement = True) -> tuple:
    if n == 1:
        return (0)
    if n == 2:
        return (0, 1)
    elements = [0, 1]
    if sampling_with_replacement:
        pairs_sum = [0, 1, 2]
        for i in range(2, n):
            elements.append(choice(pairs_sum))
            for j in range(len(elements)):
                pairs_sum.append(elements[-1] + elements[j])
    else:
        pairs_sum = [1]
        for i in range(2, n):
            elements.append(choice(pairs_sum))
            for j in range(len(elements) - 1):
                pairs_sum.append(elements[-1] + elements[j])
    return tuple(elements)

def is_random_Fibonacci_sequence(sequence: tuple) -> bool:
    n = len(sequence)
    if sequence[0] != 0:
        return False
    elif n == 1:
        return True
    elif sequence[1] != 1:
        return False
    elif n == 2:
        return True
    elif not sequence[2] in [0, 1, 2]:
        return False
    elif n == 3:
        return True
    elif sequence[2] in [0, 2]:
        pairs_sum = [0, 1, 2]
        for i in range(3, n):
            for j in range(i):
                pairs_sum.append(sequence[j] + sequence[i - 1])
            if not sequence[i] in pairs_sum:
                return False
    else:
        pairs_sum = [1]
        for i in range(3, n):
            for j in range(i - 1):
                pairs_sum.append(sequence[j] + sequence[i - 1])
            if not sequence[i] in pairs_sum:
                return False    
    return True

