import sys
import os
from pynput.keyboard import Key, Listener

clear = lambda: os.system('clear')

class Buffer():
    def __init__(self, inStart="", file=False):
        self.content = ""
        self.file = file
        if file:
            self.con = inStart
            with open(inStart) as textfile:
                for content in textfile:
                    self.content += content

        else:
            self.con =""
            self.content = inStart + " "
        self.p = 0

        self.state = "waiting"
        self.contentHistory = [self.content]
        self.stateChecker()
        print("press space")
        self.doListener(self.on_press)

    def saveFile(self):
        if self.file:
            with open(self.con, "w") as f:
                f.write(self.content)

    def insert(self, c,p):
        if len(self.content) == 0:
            print("empty")
            self.content = c
        else:
            self.content = self.content[0:-p] + c + self.content[-p:len(self.content)]
#----------

    def on_press(self,key):
        #print('{0} pressed'.format(
            #key))
        self.check_key(key)

    def on_release(self,key):
        #print('{0} release'.format(
           # key))
        if key == Key.enter:
            # Stop listener
            self.state = "waiting"
            self.saveFile()
            return False


    def on_delete(self, key):
        if key == Key.backspace:
            clear()
            print('\x1b[6;30;41m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave with enter"+ '\x1b[0m'+ "\n")
            if len(self.content) == 0:
                print('\x1b[4;31;40m' + "Content Empty" + '\x1b[0m')
            else:
                splitted = self.content.split(" ")[0:-1]
                self.content = ' '.join(splitted)
                print(self.content)

    def on_insert(self, key):
        clear()
        print('\x1b[6;30;42m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave/Save with enter / double ctrl to move" + '\x1b[0m' +
              '\x1b[5;30;41m' + "unsaved" + '\x1b[0m' + "\n")
        if key == Key.backspace:
            if self.p != len(self.content):
                self.content = self.content[0:-self.p-1] + self.content[-self.p:len(self.content)]
            print(self.content)

        elif key == Key.ctrl:
            self.state = "move"
            return False

        elif key != Key.enter:
            i =str(key)[1]
            if key in [Key.space]:
                i = " "
            if key in [Key.caps_lock,Key.shift]:
                i = ""
            if key in [Key.right, Key.left,Key.up,Key.down,Key.delete]:
                pass
            self.insert(i,self.p)
            print(self.content)

        else:
            self.state = "waiting"

    def on_move(self, key):
        clear()
        print('\x1b[6;30;42m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave with enter, use <- -> to move the cursor" + '\x1b[0m' + "\n")


        if key == Key.left:
            self.p += 1
        if key == Key.right:
            self.p -= 1

        if self.p == 1:
            print(self.content[0:-self.p] + '\x1b[3;30;41m' + self.content[-1] + '\x1b[0m')

        elif self.p > len(self.content):
            self.p = len(self.content)
            print(self.content[0:-self.p] + '\x1b[3;30;41m' + self.content[-self.p] + '\x1b[0m' + self.content[
                                                                                                  -self.p + 1:len(
                                                                                                      self.content)])
        elif self.p < 0:
            self.p = len(self.content)
            print(self.content[0:-self.p] + '\x1b[3;30;41m' + self.content[-self.p] + '\x1b[0m' + self.content[
                                                                                                  -self.p + 1:len(
                                                                                                      self.content)])
        else:
            print(self.content[0:-self.p] + '\x1b[3;30;41m' + self.content[-self.p] + '\x1b[0m' + self.content[
                                                                                                  -self.p + 1:len(
                                                                                                      self.content)])
        if key == Key.enter: self.state = "insert"


    def check_key(self,key):
        if key == Key.ctrl:
            clear()

            self.state = "move"
            print('\x1b[6;30;42m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave with enter, use <- -> to move the cursor"+ '\x1b[0m'+ "\n")
            self.stateChecker()
        if key == Key.delete:
            clear()
            self.state = "delete"
            print('\x1b[6;30;41m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave with enter" + '\x1b[0m'+ "\n")
            print(self.content)
            self.stateChecker()
        if key == Key.left:
            clear()
            if len(self.contentHistory) != 0: self.content = self.contentHistory.pop()
            else: print('\x1b[4;31;47m' + "nothing to undo!" + '\x1b[0m')
            self.stateChecker()
        if key == Key.esc:
            self.state = "exit"
            self.stateChecker()

        else:
            clear()
            #self.state ="waiting"
            self.stateChecker()

    def stateChecker(self):
        if self.state == "insert":
            clear()
            print('\x1b[6;30;42m' + self.state + '\x1b[0m' + '\x1b[1;37;41m' + "Leave/Save with enter / double ctrl to move" + '\x1b[0m'+
                  '\x1b[5;30;41m' + "unsaved" + '\x1b[0m'+ "\n")
            print(self.content)
            self.doListener(self.on_insert)
            self.p = 0

        if self.state == "move":
            if len(self.content) == 0:
                self.state = "insert"
            else:
                self.contentHistory.append(self.content)
                print(self.content)
                self.doListener(self.on_move)
                self.state = "insert"

        if self.state == "delete":
            self.contentHistory.append(self.content)
            self.doListener(self.on_delete)
            self.state = "waiting"

        if self.state == "waiting":
            print('\x1b[5;30;47m'+"select mode double esc to exit" + '\x1b[0m')
            print('\x1b[6;30;41m' + self.state +" "+ '\x1b[0m' +'\x1b[0m'+ '\x1b[3;30;42m' +
                  ' press: <- to undo last action' + '\x1b[0m')
            print('\x1b[4;30;47m'+ "Working on: " + os.path.basename(self.con) + '\x1b[0m' + '\x1b[5;37;42m'+ "Saved" + '\x1b[0m')
            print(self.content)
            print("\n")
            print('\x1b[0;30;44m' + "mode control: CTRL - move -> ENTER -> insert | DEL - delte mode, delete whole words with BACKSPACE " + '\x1b[0m')
            self.doListener(self.on_press)

        if self.state == "exit": sys.exit()

    def doListener(self,on_press):
        with Listener(
                on_press=on_press,
                on_release=self.on_release) as listener:
            listener.join()
            clear()


