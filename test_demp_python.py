# తప్పు 1: ఏ ఫైల్ ని ఓపెన్ చేస్తున్నామో ఆ 'file path' ని చెక్ చేయడం లేదు
# తప్పు 2: ఒకవేళ ఫైల్ లేకపోతే, ప్రోగ్రామ్ క్రాష్ అవుతుంది (Error handling లేదు)

def read_file_demo(filename):
    f = open(filename, 'r')
    return f.read()

# దీన్ని వాడే విధానంలో కూడా తప్పు ఉంది
data = read_file_demo("non_existent_file.txt")
print(data)
