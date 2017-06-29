import codecs
file = codecs.open("text2.txt", "r", "utf8")
data = file.readlines()

names = []
count = 0
for name in data:
    name = name.replace('\r\n','')
    print(name)
    if name == '' or name == '【個別ページ】':
        print('continue')
        continue
    elif '(' in name:
        print('option',name[1:-1])
        names[count].append(name[1:-1])
        count+=1
    else:
        print(name)
        names.append([name])
