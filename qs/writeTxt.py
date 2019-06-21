def open_txt():
    global f
    f = open('data.csv', mode='a', encoding='ISO-8859-1')


def close_txt():
    global f
    f.close()


def write_to_txt(list):
    global f
    string = ','.join(list)
    # print(temp)
    f.write(string + '\n')
