from tkinter import *
import ctypes
import random
import tkinter
import math
import re

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # for high resolution

root = Tk()
root.title("Type Speed Test")

root.geometry("1200x300")  # make it wide instead of tall
root.option_add("*Label.Font", "consolas 20")
root.option_add("*Button.Font", "consolas 20")

splitPoint = 0
passedSeconds = 0
writeAble = True
text = ""

def resetWritingLabels():
    global text, splitPoint, labelLeft, labelRight, currentLetterLabel, timeleftLabel, writeAble, passedSeconds
    splitPoint = 0
    passedSeconds = 0
    writeAble = True

    # Pool of sentences
    possibleSentences = [
        'For writers a random sentence can help them get their creative juices flowing',
        'The goal of Python Code is to provide Python tutorials recipes and problem fixes',
        'As always we start with the imports because we make the UI with tkinter',
        'Python is a high level programming language that emphasizes code readability',
        'Typing speed tests measure how fast and accurate you can type under time pressure',
        'Developers often practice by retyping random passages to improve their muscle memory',
        'Accuracy is just as important as speed when measuring typing performance',
        'Keyboard layouts such as QWERTY and Dvorak affect how fast people can type',
        'The best way to get faster is to practice regularly and track your progress over time',
        'Some professional typists can reach over one hundred words per minute consistently'
    ]

    # Clean punctuation + lowercase
    cleanedSentences = [re.sub(r"[.,]", "", s).lower() for s in possibleSentences]

    # Build a long paragraph
    random.shuffle(cleanedSentences)
    text = " ".join(cleanedSentences)

    labelLeft = Label(root, text="", fg="grey")
    labelLeft.place(relx=0.5, rely=0.5, anchor=E)

    labelRight = Label(root, text=text)
    labelRight.place(relx=0.5, rely=0.5, anchor=W)

    currentLetterLabel = Label(root, text=text[0], fg="pink")
    currentLetterLabel.place(relx=0.5, rely=0.7, anchor=N)

    timeleftLabel = Label(root, text=f"0 seconds", fg="grey")
    timeleftLabel.place(relx=0.5, rely=0.1, anchor=S)

    root.bind("<Key>", keyPress)

    root.after(60000, stopTest)  # stop after 60s
    root.after(1000, addSecond)

def stopTest():
    global writeAble, ResultLabel, ResultButton
    if not writeAble:  # already stopped
        return
    writeAble = False

    amountWords = len(labelLeft.cget("text").split(" "))
    elapsed = max(passedSeconds, 1)  # avoid div by zero
    wpm = math.floor(amountWords / elapsed * 60)

    # clean screen
    try:
        timeleftLabel.destroy()
        currentLetterLabel.destroy()
        labelRight.destroy()
        labelLeft.destroy()
    except:
        pass

    ResultLabel = Label(root, text=f"Your result is {wpm} WPM", fg="black")
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    ResultButton = Button(root, text="Try again", command=restart)
    ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)

def restart():
    ResultLabel.destroy()
    ResultButton.destroy()
    resetWritingLabels()

def addSecond():
    global passedSeconds
    passedSeconds += 1
    timeleftLabel.config(text=f"{passedSeconds} seconds")
    if writeAble:
        root.after(1000, addSecond)

def keyPress(event=None):
    global splitPoint, text, labelRight, labelLeft, currentLetterLabel
    if not writeAble:
        return
    try:
        if event.char.lower() == labelRight.cget("text")[0].lower():
            splitPoint += 1
            labelRight.configure(text=labelRight.cget("text")[1:])
            labelLeft.configure(text=labelLeft.cget("text") + event.char.lower())

            if labelRight.cget("text"):
                currentLetterLabel.config(text=labelRight.cget("text")[0])
            else:
                # if we reach the end, regenerate another paragraph
                resetWritingLabels()
    except tkinter.TclError:
        pass

resetWritingLabels()
root.mainloop()
