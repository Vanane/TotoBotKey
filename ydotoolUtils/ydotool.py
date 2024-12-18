import os, time

'''
Ydotool native functions
'''
def click(x, y, btn=None):
    os.system(f"ydotool click {x} {y}")

def mousemove(x, y):
    os.system(f"ydotool mousemove {x} {y}")

def type(text):
    os.system(f"ydotool type {text}")

def key(keys):
    if type(keys) is list:
        keys = ' '.join(keys)
    os.system(f"ydotool key {keys}")


'''
Additionnal functions
'''
def wait(ms):
    time.sleep(int(ms) / 1000)

