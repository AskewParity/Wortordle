#just a utility to do anything

def js_word_arr() :
    string = '['
    with open('init_w.txt', 'r', encoding='UTF-8') as o_weights :
        content = o_weights.readlines()
        for line in content :
            relation = line.strip().split(" ")
            string += f"['{relation[0]}', {relation[1]}, {relation[2]}], "
    string = string[0:len(string) - 2] + ']'
    return string

if __name__ == "__main__":
    print(js_word_arr())