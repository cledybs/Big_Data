
import nltk
import random
import os

#nltk.download('words')
word_list = nltk.corpus.words.words()

def generate_random_words(N):
    random_words = random.choices(word_list, k=N)
    return random_words

def instertDoc(w,f,c):
    nr = random.randint(3, 11)
    for i in range(nr):
        nrt =random.randint(0, c-1)
        if(f == nrt):
            continue
        w.append("doc"+str(nrt))

def rute(strr):

    nombre_carpeta = 'docs'
    ruta_archivo = os.path.join(nombre_carpeta, strr)
    return ruta_archivo

def save_to_file(filename,c):
    N = 15000
    for f in range(c):
        t =filename + str(f) 
        arr= rute(t)
        with open(arr, 'w') as file:
            words = generate_random_words(N) * 6
            instertDoc(words,f,c)
            words.insert(0, "\t")
            words.insert(0, t)
            file.write(' '.join(words))

if __name__ == "__main__":
    save_to_file('doc',50)
    #print(len(word_list)) #236736

