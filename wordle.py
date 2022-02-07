from mimetypes import guess_all_extensions
from operator import le
import os
import math
from re import X

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print('\n')


#Yee Yee
O_WEIGHTS = 'shortweights.txt'

def words_into_memory() :
    arr = set()
    with open(O_WEIGHTS, 'r', encoding='UTF-8') as o_weights :
        content = o_weights.readlines()
        for line in content :
            relation = line.strip().split(" ")
            arr.add(relation[0])
    return arr

words = words_into_memory()
session_set = words_into_memory()


'''
Words will look like this,  will assume 1s dont count occurences
guess = [
    H, 2
    E, 0
    L, 1
    L, 1
    O, 2 
]
'''
session_info = {
    'a': -1,
    'b': -1,
    'c': -1,
    'd': -1,
    'e': -1,
    'f': -1,
    'g': -1,
    'h': -1,
    'i': -1,
    'j': -1,
    'k': -1,
    'l': -1,
    'm': -1,
    'n': -1,
    'o': -1,
    'p': -1,
    'q': -1,
    'r': -1,
    's': -1,
    't': -1,
    'u': -1,
    'v': -1,
    'w': -1,
    'x': -1,
    'y': -1,
    'z': -1
}



def safe_log2(x) :
    return math.log2(x) if x > 0 else 0

def initialize() :
    #temporary for testing I know which thing is the best right now
    with open('test.txt', 'w', encoding='UTF-8') as file :
        for i, word in enumerate(words) :
            printProgressBar(i, len(words), prefix="Finding the best word")
            file.write(f'{word} {init_permutations(word)}\n')

def regen():
    arr = []
    for i, word in enumerate(session_set) :
        printProgressBar(i + 1, len(session_set))
        arr.append((word, permutation(word)))
    return sorted(arr, key=lambda x : x[1], reverse=True)


def valid_permutation(word) :
    set = {}
    for letter in word :
        if session_info[letter[0]] != -1 :
            if session_info[letter[0]] > -1 and letter[1] == 0:
                return False
            elif session_info[letter[0]] == -2 and letter[1] == 0:
                return False
            elif session_info[letter[0]] == -3 and letter[1] != 0:
                return False
        if letter[0] not in set :
            set[letter[0]] = letter[1]
        elif set[letter[0]] == 0 and letter[1] != 0:
            return False
        elif set[letter[0]] != 0 and letter[1] == 0:
            return False
    return True

def result(guess) :
    global session_info
    global session_set
    for i, letter in enumerate(guess) :
        if letter[1] == 2:
            session_info[letter[0]] = i
        elif letter[1] == 1:
            session_info[letter[0]] = -2
        elif letter[1] == 0:
            session_info[letter[0]] = -3

    session_set = set_left(guess, word_set=session_set)

#same as init perm but probably has to change
def permutation(word) :
    arr = [] 
    for i in range(3) :
        for j in range(3) :
            for k in range(3) :
                for l in range(3) :
                    for m in range(3) :
                        perm = [(word[0], i), (word[1], j), (word[2], k), (word[3], l), (word[4], m)]
                        if valid_permutation(perm) :
                            arr.append(number_left(perm, session_set))
    arr = list(filter(lambda a: a != 0, arr))
    for i in range(len(arr)) :
       arr[i] =  (-1 * safe_log2(arr[i]/len(words))) * (arr[i]/len(words))
    return sum(arr)

def init_permutations(word) :
    arr = [] 
    for i in range(3) :
        for j in range(3) :
            for k in range(3) :
                for l in range(3) :
                    for m in range(3) :
                        perm = [(word[0], i), (word[1], j), (word[2], k), (word[3], l), (word[4], m)]
                        if valid_permutation(perm) :
                            arr.append(number_left(perm))
    arr = list(filter(lambda a: a != 0, arr))
    for i in range(len(arr)) :
       arr[i] =  (-1 * safe_log2(arr[i]/len(words))) * (arr[i]/len(words))
    return sum(arr)


def with_guess_valid(guess, word) :
    for i, letter in enumerate(guess):
        if letter[1] == 0 and letter[0] in word :
            return False
        elif letter[1] == 2 and letter[0] != word[i] :
            return False
        elif letter[1] == 1 and (letter[0] not in word or word[i] == letter[0]):
            return False
    return True

def valid_word(guess, word) :
    for i, letter in enumerate(guess):
        if letter[1] == 0 and letter[0] in word :
            return False
        elif letter[1] == 2 and letter[0] != word[i] :
            return False
        elif letter[1] == 1 and letter[0] not in word :
            return False
    return True

def set_left(guess, word_set=words) :
    n_words = set()
    for word in word_set :
        if with_guess_valid(guess, word) :
            n_words.add(word)
    return n_words    

def number_left(guess, word_set=words) :
    count = 0
    for word in word_set :
        if valid_word(guess, word) :
            count += 1
    return count     
                
def order_o_weights() :
    arr = []
    with open(O_WEIGHTS, 'r', encoding='UTF-8') as o_weights :
        content = o_weights.readlines()
        for line in content :
            relation = line.strip().split(" ")
            if float(relation[1]) > 0 :
                arr.append((relation[0], float(relation[1])))
    return sorted(arr, key=lambda l : l[1])

def session() :
    global session_set
    avalible_words = []
    with open('init.txt', 'r') as file:
        conetent = file.readlines()
        for line in conetent:
            tuple = line.strip().split(' ')
            avalible_words.append((tuple[0], tuple[1]))
    avalible_words = sorted(avalible_words, key=lambda x: x[1], reverse=True)
    
    while(len(avalible_words) > 1) :
        max = min(10, len(avalible_words))
        for i in range(max) :
            print(avalible_words[i])
        print('Insert Result: ')
        guess = []
        for _ in range(5):
            letter = []
            letter.append(input('Letter\n'))
            letter.append(input('MISS - 0\nMISPLACE - 1\nEXACT - 2\n'))
            guess.append((letter[0], int(letter[1])))
            print(guess)
        result(guess)
        
        avalible_words = regen()
    print(avalible_words[0])
    

if __name__ == '__main__':
    session()