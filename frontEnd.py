"""
building the front end interface using tkinter
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox

from client import Client


class ClientApp:
    def __init__(self, name):
        f"""
        Initializing the interactive graphical interface for {name}
        :param name: str ( Name of the new client )
        """
        self.window = tk.Tk()
        self.window.title('Chat Box')
        self.window.configure(bg='#aff0e7')
        self.window.geometry('480x650')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.resizable(0, 0)  # to prevent maximizing the chat box
        self.chat_log = scrolledtext.ScrolledText(font=("Times New Roman", 15), bg='white', fg='#0d3542')
        self.chat_log.place(x=10, y=10, width=460, height=550)
        self.chat_log.tag_configure('right_align', justify=tk.RIGHT)  # for texts sent by 'you'
        self.chat_log.tag_configure('left_align', justify=tk.LEFT)  # for texts received from other clients
        self.chat_log.config(state='disabled')  # to make chat_box read only
        self.client = Client(name, self.chat_log)
        self.send_btn = tk.Button(command=self.send_msg, highlightthickness=0, bd=0)
        photo = tk.PhotoImage(file="Icons\\send_btn.png")
        self.send_btn.config(image=photo, bg='#aff0e7')
        self.send_btn.place(x=425, y=580, width=50, height=50)
        self.user_text = tk.Entry(font=("Times New Roman", 15), bg='#0d626b', fg='white')
        self.user_text.place(x=10, y=580, width=400, height=50)
        self.window.mainloop()

    def on_closing(self):
        self.client.disconnect()
        self.window.destroy()

    def send_msg(self):
        """
        Sending the user input (text message) iff non empty to the server
        which shall be broadcast to other connected clients
        :return: None
        """
        message = self.user_text.get()
        if message:
            # send the message only if not empty
            to_print_message = 'You: ' + message + "    " + '\n'
            self.client.num_of_msg += 1
            placing = float(self.client.num_of_msg)
            self.chat_log.config(state='normal')
            self.chat_log.insert(placing, to_print_message, ('right_align',))
            self.chat_log.config(state='disabled')  # enable just for the split second
            # and disable again to maintain read only property
            self.client.send_messages(message)
            self.user_text.delete(0, tk.END)  # clear the 'send' box
        else:
            messagebox.showwarning("Null Message", "Cannot send empty message!")


if __name__ == '__main__':
    client = ClientApp('Pritam')
