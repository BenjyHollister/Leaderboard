import json

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
while exit == False:

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

