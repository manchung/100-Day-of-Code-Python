from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import os
import json

filename = f'{os.path.dirname(__file__)}/data.json'
default_email = 'manch@email.com'
logo_image_filename = f'{os.path.dirname(__file__)}/logo.png'

def search_password():
    try: 
        with open(file=filename, mode='r') as file:
            all_data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror('No Data File Found')
        return

    website = website_entry.get()
    print(f'website: {website}')
    try:
        email = all_data[website]['email']
        password = all_data[website]['password']
    except KeyError:
        messagebox.showinfo(message=f'No details for the website {website} exists.')
    else:
        email_entry.delete(0,END)
        email_entry.insert(0, email)
        password_entry.delete(0,END)
        password_entry.insert(0, password)
        pyperclip.copy(password)
        messagebox.showinfo(title=website, 
                            message=f'Email: {email}\nPassword: {password}\nPassword already copied to clipboard.')
    

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
    
    # is_ok = messagebox.askokcancel(title=website, 
    #                                message=f'You have entered the following\nWebsite:{website}\nEmail:{email}\nPassword:{password}\nOK to proceed?')
    
    new_data = {
        website : {
            'email': email,
            'password': password,
        }
    }

    try: 
        with open(file=filename, mode='r') as file:
            all_data = json.load(file)
            all_data.update(new_data)
    except FileNotFoundError:
        all_data = new_data
    
    with open(file=filename, mode='w') as file:
        json.dump(all_data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20, bg='white')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_img = PhotoImage(file=logo_image_filename)
canvas.create_image(100, 100, image=logo_img)
# canvas_text = canvas.create_text(100,130, text='00:00', fill='white', font=(FONT_NAME,35,'bold'))
canvas.grid(row=0, column=1)

website_label = Label(text='Website:', bg='white')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:', bg='white')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:', bg='white')
password_label.grid(row=3, column=0)

website_entry = Entry(width=21, bg='white', 
                      highlightthickness=0, highlightbackground='white', highlightcolor='white')
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = Button(text='Search', bg='white', width=11,
                       highlightthickness=0, highlightbackground='white', command=search_password)
search_button.grid(row=1, column=2)

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