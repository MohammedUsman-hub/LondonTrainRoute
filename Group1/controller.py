import openpyxl
import tkinter.messagebox as tm
import collections
from collections import namedtuple, deque

# Multiple global lists that will be requested within searchButton and Display Button
path = []
path_line = []
path_lines = []

total_time_list = []
summary = []
stations = []
# Start of reading the spreadsheet through openpyxl
book = openpyxl.load_workbook('London Underground data.xlsx')
sheet = book.active


# Code gathered for a Doubly Linked List (DLL)
class Node(object):
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev


class DoublyLinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    # Appends items into the designated list against a head and tail
    def append_item(self, data):
        new_item = Node(data, None, None)
        if self.head is None:
            self.head = new_item
            self.tail = self.head
        else:
            new_item.prev = self.tail
            self.tail.next = new_item
            self.tail = new_item

        self.count += 1

    # Used to print out the data within the DLL if desired
    def print_forward(self):
        for node in self.iter():
            print(node)

    # Iterates through the same list that is being checked to gather a reversal of the list in itself
    def iter(self):
        current = self.head
        while current:
            item_val = current.data
            current = current.next
            yield item_val


# Sets all data to have the functions of the DLL
all_data = DoublyLinkedList()
# Reading of the spreadsheet is started where we are taking all the information from the sheet and will work with
# different statements / appends
for row in sheet.iter_rows(min_row=1, min_col=1, max_row=800, max_col=4):

    stations_row = []

    for cell in row:
        stations_row.append(cell.value)
    # Iterating through the spreadsheet at points where stations are from one to another
    # This is to cut down the data to what is specifically needed, enhancing the efficiency of the algorithms
    if stations_row[2] is not None:
        stations.append(stations_row)
        all_data.append_item(stations_row)

        # Here we are running through a station reverse for the list to check against the inputted data from the user
        # Without this appended reverse we wont be able to go back and forth on user searches with the correct data
        reversed_stations_row = stations_row[:]
        element0 = reversed_stations_row[1]
        reversed_stations_row[1] = reversed_stations_row[2]
        reversed_stations_row[2] = element0

        stations.append(reversed_stations_row)
        all_data.append_item(reversed_stations_row)


def searchButton_clicked(self, controller):
    global path, path_line, path_lines, total_time_list, summary, stations
    # To keep each search of the program clear and consistent we are clearing all the data that was cached
    path.clear()
    path_line.clear()
    path_lines.clear()

    total_time_list.clear()
    summary.clear()

    # Gathers the data from the combo boxes
    journeyStartTxt = getattr(self, "combo_journeyStart")
    journeyStart = journeyStartTxt.get()

    journeyEndTxt = getattr(self, "combo_journeyEnd")
    journeyEnd = journeyEndTxt.get()

    # Dijkstra's Algorithm was gathered from https://rosettacode.org/wiki/Dijkstra%27s_algorithm#Python
    inf = float('inf')
    Edge = namedtuple('Edge', ['line', 'start', 'end', 'cost'])

    class Graph():
        def __init__(self, edges):
            self.edges = [Edge(*edge) for edge in edges]
            self.vertices = {e.start for e in self.edges} | {e.end for e in self.edges}

        def dijkstra(self, source, dest):
            assert source in self.vertices
            dist = {vertex: inf for vertex in self.vertices}
            previous = {vertex: None for vertex in self.vertices}
            dist[source] = 0
            q = self.vertices.copy()
            neighbours = {vertex: set() for vertex in self.vertices}
            for line, start, end, cost in self.edges:
                neighbours[start].add((end, cost))

            while q:
                u = min(q, key=lambda vertex: dist[vertex])
                q.remove(u)
                if dist[u] == inf or u == dest:
                    break
                for v, cost in neighbours[u]:
                    alt = dist[u] + cost
                    if alt < dist[v]:
                        dist[v] = alt
                        previous[v] = u
            s, u = deque(), dest
            while previous[u]:
                s.appendleft(u)
                u = previous[u]
            s.appendleft(u)
            return s

    # Expression of using the DLL against the Dijkstra
    graph = Graph(all_data.iter())
    # Having this try statement is a error check system if the data within the entries is missing or not the same
    try:
        # Using collections to run through the deque and append to a list to iterate through
        d = collections.deque(graph.dijkstra(journeyStart, journeyEnd))
        if d is None:
            pass

        while True:
            try:
                path.append(d.popleft())
            except IndexError:
                break
        # The for loop iterates through the items and checks if the item in the correct aspect when running through the
        # list. Due to the reversal of the lists, the program does not need to run a check twice.
        for i in range(len(path)):
            prev_station = ""
            for row in stations:
                if i < len(path) - 1:
                    if path[i] == row[1] and path[i + 1] == row[2] and row[1] is not prev_station:
                        path_line = [row[0], row[1], row[2], row[3]]
                        path_lines.append(path_line)
                        prev_station = row[1]
        # Takes the "cost" from Dijkstra's and sets it as an int to be able to combine together for the total time
        total_time = 5
        for line in path_lines:
            for i in range(len(path) - 1):
                for j in range(1, len(path)):
                    if path[i] == line[1] and path[j] == line[2]:
                        total_time = total_time + int(line[3] + 1)
                        total_time_list.append(total_time)
        # Error check if the combo boxes are the same when the user selects the data
        if journeyStart == journeyEnd:
            tm.showerror("Incorrect Information", "Same stations entered")
        else:
            controller.show_frame("nextFrame")

    except:
        tm.showerror("Incorrect Information", """Either:
    1. You have entered the incorrect station name
    2. Indentation present at the start or end where data entered""")


