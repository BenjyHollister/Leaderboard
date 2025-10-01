import json
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("window")
window.geometry("400x600")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

menu_frame = tk.Frame(window)
menu_frame.grid(row=0, column=0, sticky="nsew")

label = tk.Label(menu_frame, text="Welcome to the Leaderboards", font=('Arial', 18))
label.pack(padx=20, pady=20)

label = tk.Label(menu_frame, text="Main Menu", font=('Arial', 14))
label.pack(padx=20, pady=30)


btn1 = tk.Button(menu_frame, text="Leaderboard", width=25)
btn1.pack(pady=10)

btn2 = tk.Button(menu_frame, text="Help", width=25)
btn2.pack(pady=10)

btn3 = tk.Button(menu_frame, text="Exit", width=25)
btn3.pack(pady=10)

menu_frame.tkraise()

window.mainloop()

FILENAME = "leaderboard.json"    

#So that the scores which are altered are saved and we don't just have a hard-coded dictionary, we save it to a file

try:
   with open("leaderboard.json", "r") as f:
      Leaderboard = json.load(f)
except FileNotFoundError:
   Leaderboard = {'Benjy' : 50, "Sharlie" : 6, "Eliott" : 55} #use a dictionary to store names and scores

   #save immediately to create file
   with open(FILENAME, "w") as f:
      json.dump(Leaderboard, f)

exit = False

while exit == False:                    #add a break between when the last thing was executed til when the next choice is printed

   print("What would you like to do?")
   print("1. View Leaderboard")
   print("2. Add a score")
   print("3. Add a user")
   print("4. Delete a score")
   print("5. Exit")# make a 5th option, 'exit', that cancels the program when selected, and the program otherwise always returns to the menu
   choice = int(input("  : "))

   if choice == 1:
      print("Leaderboard: ")
      for k,v in sorted(Leaderboard.items(), key=lambda item: item[1], reverse = True):
         print(k,v)

   elif choice == 2:
      name = str(input("Who is this a new score for? "))
      new_score = int(input(f"Enter the new score for {name}: " ))
      Leaderboard[name] = new_score

   elif choice == 3:
      incomer = str(input("Who is the new user? "))
      Leaderboard.update({incomer: 0})


   elif choice == 4:
      name_del = str(input("Whose score would you like to delete? "))
      if name_del in Leaderboard:
         Leaderboard.pop(name_del)
         print(f"{name_del}'s score has been deleted")
      else:
         print(f"{name_del} was not found in leaderboard")
   
   elif choice == 5:
      print("Exiting program...")
      exit = True
   
   else:
      print("No option selected, select another option")


with open(FILENAME, "w") as f:
   json.dump(Leaderboard, f)

