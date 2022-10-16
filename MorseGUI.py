from curses.ascii import isalpha
from tkinter import *
from tkinter import messagebox
import RPi.GPIO as GPIO
import time 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

morse_led = 10

GPIO.setup(morse_led, GPIO.OUT)

def rgb(rgb):
    """Convert RGB colour coding to hexadecimal string using this function. 

    Args:
        rgb (int): rgb colour tuple

    Returns:
        string: hexadecimal string representing a colour
    """
    return "#%02x%02x%02x" % rgb

root = Tk()
root.title("Morse GUI")
root.minsize(width=200, height=150)
root.geometry("300x100")
root.config(bg= rgb((76, 83, 89)))

# A dictionary to store all the alphabets and their associated morse code
alphamorse = {"a":".-", "b":"-...", "c":"-.-.", "d":"-..", "e":".",
"f":"..-.","g":"--.","h":"....", "i":"..", "j":".---", "k":"-.-", 
"l":".-..", "m":"--", "n":"-.", "o":"---", "p":".--.", "q":"--.-",
"r":".-.", "s":"...","t":"-", "u":"..-", "v":"...-", "w":".--", 
"x":"-..-", "y":"-.--", "z":"--.."}

def limitChar(*args):   # Used args because unsure about number of argumnets in function 
    """Function to limit number of characters in the entry box
    """
    value = name.get()  # Getting all the characters from the entry box
    if len(value) > 12:
        name.set(value[0:12])   #If character length increases beyond 12 then it will set the first 12 character in the entry box

name = StringVar()
name.trace('w', limitChar)

def gui():
    """Function to run main gui components
    """
    global myText, submitText, exitButton

    lable = Label(root, text="Enter Your Name", bg= rgb((76, 83, 89)), fg="white")
    lable.place(relx= 0.19, rely=0.1, relwidth=0.60, relheight=0.2)

    myText = Entry(root, font=('Courier', 16, "bold"), textvariable=name)
    myText.place(relx= 0.19, rely=0.3, relwidth=0.60, relheight=0.2)


    submitText = Button(root, text= "Submit", bg=rgb((208, 217, 216)),command= getText)
    submitText.place(relx= 0.28, rely=0.6, relwidth=0.20, relheight=0.2)

    exitButton = Button(root, text="Exit", command= exit)
    exitButton.place(relx= 0.49, rely= 0.6, relwidth= 0.20, relheight= 0.2)

def getText():
    """Function gets and validates user input from the Entry box and
    then blink_name() function to blink morse code of the name.
    """
    if userInputCheck(myText.get()):
        name = myText.get()
        # Once the submit button is pressed disabling the Text box, submit button and entry button
        myText.config(state= 'disabled')
        submitText.config(state= 'disabled')
        exitButton.config(state= 'disabled')
        blink_name(name)
        # After the blink function is class renabling the buttons
        myText.config(state= 'normal')
        submitText.config(state= 'normal')
        exitButton.config(state= 'normal')
        myText.delete(0, END)
    

def clearText():
    """Clears the text of the entry box
    """
    myText.delete(1.0, END)

def userInputCheck(userInput):
    """The function will the check the user input for string containing only alphabets 
    otherwise it will show a error message box asking user to enter alphabets

    Args:
        userInput (string): Value from the entry box to validate for alphabets

    Returns:
        bool: True if the string is of alphabets and False if the string contains numerics or string is numerics
    """
    if userInput.isalpha():
        return True
    else:
        messagebox.showerror("Error", "Please enter alphabets only", icon="error")
        myText.delete(0, END)
        return False

def generate_morse(name):
    """This function will iterate throught each charater of the name string 
    and will find the same key character from the alphamorse dictionary and will 
    add the associated value of the key to morse_code string. After the iteration 
    is complete it will return the morse_code string. 

    Args:
        name (string): Name which we want to generate more code 

    Returns:
        string: Morse of the name which is passed in this function
    """
    morse_code = ""
    for char in name:
        for x, y in alphamorse.items(): 
            if char == x:
                morse_code += y
        
        morse_code += " "
    
    return morse_code

def blink_name(name):
    """The function will first remove any spaces from front and end of the name string using the strip() function
    and then it will convert the entire name string to lower case. Then it will generate the morse code using 
    the generate_morse() funcition. Once the morse code is generated it will iterate through each character of string of
    morse code and will blink the led accrodingly.

    Args:
        name (string): The name which is entered in the entery box for 
        blinking of the morse code
    """
    name = name.strip()
    name = name.lower()
    print(name)
    morse_code = generate_morse(name)   # Calling the generate_morse function
    print(morse_code)

    for char in morse_code:
        if char == "-": # If the char is - call blink_dash() function
            blink_dash()
        elif char == ".":  #If the char is . call blink_dot() function 
            blink_dot()
        elif char == " ":   #If the char is " " add a delay of three seconds
            time.sleep(3)

def blink_dot():
    """Function is turning on led for one seconds which signifies a dot in the morse code
    """
    GPIO.output(morse_led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(morse_led, GPIO.LOW)
    time.sleep(1)

def blink_dash():
    """Function is turning on led for three seconds which signifies a dash in the morse code
    """
    GPIO.output(morse_led, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(morse_led, GPIO.LOW)
    time.sleep(1)

def exit():
    """Function will set pin 10 to low and then set all the pins to their default 
    state which is input and then it will destroy the root instance and all the 
    widgets in it. 
    """
    GPIO.output(10, GPIO.LOW)
    GPIO.cleanup()
    root.destroy()

gui()

root.mainloop()
