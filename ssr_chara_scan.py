import codecs
file = codecs.open("text.txt", "r", "utf8")
data = file.readlines()

names = []
for name in data:
    name = name[:-8]
    option = "none"
    if '(' in name:
        start = name.find('(')
        end = name.find(')')
        option = name[start+1:end]

        if option[1] == '属':
           option = option[0]
        elif option[-3:] == 'ver':
            option = option[:-3]
        else:
            print(option, "ERROR!")

        name = name[:start]
    names.append([name,option])
