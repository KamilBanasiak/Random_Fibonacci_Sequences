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

def probability_of_getting_RF_sequence(sequence: tuple, sampling_with_replacement = True): #element by element
    if not is_random_Fibonacci_sequence(sequence):
        return 0
    if sequence in [(0), (0,1)]:
        return 1
    score = probability_of_getting_RF_sequence(sequence[:len(sequence)-1], sampling_with_replacement)
    seq = Random_Fibonacci_Sequences(sequence[:len(sequence)-1], sampling_with_replacement)
    return score * seq.probability_of_next_element(sequence[-1]) 

def get_RFS_whose_sum_is_m(n: int, m: int, sampling_with_replacement = True) -> list:
    if n <= 0 or m < 0:
        return None
    if n == 1 and m == 0:
        return [(0)]
    if (n > 1 and m == 0) or (n == 1 and m > 0):
        return None
    if n == 2 and m == 1:
        return [(0, 1)]
    if n == 2 and m > 1:
        return None
    still_possible = True
    sequences = [(0, 1)]
    sequences_possible_pairs_sum = [Random_Fibonacci_Sequences(sequences[0], sampling_with_replacement).pairs_sum]    
    i = 2
    while i < n:
        if not sequences:
            still_possible = False
            break
        new_list = []
        new_lists = []
        for index, sequence in enumerate(sequences):
            for pair_sum in sequences_possible_pairs_sum[index]:
                if sum(sequence) + pair_sum <= m:
                    new_list.append(sequence + tuple([pair_sum]))
                    new_lists.append(Random_Fibonacci_Sequences(new_list[-1], sampling_with_replacement).pairs_sum)
        sequences = new_list
        sequences_possible_pairs_sum = new_lists
        i += 1
    if still_possible:
        final = list(set([sequence for sequence in sequences if sum(sequence) == m]))
        if final:
            return final
        else:
            return None
    else:
        return None
    
# set of nRFS = {sequence in RFS: len(sequence) == n}
def probability_of_getting_sequence_whose_sum_is_m_from_set_of_nRFS(n: int, m: int, sampling_with_replacement = True):
    number_of_all_nRFS = how_many_RFS(n, sampling_with_replacement)
    nRFS_whose_sum_is_m = get_RFS_whose_sum_is_m(n, m, sampling_with_replacement)
    if nRFS_whose_sum_is_m:
        return len(nRFS_whose_sum_is_m) / number_of_all_nRFS
    else:
        return 0
    
def probability_of_getting_nRF_sequence_whose_sum_is_m(n: int, m: int, sampling_with_replacement = True):
    # element by element
    probability = 0
    sequences = get_RFS_whose_sum_is_m(n, m, sampling_with_replacement)
    if sequences:
        for sequence in sequences:
            probability += probability_of_getting_RF_sequence(sequence, sampling_with_replacement)
    return probability


def enter_n():
    n = int(input('Enter n as a positive natural number: '))
    while not (isinstance(n, int) and n > 0):
        print('Try again')
        n = int(input('Enter n as a positive natural number: '))
    return n

def enter_m():
    m = int(input('Enter m as a natural number: '))
    while not (isinstance(m, int) and m >= 0):
        print('Try again')
        m = int(input('Enter m as a natural number: '))
    return m    

def enter_way_of_sampling():
    sampling_with_replacement = input('Sampling with replacement? (Yes/No): ')
    while not sampling_with_replacement in ['Yes', 'No']:
        print('Try again')
        sampling_with_replacement = input('Sampling with replacement? (Yes/No): ')
    return True if sampling_with_replacement == 'Yes' else False

def enter_sequence():
    sequence = input('Enter sequence (for example: 0, 1, 2, 3): ')
    correct = False
    while not correct:
        sequence = sequence.split(', ')
        correct = True
        for i in range(len(sequence)):
            if i == 0:
                if sequence[0][0] == ' ':
                    sequence[0] = sequence[0][1:]
            try:
                sequence[i] = int(sequence[i])
            except:
                print('Try again')
                sequence = input('Enter sequence (for example: 0, 1, 2, 3): ')
                correct = False
                break
    return tuple(sequence)

