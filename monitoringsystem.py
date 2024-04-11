# Written by Chance Gildart
# Human Computer Interaction Spring 2024
# Diabetes Monitoring System

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Input, Button, Static
from textual.screen import ModalScreen

# The interface itself
class MonitoringSystem(App): 
    # Style
    CSS = """
    Screen {
        layout: vertical;
    }
    DataTable {
        height: 5fr;
    }
    """

    # Create the buttons
    def compose(self) -> ComposeResult:
        yield Button("Sara Norman", id="sara")
        yield Button("Gregg Norman", id="gregg")
        yield Button("Help", id="help")
        yield Button("Quit", id="quit")
    
    # When Sara selects whether or not she has taken a reading, this is called
    def sara_action(self, str):
        # Send Sara's good job screen since she did her reading already
        if str == "yes":
            self.push_screen(SaraGoodJob())
        # Send Sara's reading screen so that she can input her reading.
        elif str == "no":
            self.push_screen(SaraReading(), self.sara_reading)
    
    # When Sara inputs her reading, this is called
    def sara_reading(self, int):
        # She selected "log out"
        if int == -1:
            pass
        # The number she put in was a low glucose level
        elif int < 80:
            self.push_screen(SaraTooLow())
        # The number she put in was a high glucose level
        elif int > 140:
            self.push_screen(SaraTooHigh())
        # The number she put in was a good glucose level
        else:
            self.push_screen(SaraGoodLevel())

    # When Gregg selects whether or not he took his reading, this is called
    def gregg_action(self, str):
        # Send Gregg's Good Job screen since he took his reading
        if str == "yes":
            self.push_screen(GreggGoodJob())
        # Redirect Gregg to put his reading in
        elif str == "no":
            self.push_screen(GreggReading(), self.gregg_reading)
    
    # When Gregg inputs his reading, this is called
    def gregg_reading(self, int):
        # He selected "log out"
        if int == -1:
            pass
        # His glucose is low
        elif int < 70:
            self.push_screen(GreggTooLow())
        # His glucose is high
        elif int > 120:
            self.push_screen(GreggTooHigh())
        # His glucose is at a good level
        else:
            self.push_screen(GreggGoodLevel())

    # When a user selects either name or the help button, this is called
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Help button pushed, pull up the help screen
        if event.button.id == "help":
            self.push_screen(Help())
        # Sara selected, pull up Sara's account
        elif event.button.id == "sara":
            self.push_screen(Sara(), self.sara_action)
        # Gregg selected, pull up Gregg's account
        elif event.button.id == "gregg":
            self.push_screen(Gregg(), self.gregg_action)
        elif event.button.id == "quit":
            self.exit()

# The help screen
class Help(ModalScreen[bool]):
    # Create the text and the return button
    def compose(self):
        with Container():
            yield Static("Click your name to log in. When you log in, you will be greeted with a question asking you if you've checked your glucose yet today. If you have, select \"Yes\", and if you have not, select \"No\". \n\nIf you select \"No\", it will then ask you to measure your glucose. Once you measure it, input it into the box and select \"OK\". \n\nThe software will then let you know if your glucose is too high, too low, or just right and then prompt you on what you should do next. \n\nIf your glucose is abnormal, you will be asked to input some more information on why that may be the case.", classes="static")
            yield Button.error("Return to menu", id="return")
    # When the return button is pressed, return back to the menu
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)

# Sara's account screen
class Sara(ModalScreen[str]):
    # Create the text and buttons
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nHave you taken a glucose measurement today?")
            # Make the buttons side by side and color coded.
            with Horizontal():
                yield Button.success("Yes", id="yes")
                yield Button.error("No", id="no")
            # Create the log out button at the bottom
            yield Button.error("Log out", id="return")

    # When a button is pressed, return its ID to the app to allow for it to go to the correct screen
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)

# Gregg's account screen
class Gregg(ModalScreen[str]):
    # Create the text and buttons
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nHave you taken a glucose measurement today?")
            # Make the buttons side by side and color coded.
            with Horizontal():
                yield Button.success("Yes", id="yes")
                yield Button.error("No", id="no")
            # Create the log out button at the bottom
            yield Button.error("Log out", id="return")

    # When a button is pressed, return its ID to the app to allow for it to go to the correct screen
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)

# The screen presented when Sara selects "Yes"
class SaraGoodJob(ModalScreen):
    # Create the text and log out button
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nGreat job! You do not need to do anything else. Please click the log out button below to finish!")
            yield Button.error("Log Out", id="return")

    # When the log out button is clicked, return to the original menu.
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "return")

# The screen presented when Gregg selects "Yes"
class GreggGoodJob(ModalScreen):
    # Create the text and log out button
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nGreat job! You do not need to do anything else. Please click the log out button below to finish!")
            yield Button.error("Log Out", id="return")

    # When the log out button is clicked, return to the original menu.
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "return")

# The screen presented when Sara selects "No"
class SaraReading(ModalScreen[int]):
    # Create the text, textbox, and the buttons
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nPlease take a reading of your glucose immediately. \n\nOnce you are finished, please input your reading into the textbox below and click \"OK\".")
            yield Input(placeholder="Glucose Reading (mg\dL)", type="integer", id="input")
            yield Button.success("OK", id="ok")
            yield Button.error("Log Out", id="return")

    # Check which button was pressed, and return the correct value
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Return -1 to make sure the app knows that this was a log out and not a submission
        if event.button.id == "return":
            self.dismiss(-1)
        # This is a submission, check the value to make sure it's in bounds, and return it to the app if it is
        else:
            val = int(self.query_one(Input).value)
            if val >= 0 and val <= 999:
                self.dismiss(val)
            # The value is not in bounds, clear the textbox and wait for another input
            else:
                self.query_one(Input).clear()

