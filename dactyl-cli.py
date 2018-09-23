#!/usr/env/bin python

import numpy as np
import matplotlib.pyplot as plt
import os


fixes = [None, "Abs", "Flip sign (-)", "Multiply by 500"]
fixFns = {
	None: lambda v: v,
	"Abs": lambda v: abs(v),
	"Flip sign (-)": lambda v: -1.0 * v,
	"Multiply by 500": lambda v: 500 * v
}

def get_user_fix_choice():
	print "Available fixes: "
	for i,fix in enumerate(fixes):
		print i, ")", fix

	inchoice = int(raw_input("Your choice: "))
	return fixes[inchoice] if 0 <= inchoice < len(fixes) else None

def new_figure(data):
	plt.figure()
	print "Added new figure!"
	print ""

def get_user_datatype_choice(data):
	available_datatypes = [a for (a,b) in data.items()]

	print "Available datatypes:"
	for i,dtype in enumerate(available_datatypes):
		print i, ")", dtype

	inchoice = int(raw_input("Your choice: "))
	return available_datatypes[inchoice] if 0 <= inchoice < len(available_datatypes) else None

def get_user_signal_choice(data, dtype):
	signals = data[dtype].dtype.names
	for i,name in enumerate(signals):
		print i, ")", name

	inchoice = int(raw_input("Your choice: "))
	return signals[inchoice] if 0 <= inchoice < len(signals) else None

def new_subplot(data):
	dtype = get_user_datatype_choice(data)
	if dtype is None:
		return

	print "Datatype selected: ", dtype

	signal = get_user_signal_choice(data, dtype)

	if signal is None:
		return
	
	print "Signal selected: ", signal

	fix = get_user_fix_choice()

	print "Fix selected: ", fix
	
	fixed_data = map(fixFns[fix], data[dtype][signal])

	print "PLOTTING ............................"

	time_axis = data[dtype]['time']

	plt.plot(time_axis, fixed_data, label=signal)


	print "..............................PLOTTED"

def display(data):
	plt.legend()
	plt.show()
	print "Showed figures!"

def noop(data):
	print "Invalid action attempted"

commands = ["New figure", "New subplot", "Display"]
commandFns = {
	"New figure": new_figure,
	"New subplot": new_subplot,
	"Display": display,
	None: noop
}

def get_user_file_choice(files):
	print "Pick one of the following files to parse:"
	for i,f in enumerate(files):
		print i, ")", f

	inchoice = int(raw_input("Your choice: "))
	return files[inchoice] if 0 <= inchoice < len(files) else None



def get_user_action_choice():
	print "Available actions:"
	for i,a in enumerate(commands):
		print i, ")", a

	inchoice = int(raw_input("Your choice: "))
	return commands[inchoice] if 0 <= inchoice < len(commands) else None

def parse_and_display(filename):
	d = np.load(filename)
	
	action = None
	while True:
		inact = get_user_action_choice()
		print "Executing action: ", inact
		f = commandFns[inact]
		f(d)	


if __name__ == "__main__":
	
	files = []
	for f in os.listdir('./'):
		if f.endswith('.npz'):
			files.append(f)

	files.sort()

	choice = None
	while choice is None:
		choice = get_user_file_choice(files)

	print "You chose: ", choice
	print "Parsing...."

	# Parsing now
	parse_and_display(choice)

