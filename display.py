import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import *
import os
from PIL import Image
import main

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    WIDTH = 920
    HEIGHT = 760

    def __init__(self):
        super().__init__()
        self.title("Convert NFA-epsilon to DFA")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.transitionEntries = []
        # ============ create frames ============

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_bot = customtkinter.CTkFrame(master=self, width=740, height=250)
        self.frame_bot.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        self.frame_top = customtkinter.CTkFrame(master=self)
        self.frame_top.grid(row=0, column=0, sticky="nswe", padx=20, pady=10)

        self.frame_left = customtkinter.CTkFrame(master=self.frame_top, width=400, height=350)
        self.frame_left.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.frame_right = customtkinter.CTkFrame(master=self.frame_top, width=400)
        self.frame_right.grid(row=0, column=2, sticky="nswe", padx=10, pady=10)

        # =========== frame bot =================
        self.frame_bot_1 = customtkinter.CTkFrame(master=self.frame_bot, width=540, height=350)
        self.frame_bot_1.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        self.frame_bot_2 = customtkinter.CTkFrame(master=self.frame_bot, width=540, height=350)
        self.frame_bot_2.grid(row=1, column=1, sticky="nswe", padx=20, pady=10)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_bot_1,
                                              text="Input NFA-epsilon",
                                              font=customtkinter.CTkFont(size=15, weight="bold"))  # font name and size in px
        self.label_1.grid(row=1, column=0, sticky="nw", pady=5, padx=5)

        self.entry1 = customtkinter.CTkEntry(master=self.frame_bot_1,
                                             width=200,
                                             placeholder_text="State")
        self.entry1.grid(row=2, column=0, pady=5, padx=10, sticky="we")
        self.entry2 = customtkinter.CTkEntry(master=self.frame_bot_1,
                                             width=200,
                                             placeholder_text="Alphabets")
        self.entry2.grid(row=3, column=0, pady=5, padx=10, sticky="we")

        self.entry3 = customtkinter.CTkEntry(master=self.frame_bot_1,
                                             width=200,
                                             placeholder_text="Start")
        self.entry3.grid(row=2, column=1, pady=5, padx=10, sticky="we")

        self.entry4 = customtkinter.CTkEntry(master=self.frame_bot_1,
                                             width=200,
                                             placeholder_text="Final")
        self.entry4.grid(row=3, column=1, pady=10, padx=10, sticky="we")
        self.button_0 = customtkinter.CTkButton(master=self.frame_bot_1,
                                                text="Enter Transition Table",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event0)
        self.button_1 = customtkinter.CTkButton(master=self.frame_bot_1,
                                                text="NFA-e",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event1)
        self.button_0.grid(row=4, column=0, pady=10, padx=10, sticky="nswe")
        self.button_1.grid(row=4, column=1, pady=10, padx=10, sticky="nswe")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_bot_2,
                                              text="Transition Table",
                                              font=customtkinter.CTkFont(size=15))  # font name and size in px
        self.label_3.grid(row=0, column=2, sticky="n", pady=15, padx=10)
        self.frame_bot_2_1 = customtkinter.CTkFrame(master=self.frame_bot_2, width=0, height=0)
        self.frame_bot_2_1.grid(row=1, column=2, pady=5, padx=10)
        self.frame_bot_3 = customtkinter.CTkFrame(master=self.frame_bot, width=50, height=150)
        self.frame_bot_3.grid(row=1, column=3, pady=5, padx=10)
        self.button_2 = customtkinter.CTkButton(master=self.frame_bot_3,
                                                text="DFA",
                                                width=50,
                                                height=150,
                                                border_width=2,
                                                command=self.button_event2)
        self.button_2.grid(row=0, column=0, sticky="nswe")

    def on_closing(self, event=0):
        self.destroy()

    def button_event0(self):
        states = self.entry1.get().split()
        alphabets = self.entry2.get().split()
        alphabets.append('e')
        for cIDX, alphabet in enumerate(alphabets):
            alphabetLabel = customtkinter.CTkLabel(master=self.frame_bot_2_1,
                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                           text=alphabet)
            alphabetLabel.grid(row=0, column=cIDX + 1, pady=10, padx=10, sticky="we")

        for rIDX in range(len(states)):
            state = states[rIDX]
            transitionEntriesRow = []
            for cIDX in range(len(alphabets)):
                if cIDX == 0:
                    stateLabel = customtkinter.CTkLabel(master=self.frame_bot_2_1,
                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                           text=state)
                    stateLabel.grid(row=rIDX + 1, column=0, pady=10, padx=10, sticky="we")
                    entry = customtkinter.CTkEntry(master=self.frame_bot_2_1,
                                                   width=40,
                                                   placeholder_text="...")
                    entry.grid(row=rIDX + 1, column=1, pady=10, padx=10, sticky="we")
                    transitionEntriesRow.append(entry)
                else:
                    entry = customtkinter.CTkEntry(master=self.frame_bot_2_1,
                                                   width=40,
                                                   placeholder_text="...")
                    entry.grid(row=rIDX + 1, column=cIDX + 1, pady=10, padx=10, sticky="we")
                    transitionEntriesRow.append(entry)
            self.transitionEntries.append(transitionEntriesRow)

    def button_event1(self):
        states = self.entry1.get().split()
        alphabets = self.entry2.get().split()
        start = self.entry3.get().split()
        final = self.entry4.get().split()
        transition = []
        alphabets.append('e')
        for rIDX, state in enumerate(states):
            for cIDX, alphabet in enumerate(alphabets):
                inputs = self.transitionEntries[rIDX][cIDX].get().split()
                if len(inputs) > 0:
                    for input in inputs:
                        edge = [state, alphabet, input]
                        transition.append(edge)


        print(states, '\n', alphabets,'\n', start ,'\n', final,'\n', transition)
        alphabets.remove('e')
        self.nfa = main.NFA(len(states), states, len(alphabets), alphabets, start[0], len(final), final, len(transition), transition)
        main.render_nfa(self.nfa)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        imageFile = Image.open(os.path.join(image_path, "nfa.png"))
        width, height = imageFile.size
        self.nfa_image = customtkinter.CTkImage(imageFile, size=(width, height))
        self.nfa_fram = customtkinter.CTkLabel(master=self.frame_left, text="", image=self.nfa_image)
        self.nfa_fram.grid(row=0, column=0, padx=70, pady=10, sticky="nswe")

    def button_event2(self):
        main.render_dfa(self.nfa)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        imageFile = Image.open(os.path.join(image_path, "dfa.png"))
        width, height = imageFile.size
        self.dfa_image = customtkinter.CTkImage(imageFile, size=(width, height))
        self.dfa_fram = customtkinter.CTkLabel(master=self.frame_right,text="", image=self.dfa_image)
        self.dfa_fram.grid(row=0, column=0, padx=70, pady=10, sticky="nswe")

if __name__ == "__main__":
    app = App()
    app.mainloop()