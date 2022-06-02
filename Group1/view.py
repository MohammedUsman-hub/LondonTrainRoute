from tkinter import Label, Button, Canvas
import tkinter as tk
from tkinter import ttk
from controller import searchButton_clicked, backButton_clicked, display_details


class startFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Creating the Title for the main menu of the GUI
        self.header = Label(self, text="Select Travel Route", width=20, font=("bold", 20)).place(x=90, y=53)
        # Creating text which is placed next to first drop-down menu
        self.label_journeyStart = Label(self, text="From:", width=20, font=("bold", 15)).place(x=50, y=125)
        # Creating text placed next to second drop-down menu.
        self.label_journeyEnd = Label(self, text="To:", width=20, font=("bold", 15)).place(x=50, y=155)

        self.searchButton = Button(self, text="Search", font=("Calibri 12"), width=20, bg='red', fg='white',
                                   command=lambda: searchButton_clicked(self, controller)).place(x=175,
                                                                                                 y=300)  # Creating the search button
        # Lists created to have the information appended to display within the drop down box
        list0 = []
        list1 = []
        # Temp file read where all the stations are stored
        temp_file = open("stations.txt", "r")
        for line in temp_file:
            list0.append(line.strip())
        temp_file.close()
        # Sorting the list for alphabetical order
        list0.sort()
        # Check system for duplicates to be removed
        list1 = list(dict.fromkeys(list0))

        js = tk.StringVar()
        # Creating the first drop-down menu and placing it onto a specific area within the main menu
        self.combo_journeyStart = ttk.Combobox(self, width=27, textvariable=js)
        self.combo_journeyStart['values'] = list1
        self.combo_journeyStart.place(x=210, y=130)

        je = tk.StringVar()
        # Creating the second drop-down menu and placing it onto a specific area within the main menu
        self.combo_journeyEnd = ttk.Combobox(self, width=27, textvariable=je)
        self.combo_journeyEnd['values'] = list1
        self.combo_journeyEnd.place(x=210, y=160)


class nextFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Title of the second page
        self.header = Label(self, text="Journey Details", width=20, font=("bold", 15)).place(x=0, y=5)
        # Creating button that will take user back to main menu
        self.backButton = Button(self, text="New Trip", width=10, bg='red', fg='white',
                                 command=lambda: backButton_clicked(self, controller)).place(x=400, y=5)
        # This is constructing the button that will display the route of the two chosen stations
        self.displayButton = Button(self, text="Display Route", width=28, bg='red', fg='white',
                                    command=lambda: display_details(self, controller)).place(x=20, y=65)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.tree = ttk.Treeview(self)
        self.tree.canvas = Canvas(width=500, height=500, relief='sunken')
        # Title of the columns that will display the route information
        self.tree['columns'] = ("station", "line", "stationTime", "totalTime")

        self.tree.column('#0', stretch=False, minwidth=0, width=100)
        self.tree.column('#1', stretch=False, minwidth=0, width=100)
        self.tree.column('#2', stretch=False, minwidth=0, width=120)
        self.tree.column('#3', stretch=False, minwidth=0, width=100)

        self.tree.heading("station", text="Station")
        self.tree.heading("line", text="Line")
        self.tree.heading("stationTime", text="Station Time(min)")
        self.tree.heading("totalTime", text="Total Time(min)")
        # Placing the title of the columns that will display the route information onto a specific part of the GUI
        self.tree.place(x=-100, y=100)

        # Text box to be used to display the summary of the route
        self.summary = tk.Text(self, width=60, heigh=9)
        self.summary.place(x=5, y=335)
        self.summary.config(relief="sunken")