import customtkinter
from apply import apply_styles

with open("style.css", "r") as f:
    css_data = f.read()

@apply_styles(css_data)
class MyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.entry = customtkinter.CTkEntry(self, placeholder_text='CTkEntry', width=140, height=28)
        self.otherentry = customtkinter.CTkEntry(self, placeholder_text='CTkEntry', width=140, height=28)

    def button_callback(self):
        print("button clicked")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
    