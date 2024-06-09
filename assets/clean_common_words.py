f = open('common_words.txt')
words = []
for line in f:
    if line == '\n':
        continue
    word = line.strip('-').strip()
    words.append(word.capitalize())

f.close()

f = open('new_common_word.txt', 'w')
for word in words:
    f.write(word + '\n')
f.close()
