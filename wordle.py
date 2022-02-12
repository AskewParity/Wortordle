from glob import glob
from os import openpty
import random
import math
import time

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
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

def word_weights_into_memory() :
    arr = {}
    with open('shortweights.txt', 'r', encoding='UTF-8') as s_weights :
        content = s_weights.readlines()
        for line in content :
            relation = line.strip().split(" ")
            arr[relation[0]] = float(relation[1])
    return arr

weights = word_weights_into_memory()
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
    'a': [-1, -1, -1, -1, -1],
    'b': [-1, -1, -1, -1, -1],
    'c': [-1, -1, -1, -1, -1],
    'd': [-1, -1, -1, -1, -1],
    'e': [-1, -1, -1, -1, -1],
    'f': [-1, -1, -1, -1, -1],
    'g': [-1, -1, -1, -1, -1],
    'h': [-1, -1, -1, -1, -1],
    'i': [-1, -1, -1, -1, -1],
    'j': [-1, -1, -1, -1, -1],
    'k': [-1, -1, -1, -1, -1],
    'l': [-1, -1, -1, -1, -1],
    'm': [-1, -1, -1, -1, -1],
    'n': [-1, -1, -1, -1, -1],
    'o': [-1, -1, -1, -1, -1],
    'p': [-1, -1, -1, -1, -1],
    'q': [-1, -1, -1, -1, -1],
    'r': [-1, -1, -1, -1, -1],
    's': [-1, -1, -1, -1, -1],
    't': [-1, -1, -1, -1, -1],
    'u': [-1, -1, -1, -1, -1],
    'v': [-1, -1, -1, -1, -1],
    'w': [-1, -1, -1, -1, -1],
    'x': [-1, -1, -1, -1, -1],
    'y': [-1, -1, -1, -1, -1],
    'z': [-1, -1, -1, -1, -1]
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
        #printProgressBar(i + 1, len(session_set))
        arr.append((word, permutation(word), weights[word]))
    return sorted(arr, key=lambda x : x[1] + x[2], reverse=True)


def valid_permutation(word) :
    set = {}
    for i, letter in enumerate(word) :
        sess_in = session_info[letter[0]][i]
        if sess_in != -1 :
            if sess_in == 2 and letter[1] != 2:
                return False
            elif sess_in == -2 and letter[1] == 0:
                return False
            elif sess_in == -3 and letter[1] != 0:
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
            session_info[letter[0]][i] = 2
        elif letter[1] == 1:
            for index in range(5) :
                if session_info[letter[0]][index] != -3 and session_info[letter[0]][index] < 0 :
                    session_info[letter[0]][index] = -2
            session_info[letter[0]][i] = -3
        elif letter[1] == 0:
            alone = True
            for index in range(3 - i) :
                if index != i and guess[index + i + 1][0] == letter[0] and guess[index + i + 1][1] != 0:
                    alone = False
            if alone :
                for index in range(5) :
                    if session_info[letter[0]][index] < 0 and session_info[letter[0]][index] != -2 :
                        session_info[letter[0]][index] = -3
            else :
                session_info[letter[0]][i] = -3  
    start = len(session_set)
    session_set = set_left(guess, word_set=session_set)
    #print(safe_log2(start/len(session_set)))

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
       arr[i] =  (safe_log2(len(session_set)/ arr[i])) * (arr[i]/len(session_set))
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
       arr[i] =  math.root((safe_log2(len(words)/ arr[i]))) * (arr[i]/len(words))
    return sum(arr) // len(arr)


def with_guess_valid(guess, word) :
    for i, letter in enumerate(word):
        val = session_info[word[i]][i]
        if guess[i][1] == 2 and word[i] != guess[i][0] :
            return False
        if val == -3:
            return False
    return True

def valid_word(guess, word) :
    for i, letter in enumerate(guess):
        if letter[1] == 1 and letter[0] not in word:
            return False
        elif letter[1] == 0  and letter[0] in word:
            return False
        elif letter[1] == 2 and letter[0] != word[i] :
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
    global session_info
    global session_set
    avalible_words = []
    with open('init_w.txt', 'r') as file:
        conetent = file.readlines()
        for line in conetent:
            tuple = line.strip().split(' ')
            avalible_words.append((tuple[0], float(tuple[1]), float(tuple[2])))
    avalible_words = sorted(avalible_words, key=lambda x: x[1] + x[2], reverse=True)
    
    while(len(avalible_words) > 1) :
        max = min(10, len(avalible_words))
        for i in range(max) :
            print(avalible_words[i])
        guess = []
        word = input('Input word:\n')
        values = input('Input values:\n')
        for i in range(5) :
            guess.append((word[i], int(values[i])))

        print(guess)
        
        result(guess)
        avalible_words = regen()
    print(avalible_words[0])
    
