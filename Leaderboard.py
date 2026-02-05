import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, ttk

window = tk.Tk()
window.title("window")
window.geometry("400x600")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

menu_frame = tk.Frame(window)
menu_frame.grid(row=0, column=0, sticky="nsew")

lb_frame = tk.Frame(window)
lb_frame.grid(row=0, column=0, sticky="nsew")


#Leaderboard frame

   #treeview 
columns = ("Rank", "Name", "Score")
tree = ttk.Treeview(lb_frame, columns=columns, show="headings", height=10)

for col in columns:
   tree.heading(col, text=col)
   tree.column(col, anchor="center", width=100)

tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

lb_frame.grid_rowconfigure(1, weight=1)
lb_frame.grid_columnconfigure((0,1,2), weight=1)



# FILE HANDLING

FILENAME = "leaderboard.json"  

   #file with GUI
try:
   with open(FILENAME, "r") as f:
      Leaderboard = json.load(f)
except FileNotFoundError:
   Leaderboard = {'Benjy' : 50.0, "Sharlie" : 6.0, "Eliott" : 55.0}
   with open(FILENAME, "w") as f:
      json.dump(Leaderboard, f, indent=4)

for row in tree.get_children():
   tree.delete(row)

sorted_board = sorted(Leaderboard.items(), key=lambda item: item[1], reverse=True)
for i, (name, score) in enumerate(sorted_board, start=1):
   tree.insert("", "end", values=(i, name, score))




#Button functions

def exit():
   quit() #closes the tkinter window

def help():
   help_frame = tk.Frame(menu_frame, bg="lightgrey")
   help_frame.place(relx=0.5, rely=0.5, anchor="center")

   helpLabel = tk.Label(help_frame, text="This explains everything", bg="lightgrey")
   helpLabel.pack(padx=10, pady=10)
   helpButton = tk.Button(help_frame, text="Close", command=help_frame.destroy)
   helpButton.pack(pady=5)
   
def toLeaderboard():
   lb_frame.tkraise()
   load_leaderboard()


def addPlayer():
   #add a prompt space to write who the new user is
   popup = tk.Toplevel(window)
   popup.title("Add Player")
   popup.geometry("300x150")
   #popup.resizable(False,False)
      
   addPrompt = tk.Label(popup, text="Who is this new user?", font=('Arial', 12))
   addPrompt.pack(pady=10)

   entry = tk.Entry(popup, width=25)
   entry.pack(pady=5)

   def submit():
      name = entry.get().strip()
      if not name:
         messagebox.showwarning("Input Error", "Please enter a name.")
         return
      
      rank = len(tree.get_children()) + 1
      tree.insert("", "end", values=(rank, name, 0))
      popup.destroy()


      Leaderboard[name] = 0.0
      with open(FILENAME, "w") as f:     #saving the new leaderboard to the file directly inside the function to fix the not saving score problem
         json.dump(Leaderboard, f, indent=4)

   submit_btn = tk.Button(popup, text="Submit", command=submit)
   submit_btn.pack(pady=10)
      
      
         #THE FUNCTION BELOW IS TOO COMPLICATED. SIMPLIFY IT AND THEN COMMIT TO GIT


def addScore():
   #add a prompt space to write who its for, then based on that add the score that they type in another prompt
   popup = tk.Toplevel(window)
   popup.title("Add Score")
   popup.geometry("300x180")
   #popup.resizable(False,False)

   namePrompt = tk.Label(popup, text="Who is this score for?", font=('Arial', 12))
   namePrompt.pack(pady=10)

   name_entry = tk.Entry(popup, width=25)
   name_entry.pack(pady=5)

   scorePrompt = tk.Label(popup, text="Enter new score: ", font=('Arial', 12))
   scorePrompt.pack(pady=5)

   score_entry = tk.Entry(popup, width=25)
   score_entry.pack(pady=5)

   def submit():
      name = name_entry.get().strip()
      score_text = score_entry.get().strip()
      score = float(score_text) #converting string to float so it can be added successfully to leaderboard file

      Leaderboard[name] = score
      with open(FILENAME, "w") as f:     #saving the new leaderboard to the file directly inside the function to fix the not saving score problem
         json.dump(Leaderboard, f, indent=4)

      if not name or not score_text:
         messagebox.showwarning("Missing Info", "Please enter both name and score.")
         return

      try:
         score = float(score_text)
      except ValueError:
         messagebox.showwarning("Invalid Score", "Score must be a number.")
         return

      # Update if player exists
      for item in tree.get_children():
         rank, player, old_score = tree.item(item, "values")
         if player.lower() == name.lower():
            tree.item(item, values=(rank, player, score))
            messagebox.showinfo("Updated", f"{player}'s score updated to {score}.")
            popup.destroy()
            return

      # Otherwise, add new player
      rank = len(tree.get_children()) + 1
      tree.insert("", "end", values=(rank, name, score))
      messagebox.showinfo("Added", f"{name} added with score {score}.")
      popup.destroy()
   
   submit_btn = tk.Button(popup, text="Submit", command=submit)
   submit_btn.pack(pady=10)