# The screen presented when Gregg selects "No"
class GreggReading(ModalScreen[int]):
    # Create the text, textbox, and the buttons
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nPlease take a reading of your glucose immediately. \n\nOnce you are finished, please input your reading into the textbox below and click \"OK\".")
            yield Input(placeholder="Glucose Reading (mg\dL)", type="integer", id="input")
            yield Button.success("OK", id="ok")
            yield Button.error("Log Out", id="return")

    # Check which button was pressed, and return the correct value
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Return -1 to make sure the app knows that this was a log out and not a submission
        if event.button.id == "return":
            self.dismiss(-1)
        # This is a submission, check the value to make sure it's in bounds, and return it to the app if it is
        else:
            val = int(self.query_one(Input).value)
            if val >= 0 and val <= 999:
                self.dismiss(val)
            # The value is not in bounds, clear the textbox and wait for another input
            else:
                self.query_one(Input).clear()

# The screen presented when Sara's input falls below her good glucose level interval
class SaraTooLow(ModalScreen[bool]):
    # Create the buttons, text, and textbox
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nYour blood sugar is low. Please consider eating something with sugar or taking the medicine your doctor prescribed.\n\nPlease tell us about what you've eaten or if you are feeling ill today in the textbox below. Click \"Submit\" when you're finished.")
            yield Input()
            yield Button.success("Submit", id="submit")
            yield Button.error("Log Out", id="return")
    
    # Check the button pressed and complete the correct action
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # If the logout button was pressed, send the user back to the main menu
        if event.button.id=="return":
            self.dismiss(True)
        # If the submit button was selected, take the textbox and submit button off the screen
        else:
            self.query_one(Input).visible = False
            # Find the submit button in the list of buttons and turn it off
            for button in self.query(Button):
                if button.id == "submit":
                    button.visible = False

# The screen presented when Gregg's input falls below her good glucose level interval
class GreggTooLow(ModalScreen[bool]):
    # Create the buttons, text, and textbox
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nYour blood sugar is low. Please consider eating something with sugar or taking the medicine your doctor prescribed.\n\nPlease tell us about what you've eaten or if you are feeling ill today in the textbox below. Click \"Submit\" when you're finished.")
            yield Input()
            yield Button.success("Submit", id="submit")
            yield Button.error("Log Out", id="return")
    
    # Check the button pressed and complete the correct action
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # If the logout button was pressed, send the user back to the main menu
        if event.button.id=="return":
            self.dismiss(True)
        # If the submit button was selected, take the textbox and submit button off the screen
        else:
            self.query_one(Input).visible = False
            # Find the submit button in the list of buttons and turn it off
            for button in self.query(Button):
                if button.id == "submit":
                    button.visible = False

# The screen presented when Sara's input falls above her good glucose levels
class SaraTooHigh(ModalScreen[bool]):
    # Create the buttons, text, and textbox
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nYour blood sugar is high. Please contact your doctor immediately. Their contact info is below:\n\nDr. Jason Rosenberg\nPhone Number: 579-0432\n\nPlease tell us about what you've eaten or if you are feeling ill today in the textbox below. Click \"Submit\" when you're finished.")
            yield Input()
            yield Button.success("Submit", id="submit")
            yield Button.error("Log Out", id="return")
    
    # Check the button pressed and complete the correct action
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # If the logout button was pressed, send the user back to the main menu
        if event.button.id=="return":
            self.dismiss(True)
        # If the submit button was selected, take the textbox and submit button off the screen
        else:
            self.query_one(Input).visible = False
            # Find the submit button in the list of buttons and turn it off
            for button in self.query(Button):
                if button.id == "submit":
                    button.visible = False

# The screen presented when Gregg's input falls above her good glucose levels
class GreggTooHigh(ModalScreen[bool]):
    # Create the buttons, text, and textbox
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nYour blood sugar is high. Please contact your doctor immediately. Their contact info is below:\n\nDr. Nikhil Singh\nPhone Number: 334-2309\n\nPlease tell us about what you've eaten or if you are feeling ill today in the textbox below. Click \"Submit\" when you're finished.")
            yield Input()
            yield Button.success("Submit", id="submit")
            yield Button.error("Log Out", id="return")
    
    # Check the button pressed and complete the correct action
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # If the logout button was pressed, send the user back to the main menu
        if event.button.id=="return":
            self.dismiss(True)
        # If the submit button was selected, take the textbox and submit button off the screen
        else:
            self.query_one(Input).visible = False
            # Find the submit button in the list of buttons and turn it off
            for button in self.query(Button):
                if button.id == "submit":
                    button.visible = False

# The screen that presents when Sara's input is within her good glucose interval
class SaraGoodLevel(ModalScreen[bool]):
    # Create the text and the log out button
    def compose(self):
        with Container():
            yield Static("Sara Norman, ID: 1275-4307\n\n\nYour blood sugar is at a good level. Good job! You do not need to do anything else, you may log out when you are finished.")
            yield Button.error("Log Out", id="return")

    # When the log out button is pressed, return to the main menu
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)

# The screen that presents when Gregg's input is within her good glucose interval
class GreggGoodLevel(ModalScreen[bool]):
    # Create the text and the log out button
    def compose(self):
        with Container():
            yield Static("Gregg Norman, ID: 5344-9709\n\n\nYour blood sugar is at a good level. Good job! You do not need to do anything else, you may log out when you are finished.")
            yield Button.error("Log Out", id="return")

    # When the log out button is pressed, return to the main menu
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)


if __name__ == "__main__":
    app = MonitoringSystem()
    app.run()