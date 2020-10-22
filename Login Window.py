from tkinter import *
from tkinter import messagebox
import os

def change_window_to(window1, window2, window3):
	global entry_username
	global entry_password_id
	pseudo_grid = Label(root, text="")
	pseudo_grid.grid(column=0, row=0)
	for pseudo_grid in root.grid_slaves():
		pseudo_grid.grid_forget()

	pass_or_id = "Password:"
	window3 = "Forget Password?"
	forget_delete = "Forget Password?"
	if window1 == "Log In":
		button = "Join"
		window2 = "Sign Up"
		btn_ipadx = (30)
	elif window1 == "Sign Up":
		button = "Create"
		window2 = "Log In"
		btn_ipadx = (24)
		forget_delete = "Delete an account?"
	elif window1 == "Forget Password?":
		button = "Confirm"
		pass_or_id = "ID:"
		btn_ipadx = (18)
	elif window1 == "Delete an account?":
		button = "Confirm"
		pass_or_id = "ID:"
		btn_ipadx = (18)

	if window1 == "Forget Password?":
		lbl_phase = Label(root, text="FORGET PASS", font=('Verdana', 9,'bold'))
	elif window1 == "Delete an account?":
		lbl_phase = Label(root, text=f"DELETE ACCOUNT", font=('Verdana', 9,'bold'))
	else:
		lbl_phase = Label(root, text=window1.upper(), font=('Verdana', 9,'bold'))
	if window1 == "Forget Password?":
		btn_signup = Button(root, text="Log In", relief=FLAT, font=('Verdana', 7,'bold','underline'), command=lambda: change_window_to("Log In", "Sign Up", "Forget Password?"))
	else:
		btn_signup = Button(root, text=window2, relief=FLAT, font=('Verdana', 7,'bold','underline'), command=lambda: change_window_to(window2, window1, window3))
	lbl_username = Label(root, text="Username:", font=('Verdana', 8))
	lbl_password_id = Label(root, text=pass_or_id, font=('Verdana', 8))
	entry_username = Entry(root, relief=FLAT)
	entry_password_id = Entry(root, relief=FLAT, show="*")
	btn_forget_password = Button(root, text=forget_delete, relief=FLAT, font=('Verdana', 7,'normal','underline'), command=lambda: change_window_to(forget_delete, window1, window2))	
	btn_submit = Button(root, text=button, command=lambda: do_submit(entry_username.get(), entry_password_id.get(), window1))

	lbl_phase.grid(row=0, column=0, padx=(5, 0))
	btn_signup.grid(row=0, column=1, padx=(0, 5), sticky=E)
	lbl_username.grid(row=1, column=0, padx=(5, 40), sticky=W)
	entry_username.grid(row=1, column=1, pady=(10, 5), padx=(0, 10))
	lbl_password_id.grid(row=2, column=0, padx=(5, 40), sticky=W)
	entry_password_id.grid(row=2, column=1, padx=(0, 10))
	if window1 == "Log In" or window1 == "Sign Up":
		btn_forget_password.grid(row=3, column=0, padx=(5, 0), pady=(10, 5), sticky=W)
	btn_submit.grid(row=3, column=1, pady=(10, 5), padx=(0, 10), ipadx=btn_ipadx, sticky=E)


