# Diabetes Monitoring System
Chance Gildart
Spring 2024
Human Computer Interaction, Dr. Ji Hwan Park

# How to run
This project uses Textual, which is a GUI interface for the terminal in Python. To be able to run this, you will need to download Textual using:

```pip3 install textual```

When that installs, you can run ```python3 -m textual``` to make sure you downloaded it correctly. For more information, visit https://textual.textualize.io/getting_started/.

Once textual is working, you can run ```python3 monitoringsystem.py``` to run the program.

When you run the program, you will be greeted with a screen that has three buttons: 2 for each name and one for the help. The help button will pull up the help documentation to allow the user to understand how to use the app. 

Selecting a name will pull up another menu that is personalized for that user with their name and ID at the top. It will ask the user if they have done a glucose check today. These menues are very similar for each user, but they will have their name and ID at the top. Selecting "Yes" will send the user to a screen that tells them that they can log out. Selecting "No" will send the user to a screen where they can input a reading.

After inputing a reading, the user can be directed to any of three different screens depending on their results. If their results are too low, it will send the user to a screen that reminds them to consume sugar and take the medicine their doctor prescribed. If their results are too high, it will send the user to a screen that tells them to contact their doctor immediately, and it will provide the doctor's information for the user's convenience. Both will also ask the user to describe what they ate and if they were feeling well. If the results are good, the user will be sent to a screen that tells them so.

On every screen (except for the log in screen and the help screen), they can opt to log out. This will end any process and return the user to the main menu.