def main():
    options = {'start menu': ['1. Generate a random Fibonacci sequence', '2. Check a sequence',
                              '3. Enter a sequence', '4. Pass a number of random Fibonacci sequences',
                              '5. Calculate probability of getting the sequence',
                              '6. Pass random Fibonacci sequences whose sum of elements is m',
                              '7. Calculate probability of sampling a sequence whose sum is m from set of RFS',
                              '8. Calculate probability of getting a sequence whose sum is m',
                              '9. Finish work'],
                'entering': ['1. Generate a random Fibonacci sequence and enter it',
                             '2. Check and enter sequence'],
                'work with sequence': ['1. Display: sequence, way of sampling, list of possible next element of sequence',
                                       '2. Change the sequence', '3. Change the way of sampling if it is possible',
                                       '4. Lengthen the sequence', '5. Calculate sum of elements',
                                       '6. Calculate probability that the next element of this sequence is m',
                                       '7. Return to the menu', '8. Finish work']}
    menu = 'start menu'
    print('Choose options by entering a number')
    while True:
        for option in options[menu]:
            print(option)
        decision = int(input('What do you want now? '))
        if not decision in [i for i in range(1, len(options[menu])+1)]:
            print('Try again')
            continue
        if menu == 'start menu' and decision == 1:
            n = enter_n()
            sampling_with_replacement = enter_way_of_sampling()
            print(generate_random_Fibonacci_sequence(n, sampling_with_replacement))
        elif menu == 'start menu' and decision == 2:
            sequence = enter_sequence()
            if is_random_Fibonacci_sequence(sequence):
                print('Yes, it is a random Fibonacci sequence')
            else:
                print('No, it is not a random Fibonacci sequence')
        elif menu == 'start menu' and decision == 4:
            n = enter_n()
            sampling_with_replacement = enter_way_of_sampling()
            print(how_many_RFS(n, sampling_with_replacement))
        elif menu == 'start menu' and decision == 5:
            sequence = enter_sequence()
            sampling_with_replacement = enter_way_of_sampling()
            print(probability_of_getting_RF_sequence(sequence, sampling_with_replacement))
        elif menu == 'start menu' and decision == 6:
            n = enter_n()
            m = enter_m()
            sampling_with_replacement = enter_way_of_sampling()
            print(get_RFS_whose_sum_is_m(n, m, sampling_with_replacement))
        elif menu == 'start menu' and decision == 7:
            n = enter_n()
            m = enter_m()
            sampling_with_replacement = enter_way_of_sampling()
            print(probability_of_getting_sequence_whose_sum_is_m_from_set_of_nRFS(n, m, sampling_with_replacement))         
        elif menu == 'start menu' and decision == 8:
            n = enter_n()
            m = enter_m()
            sampling_with_replacement = enter_way_of_sampling()
            print(probability_of_getting_nRF_sequence_whose_sum_is_m(n, m, sampling_with_replacement))            
        elif (menu == 'start menu' and decision == 9) or (menu == 'work with sequence' and decision == 8):
            break
        elif menu == 'start menu' and decision == 3:
            menu = 'entering'
        elif menu == 'entering' and decision == 1:
            n = enter_n()
            sampling_with_replacement = enter_way_of_sampling()
            sequence = generate_random_Fibonacci_sequence(n, sampling_with_replacement)
            print(sequence)
            menu = 'work with sequence'
            seq = Random_Fibonacci_Sequences(sequence, sampling_with_replacement)
        elif menu == 'entering' and decision == 2:
            sequence = enter_sequence()
            if is_random_Fibonacci_sequence(sequence):
                menu = 'work with sequence'
                seq = Random_Fibonacci_Sequences(sequence, sampling_with_replacement)
            else:
                print('Try again later')
        elif menu == 'work with sequence' and decision == 1:
            print(f'Sequence: {seq.sequence}')
            if seq.sampling_with_replacement:
                sampling = 'sampling with replacement'
            else:
                sampling = 'sampling without replacement'
            print(f'Way of sampling: {sampling}')
            print(f'List of possible next element of sequence: {list(set(seq.pairs_sum))}')
        elif menu == 'work with sequence' and decision == 2:
            menu = 'entering'
        elif menu == 'work with sequence' and decision == 3:
            sampling_with_replacement = enter_way_of_sampling()
            seq.sampling_with_replacement = sampling_with_replacement
        elif menu == 'work with sequence' and decision == 4:
            seq.get_longer()
            print(seq.sequence)
        elif menu == 'work with sequence' and decision == 5:
            print(seq.elements_sum())
        elif menu == 'work with sequence' and decision == 6:
            m = enter_m()
            print(seq.probability_of_next_element(m))
        elif menu == 'work with sequence' and decision == 7:
            menu = 'start menu'

if __name__ == '__main__':
    main()