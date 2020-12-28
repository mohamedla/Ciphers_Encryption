from tkinter import *
import sys
import random
import re

class MyWindow:
    error = ''
    def __init__(self, win):
        self.lbl1=Label(win, text='Mode')
        self.lbl2=Label(win, text='Massage')
        self.lbl4=Label(win, text='Key')
        self.lbl3=Label(win, text='Result')
        self.info1=Label(win, text='Do you wish to encrypt(e) or decrypt(d) a message?')
        self.einfo=Label(win, text=self.error)
        self.scrollbar = Scrollbar(orient=VERTICAL)
        self.t1=Entry(bd=3, xscrollcommand = self.scrollbar.set)
        self.t2=Text(bd=3)
        self.t4=Entry(bd=3)
        self.t3=Text(bd=3)
        self.t3.config(state='disabled')
        self.info1.place(x=100, y=10)
        self.lbl1.place(x=100, y=40)
        self.t1.place(x=200, y=40 ,width=250,)
        self.lbl2.place(x=100, y=80)
        self.t2.place(x=200, y=80 ,width=250,height=180)
        self.lbl4.place(x=100, y=270)
        self.t4.place(x=200, y=270 ,width=250)
        self.b1=Button(win, text='Caesar', command=self.getCaesarTranslatedMessage)
        self.b2=Button(win, text='Monoalphabetic', command = self.getMonoalphabeticTranslatedMessage)
        self.b3 = Button(win, text='Playfair', command = self.getPlayfairTranslatedMessage)
        self.b4 = Button(win, text='Vigenere', command = self.getVigenereTranslatedMessage)
        self.b5 = Button(win, text='Rail Fence', command = self.getRailFenceTranslatedMessage)
        self.b1.place(x=240, y=300)
        self.b2.place(x=320, y=300)
        self.b3.place(x=210, y=340)
        self.b4.place(x=290, y=340)
        self.b5.place(x=370, y=340)
        self.lbl3.place(x=100, y=400)
        self.t3.place(x=200, y=400 ,width=250,height=180)
        self.einfo.place(x=100, y=410)

    def getMode(self):
        mode = self.t1.get().lower()
        if mode in 'encrypt e decrypt d'.split():
            return mode
        else:
            self.error = 'Enter either "encrypt" or "e" or "decrypt" or "d".'

    def getMessage(self):
        message = self.t2.get('1.0','end')
        return str(message)

    def getKey(self):
        key = self.t4.get()
        return key

    def checkValidKey(self):
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        key = self.getKey().upper()
        keyList = list(key)
        lettersList = list(LETTERS)
        keyList.sort()
        lettersList.sort()
        if keyList != lettersList:
            return 0
        else:
            return 1

# Ciphers
#     Ceaser Cipher
    def getCaesarTranslatedMessage(self):
        mode = self.getMode()
        message =self.getMessage()
        key = int(self.getKey())
        if (key >= 1 and key <= 26):
            if mode[0] == 'd':
                key = -key
            translated = ''
            for symbol in message:
                if symbol.isalpha():
                    num = ord(symbol)
                    num += key
                    if symbol.isupper():
                        if num > ord('Z'):
                            num -= 26
                        elif num < ord('A'):
                            num += 26
                    elif symbol.islower():
                        if num > ord('z'):
                            num -= 26
                        elif num < ord('a'):
                            num += 26
                    translated += chr(num)
                else:
                    translated += symbol
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')
            
    # Monoalphabetic Cipher
    def getMonoalphabeticTranslatedMessage(self):
        mode = self.getMode()
        message = self.getMessage()
        key = self.getKey()
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.checkValidKey():
            translated = ''
            charsA = LETTERS
            charsB = key.upper()
            if mode[0] == 'd':
                char = charsA
                charsA = charsB
                charsB = char
            for symbol in message:
                if symbol.isalpha():
                    if symbol.upper() in charsA:
                        symIndex = charsA.find(symbol.upper())
                        if symbol.isupper():
                            translated += charsB[symIndex].upper()
                        else:
                            translated += charsB[symIndex].lower()
                    else:
                        translated += symbol
                else:
                    translated += symbol
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')
#   Playfair Cipher
    def getPlayfairTranslatedMessage(self):
        mode = self.getMode()
        message = self.getMessage()
        key = self.getKey()
        key = key.replace(" ", "")
        key = key.upper()

        message = message.upper()
        message = 'X'.join(re.findall(r"(?i)\b[a-z]+\b", message))
        def matrix(x, y, initial):
            return [[initial for i in range(x)] for j in range(y)]

        result = list()
        for c in key:  # storing key
            if c not in result:
                if c == 'J':
                    result.append('I')
                else:
                    result.append(c)

        flag = 0
        for i in range(65, 91):  # storing other character
            if chr(i) not in result:
                if i == 73 and chr(74) not in result:
                    result.append("I")
                    flag = 1
                elif flag == 0 and i == 73 or i == 74:
                    pass
                else:
                    result.append(chr(i))

        k = 0
        my_matrix = matrix(5, 5, 0)  # initialize matrix
        for i in range(0, 5):  # making matrix
            for j in range(0, 5):
                my_matrix[i][j] = result[k]
                k += 1

        def locindex(c):  # get location of each character
            loc = list()
            if c == 'J':
                c = 'I'
            for i, j in enumerate(my_matrix):
                for k, l in enumerate(j):
                    if c == l:
                        loc.append(i)
                        loc.append(k)
                        return loc

        if mode[0] == 'e':
            translated = ''
            i = 0
            for s in range(0, len(message) + 1, 2):
                if s < len(message) - 1:
                    if message[s] == message[s + 1]:
                        message = message[:s + 1] + 'X' + message[s + 1:]
            if len(message) % 2 != 0:
                message = message[:] + 'X'
            while i < len(message):
                loc = list()
                loc = locindex(message[i])
                loc1 = list()
                loc1 = locindex(message[i + 1])
                if loc[1] == loc1[1]:
                    translated += my_matrix[(loc[0] + 1) % 5][loc[1]]
                    translated += my_matrix[(loc1[0] + 1) % 5][loc1[1]]
                elif loc[0] == loc1[0]:
                    translated += my_matrix[loc[0]][(loc[1] + 1) % 5]
                    translated += my_matrix[loc1[0]][(loc1[1] + 1) % 5]
                else:
                    translated += my_matrix[loc[0]][loc1[1]]
                    translated += my_matrix[loc1[0]][loc[1]]
                i = i + 2
            translated = translated.lower()
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')
        elif mode[0] == 'd':
            translated = ''
            i = 0
            while i < len(message):
                loc = list()
                loc = locindex(message[i])
                loc1 = list()
                loc1 = locindex(message[i + 1])
                if loc[1] == loc1[1]:
                   translated += my_matrix[(loc[0] - 1) % 5][loc[1]]
                   translated += my_matrix[(loc1[0] - 1) % 5][loc1[1]]
                elif loc[0] == loc1[0]:
                    translated += my_matrix[loc[0]][(loc[1] - 1) % 5]
                    translated += my_matrix[loc1[0]][(loc1[1] - 1) % 5]
                else:
                    translated += my_matrix[loc[0]][loc1[1]]
                    translated += my_matrix[loc1[0]][loc[1]]
                i = i + 2
            translated = translated.lower()
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')

