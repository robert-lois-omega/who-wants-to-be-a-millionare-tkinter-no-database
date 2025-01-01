import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox
import time
import pygame
import os
import ast
global main_menu

# initialize pygame mixer
pygame.mixer.init()

class Sound_Effects:
    def __init__(self, generate):
        self.generate = generate
        self.counter = 00
    def stop_music():
        pygame.mixer.music.stop()
    def start_music_main():
        # load background music file
        pygame.mixer.music.load("Sound Effects/kbc.mp3")
        # start playing background music
        pygame.mixer.music.play(-1)  # -1 means infinite loop
    def start_music_lets_play():
        pygame.mixer.music.load("Sound Effects/lets play.mp3")
        pygame.mixer.music.play()
      # stop music after 3 seconds
    def start_music_correct_answer():
        pygame.mixer.music.load("Sound Effects/correct answer.mp3")
        pygame.mixer.music.play()
      # stop music after 3 seconds
    def start_music_wrong_answer():
        pygame.mixer.music.load("Sound Effects/wrong answer.mp3")
        pygame.mixer.music.play()
    def call():
        pygame.mixer.music.load("Sound Effects/call a friend.mp3")
        pygame.mixer.music.play()

class QuizGame(tk.Frame):
    def __init__(self, parent, main_menu):
        self.flagged_event = False
        self.main_menu = main_menu
        self.parent = parent
        self.disable_list = []
    
        # Life Line Validation
        self.Valid_call = True
        self.Valid_50_50 = True
        self.Valid_Aud = True

        #Stop the Music
        Sound_Effects.stop_music()
        Sound_Effects.start_music_lets_play()
        # Generate Question Buttons
        self.option_buttons = []

        self.questions = [

        ]

        with open('Text/questions.txt') as f:
            question_flow = [line.strip() for line in f.readlines()]

        options_flow = []
        with open('Text/options.txt', 'r') as f:
            for line in f:
                options_flow.append(line.strip())
        options_flow = [ast.literal_eval(str(item).replace('"', '')) for item in options_flow]

        with open('Text/answers.txt') as f:
            answers_flow = [line.strip() for line in f.readlines()]

        for i in range(len(question_flow)):
            new_question = {
                'question': question_flow[i],
                'options': options_flow[i],
                'answer': answers_flow[i]
                }
            self.questions.append(new_question)

        self.current_question = 0
        self.score = 0
        

        self.question_label = tk.Label(self.parent, text='',  font=("Helvetica", 20), bg='#8c52ff', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, wraplength=650)
        self.question_label.place(relx=0.5, rely=0.5, anchor="center", x=-250, y=-130)

 # Load the PNG images and create PhotoImage objects
        image1 = Image.open("Pictures/50button.png")
        resized_image1 = image1.resize((100, 100))
        image1 = ImageTk.PhotoImage(resized_image1)
        image2 = Image.open("Pictures/audbutton.png")
        resized_image2 = image2.resize((95, 95))
        image2 = ImageTk.PhotoImage(resized_image2)
        image3 = Image.open("Pictures/phonecall.png")
        resized_image3 = image3.resize((100, 100))
        image3 = ImageTk.PhotoImage(resized_image3)

        # Create the buttons and set their images
        self.button1_50_50 = tk.Button(self.parent, image=image1, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f', command=self.life_line_50_50)
        self.button1_50_50.image = image1
        self.button2_ask_the_audience = tk.Button(self.parent, image=image2, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f', command=self.life_line_Aud)
        self.button2_ask_the_audience.image = image2
        self.button3_phone_call = tk.Button(self.parent, image=image3, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f', command=self.life_line_Call)
        self.button3_phone_call.image = image3

        self.option_buttons.append(self.button1_50_50)
        self.option_buttons.append(self.button2_ask_the_audience)
        self.option_buttons.append(self.button3_phone_call)

        # Place the buttons
        self.button1_50_50.place(relx=0.5, rely=0.5, anchor="center", x=340, y=-180)
        self.button2_ask_the_audience.place(relx=0.5, rely=0.5, anchor="center", x=340, y=-20)
        self.button3_phone_call.place(relx=0.5, rely=0.5, anchor="center", x=340, y=140)
        
        # Generate Question Buttons
        self.option_buttons = []
        self.button1 = tk.Button(self.parent, text='', font=("Helvetica", 20), bg='#8c52ff', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=lambda option=0: self.check_answer(option))
        self.button2 = tk.Button(self.parent, text='', font=("Helvetica", 20), bg='#8c52ff', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=lambda option=1: self.check_answer(option))
        self.button3 = tk.Button(self.parent, text='', font=("Helvetica", 20), bg='#8c52ff', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=lambda option=2: self.check_answer(option))
        self.button4 = tk.Button(self.parent, text='', font=("Helvetica", 20), bg='#8c52ff', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=lambda option=3: self.check_answer(option))

        #Exit Button
        self.Exit_Button = tk.Button(text='Exit', font=("Helvetica", 20), bg='#221b6f', fg='white', relief="flat", highlightthickness=0, command=self.sudden_exit)
        self.Exit_Button.configure(fg='white', state="normal")
        self.Exit_Button.place(relx=0.5, rely=0.5, anchor="center", x=540, y=90)

        # A bug fix, for reconfiguring the old properties of the buttons
        self.button1.configure(fg='white', state="normal")
        self.button2.configure(fg='white', state="normal")
        self.button3.configure(fg='white', state="normal")
        self.button4.configure(fg='white', state="normal")
        self.option_buttons.append(self.button1)
        self.option_buttons.append(self.button2)
        self.option_buttons.append(self.button3)
        self.option_buttons.append(self.button4)

        # Place widgets
        self.button1.place(relx=0.5, rely=0.5, anchor="center", x=-460, y=140) #21
        self.button2.place(relx=0.5, rely=0.5, anchor="center", x=-60, y=140) #22
        self.button3.place(relx=0.5, rely=0.5, anchor="center", x=-460, y=5)  #11
        self.button4.place(relx=0.5, rely=0.5, anchor="center", x=-60, y=5)   #12

        self.score_label = tk.Label(self.parent, text='Score: 0', font=("Helvetica", 20), bg='#221b6f', fg='white')
        self.score_label.place(relx=0.5, rely=0.5, anchor="center", x=550, y=0)
        self.next_question()
    
    def sudden_exit(self):
        Sound_Effects.start_music_main()
        self.destroy_and_go_main()
    def change_background(self, bg_image):
        # change the background image of the main menu
        self.main_menu.bg_image_path = bg_image
        self.main_menu.bg_image = resize_image(self.main_menu.bg_image_path, self.main_menu.bg_image_width, self.main_menu.bg_image_height)
        self.main_menu.bg_label.config(image=self.main_menu.bg_image)

    def clear(self):
        del self.__dict__
    def next_question(self):
        self.button1.configure(fg='white', state="normal")
        self.button2.configure(fg='white', state="normal")
        self.button3.configure(fg='white', state="normal")
        self.button4.configure(fg='white', state="normal")

        if self.current_question == len(self.questions):
            root.update()
            # Create some widgets
            label1 = tk.Label(root, text="Hello")
            label2 = tk.Label(root, text="World")
            button = tk.Button(root, text="Refresh", command=lambda: root.update())
            self.button.place(relx=0.5, rely=0.5, anchor="center", x=340, y=-180)
            # Pack the widgets
            label1.pack()
            label2.pack()
            button.pack()
            tk.messagebox.showinfo('Quiz game', 'Quiz completed! Final score: ' + str(self.score))

        else:
            self.question_label.config(text=self.questions[self.current_question]['question'])
            random.shuffle(self.questions[self.current_question]['options'])
            for i in range(4):
                self.option_buttons[i].config(text=self.questions[self.current_question]['options'][i])
            self.current_question += 1
            self.flagged_event = False
    
    def life_line_50_50(self):
        question_deleted = 0
        #check if life line is still available
        if self.Valid_50_50:
            pygame.mixer.music.load("Sound Effects/50 50.mp3")
            pygame.mixer.music.play()
            for i in range(4):
                if (self.questions[self.current_question-1]['options'][i] == self.questions[self.current_question-1]['answer']) and question_deleted != 2:
                    pass        
                elif question_deleted != 2:
                    self.disable_list.append(i)
                    question_deleted += 1
                else:
                    pass
            #disable the choices for 50/50
            for k in self.disable_list:
                if k == 0:
                    self.button1.configure(fg='#8c52ff', state="disabled", disabledforeground="#8c52ff")
                elif k == 1:
                    self.button2.configure(fg='#8c52ff', state="disabled", disabledforeground="#8c52ff")
                elif k ==2:
                    self.button3.configure(fg='#8c52ff', state="disabled", disabledforeground="#8c52ff")
                elif k == 3:
                    self.button4.configure(fg='#8c52ff', state="disabled", disabledforeground="#8c52ff")
            self.button1_50_50.destroy()
            # Update the button
            image1 = Image.open("Pictures/50button_Cancel.png")
            resized_image1 = image1.resize((100, 100))
            image1 = ImageTk.PhotoImage(resized_image1)
            self.button1_50_50 = tk.Button(self.parent, image=image1, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f', command=self.life_line_50_50)
            self.button1_50_50.image = image1
            self.option_buttons.append(self.button1_50_50)
            self.button1_50_50.place(relx=0.5, rely=0.5, anchor="center", x=340, y=-180)
            self.Valid_50_50 = False
            self.flagged_event = True
        else:
            pass
    
    def life_line_Aud(self):
        def exit_log():
            Sound_Effects.stop_music()
            ratio_window.destroy()

        pygame.mixer.music.load("Sound Effects/ask_aud.mp3")
        pygame.mixer.music.play()
        # Create the main window
        ratio_window = tk.Tk()
        ratio_window.geometry("300x150")
        self.button2_ask_the_audience.destroy()
        image1 = Image.open("Pictures/audbutton_Cancel.png")
        resized_image1 = image1.resize((100, 100))
        image1 = ImageTk.PhotoImage(resized_image1)
        self.button2_ask_the_audience = tk.Button(self.parent, image=image1, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f')
        self.button2_ask_the_audience.image = image1
        self.option_buttons.append(self.button2_ask_the_audience)
        self.button2_ask_the_audience.place(relx=0.5, rely=0.5, anchor="center", x=340, y=-20)

        if (len(self.disable_list) == 0) or (self.flagged_event == False):
            # Generate random ratios
            ratio1 = random.randint(1, 100)
            ratio2 = random.randint(1, 100 - ratio1)
            ratio3 = random.randint(1, 100 - ratio1 - ratio2)
            ratio4 = 100 - ratio1 - ratio2 - ratio3

            # Put the ratios in a list and sort them in descending order
            ratios = [ratio1, ratio2, ratio3, ratio4]
            ratios_sorted = sorted(ratios, reverse=True)

            # Find the largest ratio
            largest = ratios_sorted[0]

            # Create the labels in the sorted order
            for ratio in ratios_sorted:
                label = tk.Label(ratio_window, text=self.questions[self.current_question-1]['options'][ratios.index(ratio)] + ": "+ str(ratio)+"%")
                label.pack()

            # Create the OK button that destroys the window
            ok_button = tk.Button(ratio_window, text="OK", command=exit_log)
            ok_button.pack()
        elif self.flagged_event == True:
            ratio1 = random.randint(1, 100)
            ratio2 = random.randint(1, 100 - ratio1)
            # Put the ratios in a list and sort them in descending order
            ratios = [ratio1, ratio2]
            ratios_sorted = sorted(ratios, reverse=True)
            ratio_head = 0
            for i in range(4):
                if i in self.disable_list:
                    pass
                else:
                    label = tk.Label(ratio_window, text=self.questions[self.current_question-1]['options'][i] + ": "+ str(ratios[ratio_head])+"%")
                    label.pack()
                    ratio_head += 1
            # Create the OK button that destroys the window
            ok_button = tk.Button(ratio_window, text="OK", command=exit_log)
            ok_button.pack()
        
        self.Valid_Aud = False
        self.disable_list.clear()
        # Start the main event loop
        ratio_window.mainloop()

    def life_line_Call(self):
        if self.Valid_call:
            random_responses = ["I am certain that it was ", "I think it was ", "Ow!, Boi! it was easy, its ", "As I remember in my senior year it was "]
            random_number = random.randint(1, 10)
            random_response = random.choice(random_responses)
            def exit_log():
                Sound_Effects.stop_music()
                new_window.destroy()
            def question_asked():
                label.config(text=self.questions[self.current_question-1]['question'])
                if (len(self.disable_list) == 8):
                    self.button_ask.destroy()
                    if random_number<=0:
                        response_final = random_response + self.questions[self.current_question-1]['answer']
                    else:
                        guess = random.choice(self.questions[self.current_question-1]['options'])
                        while guess == self.questions[self.current_question-1]['answer']:
                            guess = random.choice(self.questions[self.current_question-1]['options'])
                        response_final = random_response + guess
                else:
                    roll = random.randint(1, 2)
                    if roll == 1:
                        response_final = random_response + self.questions[self.current_question-1]['answer']
                    else:
                        for l in range(4):
                            if l in self.disable_list:
                                pass
                            else:
                                if self.questions[self.current_question-1]['options'][l] == self.questions[self.current_question-1]['answer']:
                                    pass
                                else:
                                    response_final = random_response + self.questions[self.current_question-1]['options'][l]
                self.button_ask.destroy()
                self.disable_list.clear()
                labelguess = tk.Label(new_window, text=response_final)
                labelguess.pack()
                self.button_chit_chat.destroy()
                self.button_chit_chat = tk.Button(new_window, text="Exit", command=exit_log)
                self.button_chit_chat.pack()
            def call():
                pygame.mixer.music.load("Sound Effects/calling.mp3")
                pygame.mixer.music.play()
                label.config(text="Calling...")
                root.update()
                time.sleep(3)
                # stop music after 3 seconds
                root.after(1000, Sound_Effects.call())
                label.config(text="Hello?")
                self.Valid_call = False
                self.button3_phone_call.destroy()
                image1 = Image.open("Pictures/phonecall_Cancel.png")
                resized_image1 = image1.resize((100, 100))
                image1 = ImageTk.PhotoImage(resized_image1)
                self.button3_phone_call = tk.Button(self.parent, image=image1, bg='#221b6f', borderwidth=0, highlightthickness=0, activebackground='#221b6f')
                self.button3_phone_call.image = image1
                self.option_buttons.append(self.button3_phone_call)
                self.button3_phone_call.place(relx=0.5, rely=0.5, anchor="center", x=340, y=140)
                entry.destroy()
                button.destroy()
                # create choices
                self.button_ask = tk.Button(new_window, text="Ask About the Question", command=question_asked)
                self.button_chit_chat = tk.Button(new_window, text="Just waste the life line", command=exit_log)
                self.button_ask.pack()
                self.button_chit_chat.pack()


            new_window = tk.Tk()
            new_window.title("PLDC LANDLINE")
            new_window.geometry("400x150")

            # create label and entry box
            label = tk.Label(new_window, text="Who do you want to call?")
            entry = tk.Entry(new_window)

            # create button to call
            button = tk.Button(new_window, text="Call", command=call)

            # add elements to window
            label.pack()
            entry.pack()
            button.pack()
            # show the window
            new_window.mainloop()

    def check_answer(self, option):
        selected_option = self.questions[self.current_question-1]['options'][option]
        #This fix is to prevent the buttons to be clicked while checking for the answer to be checked
        self.button1.configure(state="disabled", disabledforeground="#8c52ff")
        self.button2.configure(state="disabled", disabledforeground="#8c52ff")
        self.button3.configure(state="disabled", disabledforeground="#8c52ff")
        self.button4.configure(state="disabled", disabledforeground="#8c52ff")
        if selected_option == self.questions[self.current_question-1]['answer']:
            # Effects
            Sound_Effects.stop_music()
            Sound_Effects.start_music_correct_answer()
            # A bug fix, for reconfiguring the old properties of the buttons
            self.button1.configure(fg='white', state="normal")
            self.button2.configure(fg='white', state="normal")
            self.button3.configure(fg='white', state="normal")
            self.button4.configure(fg='white', state="normal")
            
            self.score += 1
            self.score_label.config(text='Score: ' + str(self.score))
            
        else:
            Sound_Effects.stop_music()
            Sound_Effects.start_music_wrong_answer()
            # A bug fix, for reconfiguring the old properties of the buttons
            self.button1.configure(fg='white', state="normal")
            self.button2.configure(fg='white', state="normal")
            self.button3.configure(fg='white', state="normal")
            self.button4.configure(fg='white', state="normal")

        if self.current_question >= len(self.questions):
            tk.messagebox.showinfo('Quiz game', 'Quiz completed! Final score: ' + str(self.score))
            Sound_Effects.start_music_main()
            self.destroy_and_go_main()
        else:
            self.next_question()
            #This will wrap Up Everything
    def destroy_and_go_main(self):
        self.score_label.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.button1_50_50.destroy()
        self.button2_ask_the_audience.destroy()
        self.button3_phone_call.destroy()
        self.question_label.destroy()
        self.Exit_Button.destroy()
        main_menu.default_reset()

def resize_image(image_path, width=None, height=None):
    # Load image from file
    image = Image.open(image_path)
    # Get screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # If width or height is not specified, resize image to fit screen
    if not width and not height:
        image_width, image_height = image.size
        aspect_ratio = image_width / float(image_height)
        if screen_width / float(screen_height) > aspect_ratio:
            new_image_width = int(aspect_ratio * screen_height)
            new_image_height = screen_height
        else:
            new_image_height = int(screen_width / aspect_ratio)
            new_image_width = screen_width
    else:
        new_image_width = width
        new_image_height = height
    image = image.resize((new_image_width, new_image_height), Image.ANTIALIAS)
    # Return resized image
    return ImageTk.PhotoImage(image)


class MainMenu(tk.Frame):
    def __init__(self, master, bg_image=None):
        super().__init__(master)
        self.master = master
        self.bg_image_path = bg_image
        self.bg_image_width = self.master.winfo_screenwidth()
        self.bg_image_height = self.master.winfo_screenheight()
        self.bg_image = resize_image(self.bg_image_path, self.bg_image_width, self.bg_image_height) if bg_image else None
        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def clear(self):
        del self.__dict__

    def on_resize(self, event):
        if self.bg_image:
            self.bg_image_width = self.master.winfo_screenwidth()
            self.bg_image_height = self.master.winfo_screenheight()
            self.bg_image = resize_image(self.bg_image_path, self.bg_image_width, self.bg_image_height)
            self.bg_label.config(image=self.bg_image)

    def create_widgets(self):
        # Set background image
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create other widgets
        self.button_start = tk.Button(self, text="START", font=("Helvetica", 20), bg='#191451', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=self.quiz_game)
        self.button_instructions = tk.Button(self, text="INSTRUCTIONS", font=("Helvetica", 20), bg='#191451', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=self.instruction_main)
        self.button_exit = tk.Button(self, text="EXIT", font=("Helvetica", 20), bg='#191451', fg='white', padx=20, pady=10, borderwidth=0, relief="flat", highlightthickness=0, command=root.destroy)

        # Place widgets
        self.button_start.place(relx=0.5, rely=0.5, anchor="center", x=25, y=150)
        self.button_instructions.place(relx=0.5, rely=0.5, anchor="center", x=25, y=250)
        self.button_exit.place(relx=0.5, rely=0.5, anchor="center", x=25, y=350)

        # Bind hover events
        self.button_start.bind("<Enter>", lambda event, button=self.button_start: self.button_hover(event, button))
        self.button_start.bind("<Leave>", lambda event, button=self.button_start: self.button_no_hover(event, button))
        self.button_instructions.bind("<Enter>", lambda event, button=self.button_instructions: self.button_hover(event, button))
        self.button_instructions.bind("<Leave>", lambda event, button=self.button_instructions: self.button_no_hover(event, button))
        self.button_exit.bind("<Enter>", lambda event, button=self.button_exit: self.button_hover(event, button))
        self.button_exit.bind("<Leave>", lambda event, button=self.button_exit: self.button_no_hover(event, button))


    def button_hover(self, event, button):
        button["fg"] = "yellow"
        button["font"] = ("Helvetica", 25)
        hover_sound = pygame.mixer.Sound('Sound Effects\zap.mp3')
        hover_sound.play()

    def button_no_hover(self, event, button):
        button["fg"] = "white"
        button["font"] = ("Helvetica", 20)

    def default_reset(self):
        self.bg_label.configure(image="")
        self.bg_image = resize_image("Pictures/Icongroup1.png")
        self.bg_label.configure(image=self.bg_image)
        self.create_widgets()


    def quiz_game(self):
        self.button_start.destroy()
        self.button_instructions.destroy()
        self.button_exit.destroy()
        self.bg_label.configure(image="")
        self.bg_image = resize_image("Pictures/startbackground.png")
        self.bg_label.configure(image=self.bg_image)
        game = QuizGame(self, main_menu)

    def instruction_main(self):
        def destroy_before_leaving():
            self.button_go_back.destroy()
            self.bg_label.configure(image="")
            self.bg_image = resize_image("Pictures/Icongroup1.png")
            self.bg_label.configure(image=self.bg_image)
            self.create_widgets()

        if self.bg_image:
            self.bg_label.configure(image="")
            self.bg_image = resize_image("Pictures/instructionimage.png")
            self.bg_label.configure(image=self.bg_image)
            self.button_start.destroy()
            self.button_instructions.destroy()
            self.button_exit.destroy()

            # Recreate the button
            self.button_go_back = tk.Button(self, text="Go Back", highlightthickness=2, bd=0, relief="groove", bg="black", fg="white", font=("Arial", 16), borderwidth=5, command=destroy_before_leaving)
            self.button_go_back.place(relx=0.5, rely=0.5, anchor="center", x=20, y=380)
            self.button_go_back.bind("<Enter>", lambda event, button=self.button_go_back: self.button_hover(event, button))
            self.button_go_back.bind("<Leave>", lambda event, button=self.button_go_back: self.button_no_hover(event, button))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game")
    root.attributes('-fullscreen', True) # Set full screen mode
    Sound_Effects.start_music_main()
    main_menu = MainMenu(root, bg_image="Pictures/Icongroup1.png")
    main_menu.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
