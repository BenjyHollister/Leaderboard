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
def add_Score():
   
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


@app.route("/delete_entry", methods=["POST"])
def delete_entry():

   name = request.form.get("name")

   if not name:
      redirect("/leaderboard")

   Leaderboard.pop(name, None)

   with open(FILENAME, "w") as f: 
      json.dump(Leaderboard, f, indent=4)

   return redirect("/leaderboard")



if __name__ == "__main__":
   app.run(debug=True)
