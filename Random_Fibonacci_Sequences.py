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
    pairs_sum = [0, 1, 2]
    for i in range(3, n):
        for j in range(i):
            pairs_sum.append(sequence[j] + sequence[i - 1])
        if not sequence[i] in pairs_sum:
            return False  
    return True

class Random_Fibonacci_Sequences:
    def __init__(self, sequence, sampling_with_replacement = True):
        self.sequence = sequence
        self.__length = len(self.sequence)
        self.sampling_with_replacement = sampling_with_replacement       
        self.pairs_sum = self.possible_pairs_sum()
        
    @property
    def sequence(self):
        return self._sequence
    
    @sequence.setter
    def sequence(self, new_sequence):
        if is_random_Fibonacci_sequence(new_sequence):
            self._sequence = new_sequence
            
    @property
    def sampling_with_replacement(self):
        return self._sampling_with_replacement
    
    @sampling_with_replacement.setter
    def sampling_with_replacement(self, new_sampling_with_replacement):
        help_list = [2*element for element in self.sequence]
        prev_elements = [0, 1]
        sampling_with_replacement = False
        for i in range(2, self.__length):
            if self.sequence[i] in help_list and str(prev_elements).find(str(self.sequence[i]//2), str(prev_elements).find(str(self.sequence[i]//2)) + 1) != -1:
                sampling_with_replacement = True
                break
        if sampling_with_replacement:
            if new_sampling_with_replacement:
                self._sampling_with_replacement = new_sampling_with_replacement
        else:
            self._sampling_with_replacement = new_sampling_with_replacement
        
    def possible_pairs_sum(self):
        help_list = []
        if self.sampling_with_replacement:
            for index, element in enumerate(self.sequence):
                for element2 in self.sequence[:index + 1]:
                    help_list.append(element + element2)
        else:
            for index, element in enumerate(self.sequence):
                for element2 in self.sequence[:index]:
                    help_list.append(element + element2) 
        return help_list
        
    def get_longer(self):
        if self.__length == 1:
            element = 1
        else:
            element = choice(self.pairs_sum)
        self.sequence += tuple([element])
        self.__length += 1
        self.pairs_sum = self.possible_pairs_sum()
        
    def elements_sum(self):
        return sum(self.sequence)
    
    def probability_of_next_element(self, n):
        if not isinstance(n, int):
            return 0
        if n < 0:
            return 0
        if self.__length == 1 and n != 1:
            return 0
        if self.__length == 1 and n == 1:
            return 1
        if not n in self.pairs_sum:
            return 0
        return self.pairs_sum.count(n)/len(self.pairs_sum)
    
def how_many_RFS(n: int, sampling_with_replacement: bool) -> int:
    if n == 0:
        return 0
    if n in [1, 2]:
        return 1
    current_list = [Random_Fibonacci_Sequences((0, 1), sampling_with_replacement)]
    i = 2
    while n > i:
        new_list = []
        for sequence in current_list:
            for future_element in set(sequence.pairs_sum):
                new_list.append(Random_Fibonacci_Sequences(sequence.sequence +tuple([future_element]), sampling_with_replacement))
        current_list = new_list
        i += 1
    return len(current_list)

def probability_of_getting_RF_sequence(sequence: tuple, sampling_with_replacement = True) -> float: #element by element
    if not is_random_Fibonacci_sequence(sequence):
        return 0
    if sequence in [(0), (0,1)]:
        return 1
    score = probability_of_getting_RF_sequence(sequence[:len(sequence)-1], sampling_with_replacement)
    seq = Random_Fibonacci_Sequences(sequence[:len(sequence)-1], sampling_with_replacement)
    return score * seq.probability_of_next_element(sequence[-1])                                       