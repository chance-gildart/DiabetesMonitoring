from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Input, Button, DataTable, Static
from textual.screen import ModalScreen
from asyncio import sleep
from random import randint

ROWS = [
    ("Name", "ID", "Doctor", "Doctor's Number", "Low Glucose (mg/dL)", "Normal Glucose (mg/dL)", "High Glucose (mg/dL)"),
    ("Sara Norman", "5344-9709", "Dr. Jason Rosenberg", "579-0432", "<80", "80-140", ">140"),
    ("Gregg Norman", "1275-4307", "Dr. Nikhil Singh", "334-2309", "<70", "70-120", ">120"),
]

class MonitoringSystem(App): 
    CSS = """
    Screen {
        layout: vertical;
    }
    DataTable {
        height: 5fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Button("Help", id="help")

    def on_mount(self) -> None:
        for data_table in self.query(DataTable):
            data_table.loading = True  
            self.load_data(data_table)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "help":
            self.push_screen(Help())
        elif event.button.id == "Sara":
            self.push_screen(Sara())
        else:
            self.push_screen(Gregg())
    
    @work
    async def load_data(self, data_table: DataTable) -> None:
        await sleep(randint(2, 10))  
        data_table.add_columns(*ROWS[0])
        data_table.add_rows(ROWS[1:])
        data_table.loading = False  
    
class NewScreen(ModalScreen):
    def compose(self):
        with Container():
            yield Horizontal(
                VerticalScroll(
                    Static("Select your name to log in. When you log in, you will be greeted with a question asking you if you've checked your glucose yet today. If you have, select \"Yes\", and if you have not, select \"No\". If you select \"No\", it will then ask you to measure your glucose. Once you measure it, select \"Finished\" and input it into the box and select \"OK\". The software will then let you know if your glucose is too high, too low, or just right and then prompt you on what you should do next. If your glucose is abnormal, you will be asked to input why you believe that may be the case.", classes="static")
                )
            ),
            Button.error("Return to menu", id="return")
        
    @on(Button.Pressed)
    def leave_modal_screen(self, event):
        self.dismiss(event.button.id=="return")

class Sara(ModalScreen):
    def compose(self):
        with Container():
            yield Header("Sara Norman, ID:5344-9709")
            yield Static("Have you taken a glucose measurement today?")
            with Horizontal():
                yield Button.success("Yes", id="yes")
                yield Button.error("No", id="no")

                @on(Button.pressed)
                def button_pressed(self, event):
                    if (event.button.id == "yes"):
                        yield Static("Great! You do not need to do anything else today!")
                    else:
                        yield Static("Please take a glucose reading immediately and input the reading into the box below.")
                        yield Input("Glucose reading (mg/dL)")

if __name__ == "__main__":
    app = MonitoringSystem()
    app.run()