def display_details(self, controller):
    # Taking in the aspect that path_lines is a list within a list it can be difficult to append the total time of
    # the list at the end. So using this statement and matching each time to its correct adjacent time.
    display_route_end = [[x, *z] for x, z in zip(total_time_list, path_lines)]
    # Delete's any records that have been left on the tree
    records = self.tree.get_children()
    for element in records:
        self.tree.delete(element)
    # As the data that was previously there within the tree or cached from a previous run is now deleted, we insert
    # into the tree where we wanna append the data to station, line, station time, total time as represented as row
    for row in display_route_end:
        self.tree.insert('', 'end', text=str(), values=(row[2], row[1], row[4], row[0]))
    #   Finally detail of the journey
    self.tree.insert('', 'end', text=str(), values=(path[-1], "End Journey", "", ""))

    summary = []

    for i in range(len(path_lines)):
        summary_row = []
        # The summary goes back and forth through checking the previous stations until the matched requirement is found
        current_line = path_lines[i][0]

        previous_line = ""
        if i > 0:
            previous_line = path_lines[i - 1][0]

        next_line = ""
        if i < len(path_lines) - 1:
            next_line = path_lines[i + 1][0]
        # When the current line is not the previous line it tells us that the path of the stations has come to an end on
        # that specific line and then looks to work on the next line in play
        if current_line is not previous_line:
            summary_row.append("{}".format(current_line))
            summary_row.append("from {}".format(path_lines[i][1]))

        if next_line is not current_line:
            summary_row.append("to {} - change to".format(path_lines[i][2]))
        # Append the data gathered from the summary of the lines above
        if i < len(path_lines) - 1:
            summary.append(summary_row)
        else:
            summary_row.pop()
            summary_row.append("to {}".format(path[-1]))
            summary.append(summary_row)
    # Clearing the summary texts and readying the next implementation when needed
    self.summary.delete("1.0", 'end')
    # Simple insert into the summary
    for row in summary:
        for item in row:
            self.summary.insert("end", item)
            self.summary.insert("end", "\n")
    # Inserting the last data of the total travel time
    self.summary.insert("end", "Total travel time: ")
    self.summary.insert("end", total_time_list[-1])
    self.summary.insert("end", " minutes")
    # Disables the summary text so the data can not be changed and moved around from the user
    self.summary.config(state="disabled")


def backButton_clicked(self, controller):
    # As the back button is pressed the records of the tree and text are deleted so once a new search comes in the
    # data is cleared for the next display_details
    records = self.tree.get_children()
    for element in records:
        self.tree.delete(element)
    self.summary.config(state="normal")
    self.summary.delete("1.0", 'end')

    controller.show_frame("startFrame")
