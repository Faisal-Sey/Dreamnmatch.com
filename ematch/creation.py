
import re
sentence = "What's the password katappa: 'KATAPPA 123'!, cried katappa \nSo Bhallaldev fled"
dict = dict()
first_sentence = re.sub(r"[,#$^&*+!:]", '', sentence)
remove1 = re.sub(r"[\n\t\r\f\v]", '', first_sentence)


dict1 = []
dict2 = []
dict3 = []



def find_indices_of(char, in_string):
    index = -1
    while True:
        index = in_string.find(char, index + 1)
        if index == -1:
            break
        yield index


for i in find_indices_of("'", remove1):
    dict1.append(i)


for value in dict1:
    if remove1[int(value-1)] == " " or remove1[int(value + 1)] == " ":
        dict2.append(value)


i = 0
if i == 0:
    for quote in dict2:
        string = remove1[:quote-i] + '' + remove1[quote+1-i:]
        remove1 = string
        dict3.append(remove1)
        i = i + 1

final_sentence = dict3[-1]
for word in final_sentence.lower().split():
    if word in dict:
        dict[word] += 1

    else:
        dict[word] = 1

print(dict)


