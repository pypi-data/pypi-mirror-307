import customtkinter
import os
from PIL import Image

def Message(Type, Name, Message, Style = "system"):
    mess = customtkinter.CTk()
    mess.title(Type)
    mess.resizable(False, True)
    mess.geometry("300x100")
    customtkinter.set_appearance_mode(Styleun)

    if Type == "error":
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "Delete.ico")
        mess.iconbitmap(icon_path)
        Title = customtkinter.CTkLabel(mess, font= ("Calibri", 20, "bold"), text = Name, wraplength = 300)
        Desc= customtkinter.CTkLabel(mess, font= ("Calibri", 15, "bold"), text = Message, wraplength = 280)
        Title.grid(column = 0, row =0, pady = 5, padx = 10,  sticky="w")
        Desc.grid(column = 0, row =1, pady = 5, padx = 10, sticky="w")
        ok = customtkinter.CTkButton(mess, font= ("Calibri", 15, "bold"), text = "Ok", command = mess.destroy).grid(column = 0, row =2, pady = 5, padx = 10)
    if Type == "info":
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "Info.ico")
        mess.iconbitmap(icon_path)
        Title = customtkinter.CTkLabel(mess, font= ("Calibri", 20, "bold"), text = Name, wraplength = 300)
        Desc= customtkinter.CTkLabel(mess, font= ("Calibri", 15, "bold"), text = Message, wraplength = 280)
        Title.grid(column = 0, row =0, pady = 5, padx = 10,  sticky="w")
        Desc.grid(column = 0, row =1, pady = 5, padx = 10, sticky="w")
        ok = customtkinter.CTkButton(mess, font= ("Calibri", 15, "bold"), text = "Ok", command = mess.destroy).grid(column = 0, row =2, pady = 5, padx = 10)
    mess.mainloop()