#Add menu dropdown
add_menu = tk.Menubutton(lb_frame, text="Add", width=15, relief="raised")
add_menu.menu = tk.Menu(add_menu, tearoff=0)
add_menu["menu"] = add_menu.menu

add_menu.menu.add_command(label="Add Player", command=addPlayer)
add_menu.menu.add_command(label="Add Score", command=addScore)

add_menu.grid(row=2, column=0, pady=10)

def delete():
   #add a prompt space to write who you're deleting, then based on that delete the score that they type in another prompt
   popup = tk.Toplevel(window)
   popup.title("Delete Score")
   popup.geometry("300x180")

   namePrompt = tk.Label(popup, text="Who's score are you deleting?", font=('Arial', 12))
   namePrompt.pack(pady=10)

   name_entry = tk.Entry(popup, width=25)
   name_entry.pack(pady=5)

   def confirm_delete():
      name = name_entry.get()
      #delete logic here
      popup.destroy

   def submit():
      #the logic for deleting an entry
      name = name_entry.get().strip()

      if not name:
         messagebox.showwarning("Missing Info", "Please enter a name to delete.")
         return
      
      #search and delete player
      for item in tree.get_children():
         rank, player, score = tree.item(item, "values")

         if player.lower() == name.lower():
            deleted_player = player #save deleted player, to fix messagebox error
            tree.delete(item)

            for i, item in enumerate(tree.get_children(), start=1):
               _, player, score = tree.item(item, "values")
               tree.item(item, values=(i, player, score))

            messagebox.showinfo("Deleted", f"{deleted_player} has been removed from the leaderboard.")      
            popup.destroy()
            return
      #If name not found
      messagebox.showwarning("Not Found", f"No player name '{name}' found.")

   submit_btn = tk.Button(popup, text="Submit", command=submit)
   submit_btn.pack(pady=10)


def back():
   menu_frame.tkraise()



#Main menu frame
label = tk.Label(menu_frame, text="Welcome to the Leaderboards", font=('Arial', 18))
label.pack(padx=20, pady=20)

label = tk.Label(menu_frame, text="Main Menu", font=('Arial', 14))
label.pack(padx=20, pady=30)

btn1 = tk.Button(menu_frame, text="Leaderboard", width=25, command=toLeaderboard)
btn1.pack(pady=10)

btn2 = tk.Button(menu_frame, text="Help", width=25, command=help)
btn2.pack(pady=10)

btn3 = tk.Button(menu_frame, text="Exit", width=25, command=exit)
btn3.pack(pady=10)

#Leaderboard frame

label = tk.Label(lb_frame, text="Shot Speed", font=('Arial', 18))
label.grid(row=0, column=0, columnspan=3, pady=20)

lb_btn2 = tk.Button(lb_frame, text = "Delete", width=15, command=delete) #, command=delete
lb_btn2.grid(row=2, column=1, pady=10)

lb_btn3 = tk.Button(lb_frame, text="Back", width=15, command=back)
lb_btn3.grid(row=2, column=2, pady=10)

menu_frame.tkraise()
window.mainloop()

      #MAKE A WAY TO SAVE AT THE END OF THE PROGRAM BACK TO THE FILE

#Following is the program for the terminal output
"""

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
"""

