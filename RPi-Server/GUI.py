

from Tkinter import *
import ttk
import MySQLdb
import time

BASE = RAISED
SELECTED = FLAT

# a base tab class
class Tab(Frame):
	def __init__(self, master, name):
		Frame.__init__(self, master)
		self.tab_name = name
# the bulk of the logic is in the actual tab bar
class TabBar(Frame):
	def __init__(self, master=None, init_name=None):
		Frame.__init__(self, master)
		self.tabs = {}
		self.buttons = {}
		self.current_tab = None
		self.init_name = init_name

        #self.test()
	def show(self):
		self.pack(side=TOP, expand=YES, fill=X)
		self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab

	def add(self, tab):
		tab.pack_forget()									# hide the tab on init

		self.tabs[tab.tab_name] = tab						# add it to the list of tabs
		b = Button(self, text=tab.tab_name, relief=BASE,	# basic button stuff
			command=(lambda name=tab.tab_name: self.switch_tab(name)))	# set the command to switch tabs
		b.pack(side=LEFT)												# pack the buttont to the left mose of self
		self.buttons[tab.tab_name] = b											# add it to the list of buttons


	def switch_tab(self, name):
		if self.current_tab:
			self.buttons[self.current_tab].config(relief=BASE)
			self.tabs[self.current_tab].pack_forget()			# hide the current tab
		self.tabs[name].pack(side=BOTTOM)							# add the new tab to the display
		self.current_tab = name									# set the current tab to itself
        #
		self.buttons[name].config(relief=SELECTED)					# set it to the selected style

		#self.after(1000, self.onUpdate)
        def refresh(self):
            #print("test")

            conn = MySQLdb.connect("localhost", "root", "raspberry", "IUTMESH")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nodes")
            conn.close()
            for i in tree.get_children():
                tree.delete(i) #clears current values from tree
            for row in cursor:
           # I suppose the first column of your table is ID
                tree.insert('', 'end', '',values=(row[0],row[1], row[2], row[3],row[4]))
                #cpt += 1 # increment the ID
                #tree.insert('', 'end', ,values=(row[0],row[1], row[2], row[3],row[4]))
            tree.pack()
            root.after(1000,self.refresh)

if __name__ == '__main__':

        def write(x): print x
	def send_data(payload):
		f = open('data.shahin','w')
		f.write(str(payload))
		f.close()
        root = Tk()
        root.title("Isfahan University of Technology")

        #
    	bar = TabBar(root, "Info")

        tab1 = Tab(root, "Monitoring")				# notice how this one's master is the root instead of the bar
        tree = ttk.Treeview(tab1)
        tree['show'] = 'headings' #remove the first empty column :D

        tree["columns"] = ("id", "mode", "address", "data", "Last-Check")
        tree.column("id", width=50,anchor='center')
        tree.column("mode", width=50,anchor='center')
        tree.column("address", width=100,anchor='center')
        tree.column("data",width=100,anchor='center')
        tree.column("Last-Check",width=150,anchor='center')
        #tree.column("#0", width=0)
        #tree.heading("#0", text=':|', anchor='w')
        #tree.column("#0", anchor="w")
        tree.heading("id", text="#ID")
        tree.heading("mode", text="Mode")
        tree.heading("address", text="Address")
        tree.heading("data", text="Data")
        tree.heading("Last-Check", text="Last-Check")
        conn = MySQLdb.connect("localhost", "root", "raspberry", "IUTMESH")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nodes")
        conn.close()
        #cpt = 0 # Counter representing the ID of your code.

        for row in cursor:
       # I suppose the first column of your table is ID
            tree.insert('', 'end', '',values=(row[0],row[1], row[2], row[3],row[4]))
            #cpt += 1 # increment the ID
            #tree.insert('', 'end', ,values=(row[0],row[1], row[2], row[3],row[4]))
        tree.pack()

	tab2 = Tab(root, "Send Data")
	''' The next 4 lines is one way to receive the data '''
	#Label(tab2, text="Data to be sent:\nMode: [T/R]\nReceiver's Address: [0x010203]\nPayload: [0x112233445566]", bg='black', fg='white').pack(side=TOP, fill=BOTH, expand=YES)
	#txt = Text(tab2, width=50, height=5)
	#txt.focus()
	#txt.pack(side=TOP, fill=BOTH, expand=YES)
	#Button(tab2, text="Send ->", command=(lambda: send_data(txt.get('1.0', END).strip()))).pack(side=BOTTOM, expand=YES, fill=BOTH)
	''' This is more elegant '''
	Label(tab2, text="Mode").grid(row=0)
	Label(tab2, text="Address").grid(row=1)
	Label(tab2, text="Payload").grid(row=2)
	e1 = Entry(tab2)
	e2 = Entry(tab2)
	e3 = Entry(tab2)
	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)
	e3.grid(row=2, column=1)
	e1.insert(10,"T") # This is reserved for further development (other options)
	e2.focus()
	#Button(tab2, text='Clear', command=e1.insert(10,"Miller")).grid(row=3, column=0, sticky=W, pady=4)
	Button(tab2, text='Send', command=(lambda: send_data(e1.get()+'\n'+e2.get()+'\n'+e3.get()+'\n'))).grid(row=3, column=1, sticky=W, pady=4)
	tab3 = Tab(root, "Info")
	Label(tab3, bg='white', text="Coded By: Shahin Khoobehi").pack(side=LEFT, expand=YES, fill=BOTH)

	bar.add(tab1)                                   # add the tabs to the tab bar
	bar.add(tab2)
	bar.add(tab3)
	#bar.config(bd=2, relief=RIDGE)			# add some border

	bar.show()

        root.after(1000,bar.refresh)
        root.mainloop()
