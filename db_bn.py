#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Programm for accessing the db for the birdnames"""

from pysqlite2 import dbapi2 as sqlite
import os

# Database Folder
database = 'database/'

###########################################
#Dont't change anything below this
###########################################

class db_acess():
	def __init__(self, db):
		self.db = db
		# Checks if the database exists
		if not os.path.exists(db) : self.FirstRun()
		else:
			#Establish a connection and a cursor
			self.connection = sqlite.connect(db)
			self.cursor = self.connection.cursor()		

	def DelEntry(self, Row):
		return "Not Implemented yet"
		#Function to delete an Entry
		#self.cursor.execute('INSERT INTO bnames VALUES (null, ?, ?, ?, ?, ?, null, null, null)',(Euring, Abk, Gname, Lname, Ename))
		#self.connection.commit()
		
	def NewEntry(self, Euring, Abk, Gname, Lname, Ename):
		#Function to add a new Entry
		self.cursor.execute('INSERT INTO bnames VALUES (null, ?, ?, ?, ?, ?, null, null, null)',(Euring, Abk, Gname, Lname, Ename))
		self.connection.commit()		
		
	def ReturnRow(self, row):
		#Returns the Row in the Database with the given Number
		x = self.ReturnAll()
		if row == 0:
			return x[row]
		elif row > len(x):
			return
		else:
			return x[row-1]
	
	def HowMany(self):
		#Returns an Integer Number of Entry's
		self.cursor.execute('SELECT * FROM bnames')
		return len(self.cursor.fetchall())+1
	
	def SpecialFind(self,what,where):
		#Special Search for Words with Whitespace between
		#4 = latin, 5 = english
		what = what.upper()
		a = self.ReturnAll()
		Results = []
		for i in a:
			u = str(i[where])
			uu = u.partition(" ")[0]
			uuu = u.partition(" ")[2]
			if what != uu:
				pass
			else:
				Results.append((i[0]))
			if where == 5:
				if what != uuu:
					pass
				else:
					Results.append((i[0]))
		return Results


	def Find(self,what,start=1,end=3):
		#The Search-Prozedure searchs through all Strings in the
		#Database which contain the word
		#Start is where to beginn and end where to end
		what = what.upper()
		Results = []
		z = self.ReturnAll()
		for i in range(0, len(z)):
			for j in range(start,len(z[i])-end):
				#First (Exact Result)
				if what == z[i][j]:
					Results.append(z[i])
				try:
					#Second (Database Entry contains Words)
					if z[i][j].index(what):
						if not Results.__contains__(z[i]):
							Results.append(z[i])
				except ValueError:
					continue
				# Third (Take the First Words)
				val = z[i][j]
				lenw = len(what)
				if what == val[0:lenw]:
					if not Results.__contains__(z[i]):
						Results.append(z[i])
		return Results
	
	def ReturnAll(self, w ='all'):
		#Returns a List with all Entry's in the Database
		#If you permit a special Parameter, you can get special Output
		if w =='all':
			self.cursor.execute('SELECT * FROM bnames')
			return self.cursor.fetchall()
		elif w =='Euring':
			self.cursor.execute('SELECT Euring FROM bnames')
			return self.cursor.fetchall()
		elif w =='Abk':
			self.cursor.execute('SELECT Abk FROM bnames')
			return self.cursor.fetchall()
		elif w =='Gname':
			self.cursor.execute('SELECT Gname FROM bnames')
			return self.cursor.fetchall()
		elif w =='Lname':
			self.cursor.execute('SELECT Lname FROM bnames')
			return self.cursor.fetchall()
		elif w =='Ename':
			self.cursor.execute('SELECT Ename FROM bnames')
			return self.cursor.fetchall()
		else:
			return "No Entry"
		
	def FirstRun(self):
		# -------------------------
		# DON'T USE THIS ONE !
		# USE NewEntry()
		# -------------------------
		print "----------------------"
		print "No Database detected. Please give in the name of a File containing Birdnames"
		print "It has to be a file with 5 values in '' per row separated by an ,"
		print "'Euringnumber','Shortname','Germanname','Latinname','Englishname'"
		print "If you don't know what to do contact me: martinjung@gmx.net"
		print "-----------------------"
		data = raw_input(" Enter the name of the File: \n ")
		# Fill in the Data
		try:
			liste = open(data, 'r').xreadlines()
		except:
			print "The File can't be found. please Restart"
			return
		#Create the Database
		connection = sqlite.connect(self.db)
		cursor = connection.cursor()
		# Creating Database Tables
		cursor.execute('CREATE TABLE bnames (id INTEGER PRIMARY KEY, Category VARCHAR(5), Gname VARCHAR(50), Lname VARCHAR(50), Ename VARCHAR(50))')
		for zeile in liste:
			a = zeile.rsplit(',')
			Category = a[0]
			Category = Category[1:-1]
			Gname = a[1]			
			Gname = Gname[1:-1]
			Lname = a[3]
			Lname = Lname[1:-2]
			Ename = a[2]
			Ename = Ename[1:-1]
			cursor.execute('INSERT INTO bnames VALUES (null, ?, ?, ?, ?)',(Category, Gname, Lname, Ename))
		connection.commit()
		print "Sucessfully created Database"
		print "Please Restart !"
		connection.close()
	
	def CreateFilter4Test(self):
		db = db_acess(database+'db_names.db')
		x = db.ReturnAll('Lname')
		z = []
		f = open("fldb","w")
		for line in x:
			u = str(line[0])
			uu = u.partition(" ")[0]
		if uu in z:
			pass
		else:
			z.append(uu)
		z.sort()
		for i in z:
			f.write(i)
			f.write("\n")
		f.flush()
		f.close()
		f = open("fldb","r")
		data = f.readlines()
		print data
		f.close()
	
	
if __name__ == "__main__":
	db = db_acess(database+'db_names.db')
	x = db.ReturnAll('Lname')
	print db.SpecialFind("little",5)	