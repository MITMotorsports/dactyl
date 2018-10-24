#!/usr/env/bin python

from functools import total_ordering
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

global err
err = False

global saved
saved = False

global pc
pc = None

PTERODACTYL = """
                             <\              _
                              \\          _/{
                       _       \\       _-   -_
                     /{        / `\   _-     - -_
                   _~  =      ( @  \ -        -  -_
                 _- -   ~-_   \( =\ \           -  -_
               _~  -       ~_ | 1 :\ \      _-~-_ -  -_
             _-   -          ~  |V: \ \  _-~     ~-_-  -_
          _-~   -            /  | :  \ \            ~-_- -_
       _-~    -   _.._      {   | : _-``               ~- _-_
    _-~   -__..--~    ~-_  {   : \:}
  =~__.--~~              ~-_\  :  /
                             \ : /__
                            //`Y'--\\
                           <+       \\
                            \\      WWW
  
  ██████╗      █████╗      ██████╗    ████████╗    ██╗   ██╗    ██╗     
  ██╔══██╗    ██╔══██╗    ██╔════╝    ╚══██╔══╝    ╚██╗ ██╔╝    ██║     
  ██║  ██║    ███████║    ██║            ██║        ╚████╔╝     ██║     
  ██║  ██║    ██╔══██║    ██║            ██║         ╚██╔╝      ██║     
  ██████╔╝    ██║  ██║    ╚██████╗       ██║          ██║       ███████╗
  ╚═════╝     ╚═╝  ╚═╝     ╚═════╝       ╚═╝          ╚═╝       ╚══════╝
                                                                        
"""

BAR = "////////////////////////////////////////////////////////////////"

TRANSFORM_NAMES = ["Identity", "Absolute value", "Negate", "Times 500", "Divide by 1000", "Enum to int * 500"]

class Signal(object):
    def __init__(self, name):
        self.name = name
        self.transform_fn = None

    def add_transformation(self, transform_fn):
        self.transform_fn = transform_fn

    def get_results(self, data, msgname):
        x = data[msgname][self.name]
        if self.transform_fn == "Identity":
            return (x, None)
        elif self.transform_fn == "Absolute value":
            return (list(map(abs, x)), None)
        elif self.transform_fn == "Negate":
            return (list(map(lambda v: -v, x)), None)
        elif self.transform_fn == "Times 500":
            return (list(map(lambda v: v*500, x)), None)
        elif self.transform_fn == "Divide by 1000":
            return (list(map(lambda v: v/1000, x)), None)
        elif self.transform_fn == "Enum to int * 500":
            keys = list(set(list(x)))
            idx = {k: i for i,k in enumerate(keys)}
            return (list(map(lambda v: idx[v], x)), idx)

    def __str__(self):
        return "Signal | {} => {}".format(self.name, self.transform_fn)

class Message(object):
    def __init__(self, name):
        self.name = name
        self.signals = {}

    def add_signal(self, signal):
        self.signals[signal.name] = signal

    def __str__(self):
        return "Message | {} {}".format(self.name, 
                "".join(["\n\t\t{}".format(x) for x in self.signals.values()]))

@total_ordering
class Graph(object):
    def __init__(self, name):
        self.name = name
        self.msgs = {}

    def add_msg(self, msg):
        if not msg.name in self.msgs:
            self.msgs[msg.name] = msg
        else:
            for s in msg.signals.values():
                self.msgs[msg.name].add_signal(s)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return "Graph | {} {}".format(self.name, 
                "".join(["\n\t{}".format(x) for x in self.msgs.values()]))

class Program(object):
    def __init__(self):
        self.name = "" 
        self.graphs = []

    def add_graph(self, graph):
        self.graphs.append(graph)

    def remove_graph(self, index):
        self.graphs.remove(index)

    def __str__(self):
        return "{}\n\nProgram | {} {}\n\n{}".format(BAR, self.name, 
                "".join(["\n  {} ) {}".format(i, x) for i,x in enumerate(self.graphs)]), BAR)

    def save(self):
        pass

    def load(self):
        pass

def askq_enum(q_string, items, sort_vals=True, multiple=False, clear=True, return_index=False):
    if clear:
        clear_screen()
    
    print("\n{}\n".format(q_string))
    sorted_list = sorted(items) if sort_vals else items
    for i,item in enumerate(sorted_list):
        print(" {} ) {}".format(i, item))

    if len(items) < 1:
        return None

    answer = input("\n>> ").split(",")
    output = []
    
    if len(answer) < 1:
        return None

    for v in answer:
        try:
            v = int(v)
            if not (0 <= v < len(items)):
                raise ValueError
            output.append(sorted_list[v] if not return_index else v)
        except ValueError:
            global err
            err = True
            return None

    print("")
    return output if multiple else output[0]

def clear_screen():
    print(chr(27) + "[2J")
   
    print(PTERODACTYL)
 
    global err
    if err:
        err = False
        print("")
        print(">> Error: invalid format for your answer or index out of range, skipping. <<")
        print("")

    global saved
    if saved:
        saved = False
        print("")
        print("The file was saved!")
        print("")
    
    global pc
    if pc is not None:
        # Prompt the user for new inputs
        print("Data file(s): {}".format(filename))
        print(pc)

