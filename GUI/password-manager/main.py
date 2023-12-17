from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip

filename = 'data.txt'
default_email = 'manch@email.com'

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def gen_password():
    num_letters = random.randint(8, 12) 
    num_symbols = random.randint(2, 4)
    num_numbers = random.randint(2, 4) 

    letters = string.ascii_letters
    numbers = string.digits
    symbols = '!@#$%^&*()'

    password_list = [random.choice(letters) for _ in range(num_letters)]
    password_list += [random.choice(numbers) for _ in range(num_numbers)]
    password_list += [random.choice(symbols) for _ in range(num_symbols)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    # print(f"Here is your password {''.join(password)}")
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)      

# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_password():
    website = website_entry.get()
    if len(website) == 0: 
        messagebox.showerror(title='Error', message='The "Website" field cannot be empty')
        return
    
    email = email_entry.get()
    if len(email) == 0:
        messagebox.showerror(title='Error', message='The "Email" field cannot be empty')
        return
    
    password = password_entry.get()
    if len(password) == 0:
        messagebox.showerror(title='Error', message='The "Password" field cannot be empty')
        return
    
    is_ok = messagebox.askokcancel(title=website, 
                                   message=f'You have entered the following\nWebsite:{website}\nEmail:{email}\nPassword:{password}\nOK to proceed?')
    
    if is_ok:
        with open(file=filename, mode='a') as file:
            file.write(f'{website} | {email} | {password}\n')
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20, bg='white')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
# canvas_text = canvas.create_text(100,130, text='00:00', fill='white', font=(FONT_NAME,35,'bold'))
canvas.grid(row=0, column=1)

website_label = Label(text='Website:', bg='white')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:', bg='white')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:', bg='white')
password_label.grid(row=3, column=0)

website_entry = Entry(width=36, bg='white', 
                      highlightthickness=0, highlightbackground='white', highlightcolor='white')
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=36, bg='white', 
                      highlightthickness=0, highlightbackground='white', highlightcolor='white')
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, default_email)

password_entry = Entry(width=21, bg='white', 
                        highlightthickness=0, highlightbackground='white', highlightcolor='white')
password_entry.grid(row=3, column=1)

generate_button = Button(text='Generate Password', bg='white', width=11,
                         highlightthickness=0, highlightbackground='white', command=gen_password)
generate_button.grid(row=3, column=2)

add_button = Button(text='Add', bg='white', width=34,
                        highlightthickness=0, highlightbackground='white', command=add_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()