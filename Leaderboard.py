import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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



#Leaderboard frame

   #previously had displaying of leaderboard, so need to be done in flask

@app.route("/leaderboard") #When this function is run, go to the url in the brackets
def leaderboard():
   sorted_board = sorted(Leaderboard.items(), key=lambda item: item[1], reverse=True)

   leaderboard_data = [
      {"rank": i+1, "name": name, "score": score}
      for i, (name, score) in enumerate(sorted_board)
   ]

   return render_template("leaderboard.html", leaderboard=leaderboard_data)


""" commented out until i can rewrite in for flask
def refresh_leaderboard():
   #This function will be for live updating and sorting the leaderboard when things are changed
   sorted_board = sorted(Leaderboard.items(), key=lambda item: item[1], reverse=True)
   for item in tree.get_children():
      tree.delete(item)
   for i, (name, score) in enumerate(sorted_board, start=1):
      tree.insert("", "end", values=(i, name, score))

refresh_leaderboard()
"""
""" all below is mixed logic/tkinter so is commented out so we can test step by step
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
   refresh_leaderboard()     #used for live updating

"""
@app.route("/add_player", methods=["POST"])   
def add_Player():
      
   name = request.form.get("name")

   if not name:
      return redirect("/leaderboard")
   
   Leaderboard[name] = 0.0

   with open(FILENAME, "w") as f:     #saving the new leaderboard to the file directly inside the function to fix the not saving score problem
      json.dump(Leaderboard, f, indent=4)

   return redirect("/leaderboard")
      
      

@app.route("/add_score", methods=["POST"])
def addScore():
   
   name = request.form.get("name")
   score = request.form.get("score")

   if not name:
      return redirect("/leaderboard")

   if not score:
      return redirect("/leaderboard")

   try:
      score = float(score)
   except ValueError:
      return redirect("/leaderboard")

   Leaderboard[name] = score

   with open(FILENAME, "w") as f:     #saving the new leaderboard to the file directly inside the function to fix the not saving score problem
      json.dump(Leaderboard, f, indent=4)

   return redirect("/leaderboard")


"""
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

            Leaderboard.pop(player, None)

            for i, item in enumerate(tree.get_children(), start=1):
               _, player, score = tree.item(item, "values")
               tree.item(item, values=(i, player, score))

            
            with open(FILENAME, "w") as f: 
               json.dump(Leaderboard, f, indent=4)
            #saving the new leaderboard with deleted members to the file, as currently they aren't deleted on the jsongit 

            messagebox.showinfo("Deleted", f"{deleted_player} has been removed from the leaderboard.")      
            popup.destroy()
            return
      #If name not found
      messagebox.showwarning("Not Found", f"No player name '{name}' found.")

      refresh_leaderboard()

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

"""

if __name__ == "__main__":
   app.run(debug=True)