def histogram(n) :
    global session_info
    avg = 0
    losses = 0
    hist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for _ in range(n) :
        printProgressBar(_ + 1, n)
        try:
            index = simulation() - 1
            hist[index] = hist[index] + 1
        except Exception as e:
            print(e)
            avg += len(hist)
            losses += 1
        session_info = {
    'a': [-1, -1, -1, -1, -1],
    'b': [-1, -1, -1, -1, -1],
    'c': [-1, -1, -1, -1, -1],
    'd': [-1, -1, -1, -1, -1],
    'e': [-1, -1, -1, -1, -1],
    'f': [-1, -1, -1, -1, -1],
    'g': [-1, -1, -1, -1, -1],
    'h': [-1, -1, -1, -1, -1],
    'i': [-1, -1, -1, -1, -1],
    'j': [-1, -1, -1, -1, -1],
    'k': [-1, -1, -1, -1, -1],
    'l': [-1, -1, -1, -1, -1],
    'm': [-1, -1, -1, -1, -1],
    'n': [-1, -1, -1, -1, -1],
    'o': [-1, -1, -1, -1, -1],
    'p': [-1, -1, -1, -1, -1],
    'q': [-1, -1, -1, -1, -1],
    'r': [-1, -1, -1, -1, -1],
    's': [-1, -1, -1, -1, -1],
    't': [-1, -1, -1, -1, -1],
    'u': [-1, -1, -1, -1, -1],
    'v': [-1, -1, -1, -1, -1],
    'w': [-1, -1, -1, -1, -1],
    'x': [-1, -1, -1, -1, -1],
    'y': [-1, -1, -1, -1, -1],
    'z': [-1, -1, -1, -1, -1]
}
    print(hist)
    for i in range(len(hist)) :
        avg += (i + 1) * hist[i]
        if i > 5 :
            losses += hist[i]
    print(avg / n)
    print(losses)
    print(losses * 100 / n)

def simulation() :
    
    count = 0
    global session_set
    session_set = words_into_memory()
    avalible_words = []
    with open('init_w.txt', 'r') as file:
        conetent = file.readlines()
        for line in conetent:
            tuple = line.strip().split(' ')
            avalible_words.append((tuple[0], float(tuple[1]), float(tuple[2])))
    avalible_words = sorted(avalible_words, key=lambda x: x[1] + x[2], reverse=True)
    choice = random.choice(avalible_words)[0]
    print(choice)
    while(len(avalible_words) > 1) :
        chosen = avalible_words[0][0]
        guess = []
        temp = choice
        for i in range(5) :
            if chosen[i] == temp[i] :
                guess.append((chosen[i], 2))
                temp = temp[:i] + "!" + temp[i + 1:]
            elif chosen[i] in temp :
                guess.append((chosen[i], 1))
            else :
                guess.append((chosen[i], 0))
        if count > 10 :
            return count
        if chosen == choice :
            return count + 1
        
        result(guess)
        
        avalible_words = regen()

        count += 1
    if avalible_words[0][0] != choice :
        return 50
    return count + 1

def redo_list():
    weights = {}
    init_l = {}
    with open('shortweights.txt', 'r', encoding='UTF-8') as o_weights :
        content = o_weights.readlines()
        for line in content :
            relation = line.strip().split(" ")
            weights[relation[0]] = float(relation[1])

    with open('init.txt', 'r', encoding='UTF-8') as processesed:
        content = processesed.readlines()
        for line in content :
            relation = line.strip().split(" ")
            init_l[relation[0]] = float(relation[1])
        with open('init_w.txt', 'w', encoding='UTF-8') as new_pros:
            for line in content :
                word = line.split(" ")[0]
                if word in weights :
                    new_pros.write(f'{word} {init_l[word]} {weights[word]}\n')
                else :
                    new_pros.write(f'{word} {init_l[word]} {float(-1)}\n')
    


if __name__ == '__main__':
    curr = time.time()
    histogram(100)
    print(time.time() - curr)