def load_data_file():
    files = []
    for f in os.listdir('./'):
        if f.endswith('.npz'):
            files.append(f)

    files.sort()
    
    choice = askq_enum("Which file would you like to load?\n>> ", files)
    if choice is not None:
        data = np.load(choice)
        filename = choice
        return (data, filename)

    return None

def load_program():
    files = []
    for f in os.listdir('./'):
        if f.endswith('.pkl'):
            files.append(f)

    files.sort()

    choice = askq_enum("Which file would you like to load from this directory?\n>> ", files)
    if choice is not None:
        pc = None
        with open(choice, 'rb') as handle:
            pc = pickle.load(handle)
        fname_save = choice
        return (pc, fname_save)

    return None

if __name__ == "__main__":
    global pc
    data = None
    fname_save = ""
    filename = "No data has been loaded yet"
    while True:
        clear_screen()
        
        # Setup the program programuration if it has not already been init'd
        if pc is None or pc.name == "":
            choice = askq_enum("Starting Dactyl: \nWould you like to make a new program or load an old one?", 
                    ["Create new program", "Load program from file"])
            if choice == "Create new program":
                pc = Program()
                pc.name = str(input("New program name \n>> "))
                print("")
            elif choice == "Load program from file":
                pc = Program()
               
                result = load_program()
                if result is not None:
                    pc, fname_save = result
            else:
                continue

        if data is None:
            result = load_data_file()
            if result is not None:
                data, filename = result
            continue

        choice = askq_enum("What would you like to do?", 
                [
                    "New graph",
                    "New signal",
                    "Display",
                    "Remove graph",
                    "Remove message",
                    #"Remove signal",
                    "Load another file",
                    "Load another program",
                    "Save program",
                    "Exit"
                    ], sort_vals=False, clear=False)

        if choice == "New graph":
            graph_name = input("What would you like to call it?\n>> ")
            print("")
            pc.add_graph(Graph(graph_name))
        elif choice == "New signal":
            if len(pc.graphs) < 1:
                continue
            msgs = [k for k,v in data.items()]
            msg_choice = askq_enum("What message is the signal in?\n>> ", msgs)
            
            if msg_choice is None:
                continue

            signals = data[msg_choice].dtype.names
            sig_choices = askq_enum("What signals do you want? (use commas)\n>> ", 
                        signals, multiple=True)
                
            if sig_choices is None:
                continue
                
            m = Message(msg_choice)
            wasbad = False
            for s in sig_choices:
                trans_choice = askq_enum("{} : What transformation should be applied?"
                        .format(s), TRANSFORM_NAMES, sort_vals=False) 
                if trans_choice is None:
                    wasbad = True
                    break

                sig = Signal(s)
                sig.add_transformation(trans_choice)
                m.add_signal(sig)

            if wasbad:
                continue
                
            if len(pc.graphs) == 1:
                pc.graphs[0].add_msg(m)
            else:
                graph_choices = askq_enum(
                        "What graphs do you want to add it to? (use commas)\n>> ", 
                        pc.graphs, sort_vals=False, multiple=True)

                for g in graph_choices:
                    g.add_msg(m)

        elif choice == "Display":
            if len(pc.graphs) < 1:
                continue

            for g in pc.graphs:
                plt.figure()
                plt.title(g.name)
                plt.xlabel('time')
                for m in g.msgs.values():
                    time_axis = data[m.name]['time']
                    for s in m.signals.values():
                        vals, idx = s.get_results(data, m.name)
                        if idx is not None:
                            print("\nMAPPING FOR {}:\n{}\n".format(s.name, idx))
                        plt.plot(time_axis, vals, label=s.name)
                plt.legend()

            plt.show()

        elif choice == "Remove graph":
            choice = askq_enum("What graph would you like to remove (index)?\n>> ", pc.graphs, sort_vals=False)
            print("")
            if choice is not None:
                pc.remove_graph(choice)
        elif choice == "Remove signal":
            pass
        elif choice == "Remove message":
            choice = askq_enum("From what graph (index)?\n>> ", pc.graphs, sort_vals=False, return_index=True)
            if choice is not None:
                m_choice = askq_enum("What message would you like to remove (index)?\n>> ", 
                        pc.graphs[choice].msgs.keys())
                if m_choice is not None:
                    del pc.graphs[choice].msgs[m_choice]

        elif choice == "Load another file":
            result = load_data_file()
            if result is not None:
                data, filename = result
        elif choice == "Load another program":
            result = load_program()
            if result is not None:
                pc, fname_save = result
        elif choice == "Save program":
            fname = fname_save
            if fname == "":
                fname = str(input("What should the file name be? (.pkl)\n>> "))
                if fname == "":
                    global err
                    err = True
                    continue
                fname = fname.replace(".pkl", "")
                fname += ".pkl"
            
            with open(fname, 'wb') as handle:
                pickle.dump(pc, handle, protocol=pickle.HIGHEST_PROTOCOL)

            global saved
            saved = True

            fname_save = fname
            
        elif choice == "Exit":
            break
        else:
            continue

