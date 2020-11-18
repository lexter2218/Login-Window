from tkinter import *
from tkinter import messagebox
import sqlite3
from os.path import isfile
from hashlib import sha512
import sys

def center(master):
	master.update_idletasks()
	width = master.winfo_width()
	height = master.winfo_height()
	x = (master.winfo_screenwidth() // 2) - (width // 2)
	y = (master.winfo_screenheight() // 2) - (height // 2)
	master.geometry(f"{width}x{height}+{x}+{y}")
	print(width, height)

class Client():
	def __init__(self, master):
		self.master = master
		self.current_window = "login"
		self.on_window = "main"

		self.frm_win_login = Frame(self.master)

		self.frm_win_login.pack(padx=20, pady=10)

		self.lbl_win_name = Label(self.frm_win_login, text="Log In", font=("times", 13, "bold"))
		self.btn_change_win = Button(self.frm_win_login, text="Sign Up", font=("calibri", 9, "bold", "underline"), width=7, relief=FLAT, bd=1, command=lambda: self.window_change("setup"))
		self.lbl_username = Label(self.frm_win_login, text="Username:", font=("calibri", 10))
		self.ety_username = Entry(self.frm_win_login, width=25, relief=FLAT)
		self.lbl_password_id = Label(self.frm_win_login, text="Password:", font=("calibri", 10))
		self.ety_password_id = Entry(self.frm_win_login, width=25,  show="*", relief=FLAT)
		self.btn_acct_issue = Button(self.frm_win_login, text="Forgot Password?", font=("calibri", 8, "bold"), width=14, relief=FLAT, bd=1, command=lambda: self.window_change("issue"))
		self.btn_submit = Button(self.frm_win_login, text="Log In", font=("calibri", 10, "bold"), width=12, relief=FLAT, bd=1, command=self.process_submit)

		self.lbl_win_name.grid(row=0, column=0, columnspan=2, sticky=W, padx=(10,0), pady=(0,10))
		self.btn_change_win.grid(row=0, column=1, sticky=E, padx=(0,5), pady=(0,10))
		self.lbl_username.grid(row=1, column=0, sticky=W, padx=(0,20), pady=(0,2))
		self.ety_username.grid(row=1, column=1, sticky=E, pady=(0,2))
		self.lbl_password_id.grid(row=2, column=0, sticky=W, padx=(0,20), pady=(0,7))
		self.ety_password_id.grid(row=2, column=1, sticky=E, pady=(0,7))
		self.btn_acct_issue.grid(row=3, column=0, columnspan=2, sticky=W, padx=(0,10))
		self.btn_submit.grid(row=3, column=1, sticky=E, padx=(0,10))

		self.window_login()

		self.master.bind("<Button-1>", self.on_click)
		self.master.bind("<Key>", lambda a: self.on_click(a, self.process_submit))
		self.master.protocol("WM_DELETE_WINDOW", lambda: self.window_close(self.master))

		center(self.master)

	def on_click(self, event, func=None, value=None):
		if self.on_window == "toplevel":
			self.ety_username.delete(0, END)
			self.ety_password_id.delete(0, END)
		if event.keysym == "Return" and event.char == "\r" and func:
			if value:
				func(value)
			else:
				func()

	def window_change(self, choices):
		self.ety_username.delete(0, END)
		self.ety_password_id.delete(0, END)
		if self.current_window in ("login", "delete"):
			if choices == "setup":
				self.window_signup()
			else:
				self.window_forgot_password()
		else:
			if choices == "setup":
				self.window_login()
			else:
				self.window_delete_account()

	def window_login(self):
		self.master.configure(bg="#bbbbbb")
		self.frm_win_login.config(bg="#bbbbbb")
		self.lbl_win_name.config(text="Log In", bg="#bbbbbb")
		self.btn_change_win.config(text="Sign Up", bg="#bbbbbb", activebackground="#cccccc")
		self.lbl_username.config(bg="#bbbbbb")
		self.ety_username.config(bg="#dddddd")
		self.lbl_password_id.config(text="Password:", bg="#bbbbbb")
		self.ety_password_id.config(bg="#dddddd")
		self.btn_acct_issue.grid() #To show when the window transitioned from forget pass
		self.btn_acct_issue.config(text="Forgot Password?", bg="#bbbbbb", activebackground="#cccccc")
		self.btn_submit.config(text="Log In", bg="#aaaaaa", fg="#111111", activebackground="#cccccc", activeforeground="#333333")
		self.current_window = "login"

	def window_signup(self):
		self.master.configure(bg="#cccccc")
		self.frm_win_login.config(bg="#cccccc")
		self.lbl_win_name.config(text="Sign Up", bg="#cccccc")
		self.btn_change_win.config(text="Log In", bg="#cccccc", activebackground="#dddddd")
		self.lbl_username.config(bg="#cccccc")
		self.ety_username.config(bg="#eeeeee")
		self.lbl_password_id.config(bg="#cccccc")
		self.ety_password_id.config(bg="#eeeeee")
		self.btn_acct_issue.grid() #To show when the window transitioned from delete account
		self.btn_acct_issue.config(text="Delete Account", bg="#cccccc", activebackground="#dddddd")
		self.btn_submit.config(text="Sign Up", bg="#bbbbbb", fg="#222222", activebackground="#dddddd", activeforeground="#444444")
		self.current_window = "signup"

	def window_forgot_password(self):
		self.master.configure(bg="#aaaaaa")
		self.frm_win_login.config(bg="#aaaaaa")
		self.lbl_win_name.config(text="Forgot Password", bg="#aaaaaa")
		self.btn_change_win.config(text="Log In", bg="#aaaaaa", activebackground="#bbbbbb")
		self.lbl_username.config(bg="#aaaaaa")
		self.ety_username.config(bg="#cccccc")
		self.lbl_password_id.config(text="User ID:", bg="#aaaaaa")
		self.ety_password_id.config(bg="#cccccc")
		self.btn_acct_issue.grid_remove()
		self.btn_submit.config(text="Check", bg="#999999", fg="#000000", activebackground="#bbbbbb", activeforeground="#222222")
		self.current_window = "forgot"

	def window_delete_account(self):
		self.master.configure(bg="#dddddd")
		self.frm_win_login.config(bg="#dddddd")
		self.lbl_win_name.config(text="Delete Account", bg="#dddddd")
		self.btn_change_win.config(text="Sign Up", bg="#dddddd", activebackground="#eeeeee")
		self.lbl_username.config(bg="#dddddd")
		self.ety_username.config(bg="#ffffff")
		self.lbl_password_id.config(bg="#dddddd")
		self.ety_password_id.config(bg="#ffffff")
		self.btn_acct_issue.grid_remove()
		self.btn_submit.config(text="Delete", bg="#cccccc", fg="#333333", activebackground="#eeeeee", activeforeground="#555555")
		self.current_window = "delete"

	def window_confirmation(self, prompted_values):
		self.on_window = "toplevel"
		self.btn_submit.config(state=DISABLED, bg="#999999", fg="#000000")
		self.btn_change_win.config(state=DISABLED)
		self.btn_acct_issue.config(state=DISABLED)
		self.ety_username.config(state=DISABLED)
		self.ety_password_id.config(state=DISABLED)

		self.win_confirm = Toplevel()
		self.frm_confirm = Frame(self.win_confirm)
		self.frm_confirm.pack(padx=20, pady=10)

		self.lbl_title = Label(self.frm_confirm, font=("times", 11, "bold"))
		self.lbl_question_1 = Label(self.frm_confirm)
		self.ety_question_1 = Entry(self.frm_confirm, relief=FLAT, bg="#cccccc", selectbackground="#999999")
		self.lbl_question_2 = Label(self.frm_confirm)
		self.ety_question_2 = Entry(self.frm_confirm, show="*", relief=FLAT, bg="#cccccc", selectbackground="#999999")
		self.lbl_question_3 = Label(self.frm_confirm)
		self.ety_question_3 = Entry(self.frm_confirm, show="*", relief=FLAT, bg="#cccccc", selectbackground="#999999")
		self.btn_change = Button(self.frm_confirm, width=30, relief=FLAT, bd=1, bg="#999999", fg="#000000", activebackground="#bbbbbb", activeforeground="#222222", command=lambda: self.process_confirmation(prompted_values))

		self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(0,10))
		self.lbl_question_1.grid(row=1, column=0, sticky=W, padx=(0,20), pady=(0,5))
		self.ety_question_1.grid(row=1, column=1, sticky=E, pady=(0,5))
		self.lbl_question_2.grid(row=2, column=0, sticky=W, padx=(0,20), pady=(0,5))
		self.ety_question_2.grid(row=2, column=1, sticky=E, pady=(0,5))
		self.lbl_question_3.grid(row=3, column=0, sticky=W, padx=(0,20), pady=(0,10))
		self.ety_question_3.grid(row=3, column=1, sticky=E, pady=(0,10))
		self.btn_change.grid(row=4, column=0, columnspan=2)

		if self.current_window == "forgot":
			self.lbl_title.config(text="CHANGE PASSWORD")
			self.lbl_question_1.config(text="New Password:")
			self.ety_question_1.config(show="*")
			self.lbl_question_2.config(text="Confirm New Password:")
			self.lbl_question_3.config(text="User ID:")
			self.btn_change.config(text="Change Passsword")
		elif self.current_window == "delete":
			self.lbl_title.config(text="DELETE ACCOUNT")
			self.lbl_question_1.config(text="Username:")
			self.lbl_question_2.config(text="Password:")
			self.lbl_question_3.config(text="User ID:")
			self.btn_change.config(text="Delete Account")

		center(self.win_confirm)

		self.master.bind("<Return>", lambda a: self.on_click(a, self.process_confirmation, prompted_values))
		self.win_confirm.protocol("WM_DELETE_WINDOW", lambda: self.window_close(self.win_confirm))

	def process_confirmation(self, prompted_values):
		question_1 = self.ety_question_1.get()
		question_2 = self.ety_question_2.get()
		question_3 = self.ety_question_3.get()
		self.ety_question_1.delete(0, END)
		self.ety_question_2.delete(0, END)
		self.ety_question_3.delete(0, END)
		if self.current_window == "forgot":
			if question_1 == question_2 and prompted_values[0] == int(question_3):
				if len(question_1) > 7:
					hashed_password = sha512(question_1.encode()).hexdigest()
					if hashed_password != prompted_values[1]:
						self.process_database("update", hashed_password, prompted_values[0])
						messagebox.showinfo("Success", "Password Changed Successfully!")
					else:
						messagebox.showwarning("Failed", "Password is the same as previous one!")
					self.window_close(self.win_confirm, True)
				else:
					messagebox.showwarning("Failed", "Password should have at least 7 characters!")
			elif question_1 != question_2:
				messagebox.showwarning("Failed", "New Password and Confirm New Password are not the same!")
			elif prompted_values[0] != int(question_3):
				messagebox.showwarning("Failed", "User ID is incorrect!")
		elif self.current_window == "delete":
			if prompted_values[1] == question_1 and prompted_values[2] == question_2 and prompted_values[0] == int(question_3):
				hashed_username = sha512(prompted_values[1].encode()).hexdigest()
				hashed_password = sha512(prompted_values[2].encode()).hexdigest()
				self.process_database("delete", (prompted_values[0], hashed_username, hashed_password))
				messagebox.showinfo("Success", "Account Deleted Successfully!")
				self.window_close(self.win_confirm, True)
			elif prompted_values[1] != question_1:
				messagebox.showwarning("Failed", "Username is incorrect!")
			elif prompted_values[2] != question_2:
				messagebox.showwarning("Failed", "Password is incorrect!")
			elif prompted_values[0] != int(question_3):
				messagebox.showwarning("Failed", "User ID is incorrect!")

	def window_close(self, master, back=False):
		if back or (not back and not (master == self.master and self.on_window == "toplevel") and messagebox.askyesno("Close", "Do you really want to close?")):
			self.on_window = "main"
			self.btn_submit.config(state=NORMAL, bg="#aaaaaa", fg="#000000")
			self.btn_change_win.config(state=NORMAL)
			self.btn_acct_issue.config(state=NORMAL)
			self.ety_username.config(state=NORMAL)
			self.ety_password_id.config(state=NORMAL)
			master.destroy()

	def process_submit(self):
		prompted_username = self.ety_username.get()
		prompted_password = self.ety_password_id.get()
		self.ety_username.delete(0, END)
		self.ety_password_id.delete(0, END)

		hashed_username = sha512(prompted_username.encode()).hexdigest()
		hashed_password = sha512(prompted_password.encode()).hexdigest()
		if self.current_window == "login":
			if self.process_database("exist", (hashed_username, hashed_password), "UP"):
				messagebox.showinfo("Success", "Successfully Logged In!")
				sys.exit()
			elif self.process_database("exist", hashed_username, "U"):
				messagebox.showwarning("Failed", "Password is incorrect!")
			else:
				messagebox.showwarning("Failed", "Username and Password are incorrect!")

		elif self.current_window == "signup":
			if len(prompted_username) not in range(5,18):
				messagebox.showwarning("Failed", "Username should have 5 to 17 characters only!")
			elif len(prompted_password) <= 6:
				messagebox.showwarning("Failed", "Password should have at least 7 characters!")
			else:
				#Checks if username is still available (False) or already taken (True)
				if self.process_database("exist", hashed_username, "U"):
					messagebox.showwarning("Failed", "Username is already taken!")
				else:
					self.process_database("save", (hashed_username, hashed_password))
					registered_id = int(self.process_database("fetch", (hashed_username, hashed_password), "UP")[0][0])
					messagebox.showinfo("Success", f"ACCOUNT DETAILS:\n\nUSER ID:\t\t{registered_id}\nUSERNAME:\t{prompted_username}\nPASSWORD:\t{prompted_password}")
					self.window_change("setup")

		elif self.current_window == "forgot":
			try:
				prompted_id = int(prompted_password)
			except ValueError:
				messagebox.showwarning("Failed", "User ID should only contain integers!")
			else:
				#Checks if account exists
				if self.process_database("exist", (prompted_id, hashed_username), "IU"):
					fetch_account = self.process_database("fetch", (prompted_id, hashed_username), "IU")
					hashed_password = fetch_account[0][2]
					self.window_confirmation((prompted_id, hashed_password))
				elif self.process_database("exist", hashed_username, "U"):
					messagebox.showwarning("Failed", "User ID is incorrect!")
				else:
					messagebox.showwarning("Failed", "Account does not exist. Either Username or User Id is incorrect!")

		elif self.current_window == "delete":
			#Checks if account exists
			if self.process_database("exist", (hashed_username, hashed_password), "UP"):
				registered_id = self.process_database("fetch", (hashed_username, hashed_password), "UP")[0][0]
				self.window_confirmation((registered_id, prompted_username, prompted_password))
			elif self.process_database("exist", hashed_username, "U"):
				messagebox.showwarning("Failed", "Password is incorrect!")
			else:
				messagebox.showwarning("Failed", "Username and Password are incorrect!")

	def process_database(self, action, value=None, to_be_fetched=None):
		data = sqlite3.connect("data.db")
		accnt = data.cursor()
		result = None

		try: 
			accnt.execute("CREATE TABLE accounts(username text, password text)")
		except sqlite3.OperationalError:
			pass

		if action in ("exist", "fetch"):
			if to_be_fetched == "U":
				accnt.execute("SELECT rowid, * FROM accounts WHERE username = '{}'".format(value))
			elif to_be_fetched == "P":
				accnt.execute("SELECT rowid, * FROM accounts WHERE password = '{}'".format(value))
			elif to_be_fetched == "I":
				accnt.execute("SELECT rowid, * FROM accounts WHERE rowid = {}".format(value))
			elif to_be_fetched == "UP":
				accnt.execute("SELECT rowid, * FROM accounts WHERE username = '{}' AND password = '{}'".format(value[0], value[1]))
			elif to_be_fetched == "IU":
				accnt.execute("SELECT rowid, * FROM accounts WHERE rowid = {} AND username = '{}'".format(value[0], value[1]))
			elif to_be_fetched == "IP":
				accnt.execute("SELECT rowid, * FROM accounts WHERE rowid = {} AND password = '{}'".format(value[0], value[1]))
			elif to_be_fetched == "A":
				accnt.execute("SELECT rowid, * FROM accounts WHERE rowid = {} AND username = '{}' AND password = '{}'".format(value[0], value[1], value[2]))
			if action == "exist":
				result = len(accnt.fetchall()) > 0
			elif action == "fetch":
				result = accnt.fetchall()
		elif action == "save":
			accnt.execute("INSERT INTO accounts VALUES {}".format(value))
		elif action == "update":
			accnt.execute("UPDATE accounts SET password = '{}' WHERE rowid = {}".format(value, to_be_fetched))
		elif action == "delete":
			accnt.execute("DELETE FROM accounts WHERE rowid = {} AND username = '{}' AND password = '{}'".format(value[0], value[1], value[2]))

		data.commit()
		data.close()

		return result


if __name__ == "__main__":
	root = Tk()
	root.title("Login Window V.2")

	client = Client(root)
	client.window_login()

	root = mainloop()