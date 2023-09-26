import requests
import tkinter
from tkinter import messagebox


class Application:
	windows_bg = '#333'
	windows_fg = '#CCC'

	def __init__(self):
		self.window = tkinter.Tk()
		self.window.title('Login')
		self.window.geometry('340x440')
		self.window.configure(bg=self.windows_bg)

		frame = tkinter.Frame(self.window, bg=self.windows_bg)

		# Widgets
		login_label = tkinter.Label(frame, text='Sign in', bg=self.windows_bg, fg='#F39', font=('Helvetica', 22))

		username_label = tkinter.Label(frame, text='Username', bg=self.windows_bg, fg=self.windows_fg, font=('Helvetica', 16))
		username_entry = tkinter.Entry(frame)
		
		password_label = tkinter.Label(frame, text='Password', bg=self.windows_bg, fg=self.windows_fg, font=('Helvetica', 16))
		password_entry = tkinter.Entry(frame, show='*')
		
		login_button = tkinter.Button(frame, text='Login', bg=self.windows_bg, fg='#F39', font=('Helvetica', 16), command=self.login)

		register_label = tkinter.Label(frame, text='New to the app?', bg=self.windows_bg, fg=self.windows_fg, font=('Helvetica', 12))
		register_button = tkinter.Button(frame, text='Register here', bg=self.windows_bg, fg='#F39', font=('Helvetica', 12), border=0, command=self.new_user)


		# Widget placement
		login_label.grid(row=0, column=0, columnspan=2, pady=30)

		username_label.grid(row=1, column=0, pady=20)
		username_entry.grid(row=1, column=1)
		
		password_label.grid(row=2, column=0, pady=20)
		password_entry.grid(row=2, column=1)
		
		login_button.grid(row=3, column=0, columnspan=2, pady=30)
		
		register_label.grid(row=4, column=0)
		register_button.grid(row=4, column=1)
		
		frame.pack()

		self.window.mainloop()

	
	def login(self):
		if not True:
			messagebox.showinfo(title='Success', message='Successfully Logged In')
		
		else:
			messagebox.showerror(title='Failed', message='Invalid login details')


	def new_user(self):
		screen = tkinter.Toplevel(self.window, bg=self.windows_bg)
		screen.geometry('340x340+200+200')
		screen.title('Register')

		frame = tkinter.Frame(screen, bg=self.windows_bg)

		# Widgets
		register_label = tkinter.Label(frame, text='Register', bg=self.windows_bg, fg='#F39', font=('Helvetica', 22))

		username_label = tkinter.Label(frame, text='Username', bg=self.windows_bg, fg=self.windows_fg, font=('Helvetica', 16))
		username_entry = tkinter.Entry(frame)
		
		password_label = tkinter.Label(frame, text='Password', bg=self.windows_bg, fg=self.windows_fg, font=('Helvetica', 16))
		password_entry = tkinter.Entry(frame, show='*')
		
		register_button = tkinter.Button(frame, text='Sign Up', bg=self.windows_bg, fg='#F39', font=('Helvetica', 16), command=self.register)

		# Widget placement
		register_label.grid(row=0, column=0, columnspan=2, pady=30)

		username_label.grid(row=1, column=0, pady=20)
		username_entry.grid(row=1, column=1)
		
		password_label.grid(row=2, column=0, pady=20)
		password_entry.grid(row=2, column=1)
		
		register_button.grid(row=3, column=0, columnspan=2, pady=30)
		
		frame.pack()

		screen.mainloop()


	def register(self):
		pass


if __name__ == '__main__':
	app = Application()
	app.login()