def do_submit(username, password_id, window):
	min_max_chars = (5,17)
	chr_shift = 5
	entry_username.delete(0, END)
	entry_password_id.delete(0, END)

	#Checks if entry is blank
	if len(username) < 5 or len(username) > 17 or len(password_id) == 0:
		if len(username) == 0 or len(password_id) == 0:
			if len(username) == 0 and len(password_id) != 0:
				blank = "Username"

			elif len(username) != 0 and len(password_id) == 0:
				blank = "Password"

			elif len(username) == 0 and len(password_id) == 0:
				blank = "Username and Password"
			response = messagebox.showwarning("WARNING!", "Don't leave your " + blank + " blank!")
		elif len(username) < 5 or len(username) > 17:
			response = messagebox.showwarning("WARNING!", "Username should only have 5 to 17 number of characters!")
		return

	password_id = str(password_id)
	pseudo_account = [username, password_id]
	account = ["", ""]

	#char checker and shifter
	for value in pseudo_account:
		for char in value:
			if ord(char) in range(48, 58) or ord(char) in range(65, 91) or ord(char) in range(97, 123):
				if len(account[0]) != len(username):
					account[0] += str(char)
				elif len(account[1]) != len(password_id):
					pseudo_char = char
					if window == "Log In" or window == "Sign Up":
						if ord(char) in range(65,91):
							upper_lower = "upper"
						elif ord(char) in range(97,123):
							upper_lower = "lower"
						elif ord(char) in range(48,58):
							upper_lower = "num"
						pseudo_char = chr(ord(pseudo_char) + chr_shift)
						if (ord(pseudo_char) > 90 and upper_lower == "upper") or (ord(pseudo_char) > 122 and upper_lower == "lower"):
							pseudo_char = chr(ord(pseudo_char.upper()) - 26)
						elif ord(pseudo_char) > 57 and upper_lower == "num":
							pseudo_char = chr(ord(pseudo_char.upper()) - 5)
					elif window == "Forget Password?" or window == "Delete an account?":
						if ord(char) not in range(48, 58):
							response = messagebox.showwarning("WARNING!", "ID is an Integer!")
							return
					account[1] += str(pseudo_char)
			else:
				account = ["", ""]
				response = messagebox.showwarning("FAILED!","Only use letters and numbers!")
				return

	#Account file creator or opener
	account_exist = [-1, -1]
	if not os.path.isdir("data"):
		os.system('mkdir data')
	if not os.path.isfile("accounts.txt"):
		os.system('type nul > accounts.txt')
	account_files = open("accounts.txt", "r")
	accounts_list = account_files.readlines()
	account_files.close()
	account_id = len(accounts_list)

	#Account Existence Checker
	for account_pair in accounts_list:
		if account_pair.find("-" + account[0] + "-") != -1:
			account_index = accounts_list.index(account_pair)
			account_exist[0] = 0
			account_exist[1] = account_pair.find("-" + account[1] + "-")
			account_pass = account_pair.replace("-" + account[1] + "-" + account[0] + "-","")
			account_pass = account_pass.replace("-","")
			break
		else:
			if window != "Sign Up":
				response = messagebox.showwarning("WARNING!","Account doesn't exist!")
				return

	#Account Saving and Output
	if window == "Sign Up":
		if account_exist[0] != -1 and account_exist[1] != -1:
			response = messagebox.showwarning("FAILED!", account[0] + ", This account already exist!")
		elif account_exist[0] == -1:
			account_files = open("accounts.txt", "a")
			account_files.write("-" + str(account_id + 1) + "-" + account[0] + "-" + account[1] + "-\n")
			account_files.close()
			response = messagebox.showinfo("SUCCESS!", "Account Succefully made!\n\nUsername: " + account[0] + "\nPassword: " + password_id + "\nAccount Id: " + str(account_id + 1))
			return

	if accounts_list == []:
		response = messagebox.showwarning("WARNING!", "There is no account saved in your device!")
		return

	#Logging In	
	if window == "Log In":
		if account_exist[0] != -1 and account_exist[1] != -1:
			response = messagebox.showinfo("SUCCESS!", "Hi " + account[0] + "! You have been successfully logged in!")
			screen.destroy()
		elif account_exist[1] == -1:
			response = messagebox.showwarning("WARNING!", "Your Password is wrong!")

	#Password reader and confirmation to delete an account
	elif window == "Forget Password?" or window == "Delete an account?":
		if account_exist[1] == -1:
			response = messagebox.showwarning("WARNING!", "Wrong ID!")
			return

		#Password Reader	
		pseudo_account_pass = account_pass
		account_pass = ""
		chr_shift = -chr_shift
		for char in pseudo_account_pass:
			pseudo_char = char
			if ord(char) in range(65,91):
				upper_lower = "upper"
			elif ord(char) in range(97,123):
				upper_lower = "lower"
			elif ord(char) in range(48,58):
				upper_lower = "num"
			if pseudo_account_pass.index(char) != len(pseudo_account_pass) - 1:
				pseudo_char = chr(ord(pseudo_char) + chr_shift)
				if (ord(pseudo_char) < 65 and upper_lower == "upper") or (ord(pseudo_char) < 97 and upper_lower == "lower"):
					pseudo_char = chr(ord(pseudo_char.upper()) + 26)
				elif ord(pseudo_char) < 48 and upper_lower == "num":
					pseudo_char = chr(ord(pseudo_char.upper()) + 5)
				account_pass += str(pseudo_char)
			else:
				break

		#Account Delete Confirmation
		if window == "Delete an account?":
			if account_exist[0] != -1 and account_exist[1] != -1:
				confirm_window = Toplevel()
				confirm_window.title("CONFIRMATION")

				lbl_confirm = Label(confirm_window, text="Confirm Password to continue.")
				entry_confirm = Entry(confirm_window, justify=CENTER, relief=FLAT, show="*")
				btn_confirm = Button(confirm_window, text=f"DELETE", command=lambda: [do_delete(account[1], entry_confirm.get(), account_pass), confirm_window.destroy()])
				btn_cancel = Button(confirm_window, text="CANCEL", command=lambda: confirm_window.destroy())

				lbl_confirm.grid(row=0, column=0, columnspan=2)
				entry_confirm.grid(row=1, column=0, columnspan=2, pady=10)
				btn_confirm.grid(row=2, column=0, pady=(0, 5), padx=(10, 5), ipadx=20, sticky=E)
				btn_cancel.grid(row=2, column=1, pady=(0, 5), padx=(5, 10), ipadx=20, sticky=E)
			else:
				response = messagebox.showwarning("WARNING!", "Your ID is wrong!")
		else:
			response = messagebox.showinfo("SUCCESS!", "Account Succefully found!\n\nUsername: " + account[0] + "\nPassword: " + str(account_pass) + "\nAccount Id: " + account[1])


def do_delete(id_number, confirmation, password):

	id_number = int(id_number)
	if confirmation == password:
		account_files = open("accounts.txt", "r")
		accounts_list = account_files.readlines()
		account_files.close()

		#Account Remover
		if accounts_list[int(id_number) - 1].find("-" + str(id_number) + "-") != -1:
			accounts_list.remove(accounts_list[int(id_number) - 1])

		#Blanks data saved if deleted the only data
		if accounts_list == []:
			account_files = open("accounts.txt", "w")
			account_files.write("")
		else:
			for account in accounts_list:
				#1st Account overwrite to txt
				if accounts_list.index(account) == 0:
					account_files = open("accounts.txt", "w")
					account_files.write(accounts_list[0])
					account_files.close()
				#Accounts append to txt
				else:
					account_files = open("accounts.txt", "a+")
					account_files.write(accounts_list[accounts_list.index(account)])
		account_files.close()
		response = messagebox.showinfo("SUCCESS!", "Account Successfully Deleted!")
	else:
		response = messagebox.showwarning("WARNING!", "You entered a wrong password!")


screen = Tk()
screen.title("Account Menu")
screen.resizable(0, 0)
screen.geometry("300x150")
screen.resizable(0, 0)

root = LabelFrame(screen, relief=FLAT)
root.pack()
change_window_to("Log In", "Sign Up", "Forget Password?")

screen = mainloop()