#   Playfair Cipher
    def getVigenereTranslatedMessage(self):
        mode = self.getMode()
        message = self.getMessage()
        message = message.lower()
        key = self.getKey()
        alphabets = "abcdefghijklmnopqrstuvwxyz"
        translated = ''
        if key.isalpha():
            kpos = []
            if mode[0] == 'e':
                for x in key:
                    kpos.append(alphabets.find(x))
                i = 0
                for x in message:
                    if x.isalpha():
                        if i == len(kpos):
                            i = 0
                        pos = alphabets.find(x) + kpos[i]
                        if pos > 25:
                            pos = pos - 26
                        translated += alphabets[pos].capitalize()
                        i += 1
                    else:
                        translated += x
            elif mode[0] == 'd':
                for x in key:
                    kpos.append(alphabets.find(x))
                i = 0
                for x in message:
                    if i == len(kpos):
                        i = 0
                    pos = alphabets.find(x.lower()) - kpos[i]
                    if pos < 0:
                        pos = pos + 26
                    translated += alphabets[pos].lower()
                    i += 1
        translated = translated.lower()
        self.t3.config(state='normal')
        self.t3.delete('1.0','end')
        self.t3.insert(END, str(translated))
        self.t3.config(state='disabled')
#   Rail Fence Cipher
    def getRailFenceTranslatedMessage(self):
        mode = self.getMode()
        message = self.getMessage()
        key = self.getKey()
        key = int(key)

        row, col = 0, 0
        rail = [['\n' for i in range(len(message))] for j in range(key)]
        if mode[0] == 'e':
            dir_down = False
            for i in range(len(message)):
                if (row == 0) or (row == key - 1):
                    dir_down = not dir_down
                rail[row][col] = message[i]
                col += 1
                if dir_down:
                    row += 1
                else:
                    row -= 1
            result = []
            for i in range(key):
                for j in range(len(message)):
                    if rail[i][j] != '\n':
                        result.append(rail[i][j])
            translated = "".join(result)
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')
        elif mode[0] == 'd':
            dir_down = None
            for i in range(len(message)):
                if row == 0:
                    dir_down = True
                if row == key - 1:
                    dir_down = False
                rail[row][col] = '*'
                col += 1
                if dir_down:
                    row += 1
                else:
                    row -= 1
            index = 0
            for i in range(key):
                for j in range(len(message)):
                    if ((rail[i][j] == '*') and
                            (index < len(message))):
                        rail[i][j] = message[index]
                        index += 1
            result = []
            row, col = 0, 0
            for i in range(len(message)):
                if row == 0:
                    dir_down = True
                if row == key - 1:
                    dir_down = False
                if (rail[row][col] != '*'):
                    result.append(rail[row][col])
                    col += 1
                if dir_down:
                    row += 1
                else:
                    row -= 1
            translated = "".join(result)
            self.t3.config(state='normal')
            self.t3.delete('1.0','end')
            self.t3.insert(END, str(translated))
            self.t3.config(state='disabled')


window=Tk()
mywin=MyWindow(window)
window.title('Hello Python')
window.geometry("550x600+10+10")
window.resizable(width = False , height = False) 
window.mainloop()
