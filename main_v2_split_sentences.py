#import library
import numpy as np
import math
import pandas as pd
import re
from collections import Counter
import os


def buildUnigramModel(text):
    '''
    BUILD UNIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model unigram yang dibuat dalam bentuk dictionary (key: kata; value: probabilitas kemunculan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    dataset = ' '.join(text).lower().strip()
    dataset = re.split(r'\W+', dataset)
    word_probability = dict(Counter(dataset))
    n = sum(word_probability.values())
    word_probability = {key: val / n for key, val in word_probability.items()}
    return word_probability


def buildBigramModel(text):
    '''
    BUILD BIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model bigram yang dibuat dalam bentuk dictionary (key: pasangan kata; value: probabilitas kemunculan pasangan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    start = '<start>'
    end =   '<end>'
    dataset = []     
    for data in text:
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',data.lower().strip())
        for sentence in sentences :
            dataset.append(start)
            dataset = dataset + re.split(r'\W+',sentence)
            dataset.append(end)
    bigrams = [(dataset[i+1],dataset[i]) for i in range(len(dataset)-1)]
    unigram_count = dict(Counter(dataset))
    bigram_count  = dict(Counter(bigrams))
    bigrams = {key: val/unigram_count[key[1]] for key, val in bigram_count.items()}
    return bigrams


def nextBestWord(bigramModel, currentWord):
    '''
    MENAMPILKAN NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Meng-outputkan kata berikutnya yang memiliki probabilitas tertinggi berdasarkan model bigram
    '''
    temp = {key[0]: val for key, val in bigramModel.items() if key[1]
            == currentWord}
    return max(temp, key=temp.get)


def nextTenBestWords(bigramModel, currentWord, n = 10):
    '''
    MENYIMPAN TOP 10 NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Menghasilkan list berisi 10 kata berikutnya (beserta probabilitasnya) dengan probabilitas tertinggi berdasarkan model bigram. 
    '''
    temp = {key: val for key, val in sorted(bigramModel.items(), key=lambda item: item[1],reverse=True) if key[1] == currentWord}
    temp = dict(list(temp.items())[:n]) 
    return temp


def generateSentence(bigramModel, length):
    '''
    GENERATE SENTENCE
    IS : Menerima input model bigram dan panjang kalimat yang ingin di-generate
    FS : Mengembalikan kalimat dengan panjang sesuai inputan
    Note : Generate sentence
    '''
    big3 = list(nextTenBestWords(bigramModel, '<start>',n=33))
    k = np.random.randint(0, len(big3))
    sentences = [big3[k][0]]
    for i in range(1, length):
        current = sentences[i-1]
        big3 = list(nextTenBestWords(bigramModel, current))[:3]
        k = np.random.randint(0, len(big3))
        sentences.append(big3[k][0])
    return ' '.join(sentences)


if __name__ == '__main__':
    print("TUGAS LANGUAGE MODELING NLP - SFY")
    print("SILAKAN MASUKKAN IDENTITAS ANDA")
    Nama = input("NAMA : ")
    NIM = input("NIM : ")

    os.system("pause")
    os.system("cls")

    #import dataset
    data = pd.read_csv('text.csv')

    print("TUGAS 1. TAMPILKAN 5 BARIS PERTAMA DARI DATASET")
    print()
    print("HASIL : ")
    print(data.head())

    os.system("pause")
    os.system("cls")

    print("TUGAS 2. BUAT MODEL UNIGRAM")
    print()
    print("HASIL : ")
    print(buildUnigramModel(data['text']))

    os.system("pause")
    os.system("cls")

    print("TUGAS 3. BUAT MODEL BIGRAM")
    print()
    print("HASIL : ")
    bigramModel = buildBigramModel(data['text'])
    print(bigramModel)

    os.system("pause")
    os.system("cls")

    print("TUGAS 4. MENAMPILKAN NEXT BEST WORD")
    print()
    print("HASIL : ")
    print("of -> ", nextBestWord(bigramModel, "of"))
    print("update -> ", nextBestWord(bigramModel, "update"))
    print("hopes -> ", nextBestWord(bigramModel, "hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 5. TOP 10 BEST NEXT WORD")
    print()
    print("HASIL : ")
    print("of -> ", nextTenBestWords(bigramModel, "of"))
    print("update -> ", nextTenBestWords(bigramModel, "update"))
    print("hopes -> ", nextTenBestWords(bigramModel, "hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 6. GENERATE KALIMAT")
    print()
    n = int(input("Panjang Kalimat : "))
    print("HASIL : ")
    print(generateSentence(bigramModel, n))

    os.system("pause")
    os.system("cls")

    print("SELAMAT", Nama, "ANDA SUDAH MENYELESAIKAN TUGAS LANGUAGE MODELING NLP-SFY")
