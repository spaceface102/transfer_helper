#!/usr/bin/python3
import sys
import pickle #used to serialize data for later use; store dicts in bytes

def store(data, fname):
	"pickle data and store into fname"
	with open(fname, "wb") as f:
		pickle.dump(data, f)


def extract(fname):
	"unpickle data and return if for use in other funcs"
	try:
		with open(fname, "rb") as f:
			temp = pickle.load(f) 
	except:
		print(f"Initilizing... {fname}\n")
		store(dict(), fname)
		return extract(fname)
	else:
		return temp


def process_name(name):
	"make sure that course is easily found in set, even with small variations"
	name = name.replace(' ', '')
	name = name.replace('\t', '')
	name = name.replace('-', '')
	return name.upper()


def addnew(name = None, course_dict = {}): 
	"add a new school's transfer requirments"
	if not len(course_dict): #reduce the number of times opening file to unpickle
		course_dict = extract()
	print("\n")#spacer
	if not name:
		name = process_name(input("What is the name of the instituion: "))
	print("\nPlease input the courses related with this institution")
	print("Enter 'q' when you are finished")
	print("NOTE: If you miss typed a course name use 'b'!")	
	count = 1
	prev_course = None
	while((c := input("%d: " %(count))) != 'q'):
		if c == 'b' and prev_course:	
			course_dict[prev_course].discard(name) #remove name from set associated w/ course
			print("Removed %s from %s's course list!" %(course, name)) 
			continue
		c = process_name(c)
		if c in course_dict:
			course_dict[c].add(name)
		else:
			course_dict[c] = {name} #set to ensure no repeats, also checkschool() benifit
		prev_course = c
		count += 1
	store(course_dict)


def checkschool(name = None, course_dict = {}):
	"print all the courses related with a specific course"
	if not len(course_dict):
		course_dict = extract()
	print("\n")#spacer
	if not name:
		name = process_name(input("What is the name of the instituion: "))
	print(f"These are the courses related to {name}")

	count = 0
	for course, schools in course_dict.items():
		if name in schools:
			print(course)
			count += 1

	if not count:
		print(f"It seems like {name} is not school we have in the data base :(")
		x = input("Don't fret, would you like to add the school(y/n): ")
		if 'y' ==  x[0].lower():
			addnew(name = name)
	#for "add_course" and "remove_course" action, use return value to pipe to addnew()
	return {"name": name, "course_dict": course_dict} 


def remove_course(name = None, course_dict = {}):
	if not len(course_dict):
		course_dict = extract()
	print("\n")#spacer
	if not name:
		name = process_name(input("What is the name of the instituion: "))

	print("\nPlease choose a course from the list above!")
	print("Enter 'q' when you are finished")
	count = 0
	while((c := input("Course Name: ")) != 'q'):
		if input("Are you sure?(y/n): ").lower()[0] == 'y':
			try:
				course_dict[c].discard(name)
			except:
				print("Please make sure the course name is typed correctly!")
			else:
				print(f"You just removed {course} from {name}'s course list!")
				count += 1

	if count: #don't want to write to file uneceserally
		store(course_dict)


def displayall_schools(course_dict = {}, school_db = {}):
	if not len(course_dict):
		course_dict = extract()
	'''rather not pickle the data related to
	the school_db because this will not be 
	often checked, and pickling more data than
	just course_dict adds another layer of 
	complexity that I don't want to deal with'''
	for course, schools in course_dict.items():
		for school in schools:
			if school not in school_db:
				school_db
	print("\nThese are all the schools you can remove:")
	for school in school_db: print(school)


def remove_school(name = None, course_dict = {}, school_db = set()):
	if not len(course_dict):
		course_dict = extract()
	if not name:
		name = process_name(input("What is the name of the instituion: "))

	'''if using main, school_db will be passed by ref. from main(), therefore
	any modification or addition will be relayed back to main()'''
	if 
	displayall_schools(course_dict = course_dict, school_db = school_db)
	remove = process_name(input("Please choose a school to remove from the list above!"))
	if input(f"Are you sure you want to remove {remove}?(y/n)").lower()[0] == 'y':
		for schools in cour


def displayall(course_dict = {}):
	"display all the courses and the related institutions"
	if not len(course_dict):
		course_dict = extract()
	print("\n")#spacer
	print("These are all the course!")

	for course, schools in course_dict.items():
		print(f"Course: {course}", end = "\t|    ")
		print("Schools: ", end = '')
		for school in schools: print(school, end = '  ')
		print() #new line

def usage(reminder):
	if reminder:
		print("If you want to make another data base with out ")
		print("reseting the current one, you can do it with args!")
		print(f"Usage: {sys.argv[0] <course_fname> <school_fname>")
	sys.exit("Please come again!")

def main():
	"driver code"
	options = [
	"Add new school add its courses", 
	"Check course related to a school",
	"Add course to exisiting school",
	"Remove course from a school",
	"Remove a school from data base",
	"Display all courses and their related schools", 
	"Quit"]
	
	if len(sys.argv) > 2:
		school_fname, course_fname = sys.argv[1:3]
		reminder = False #inform user what they can do with sys args
	else:
		school_fname, course_fname = ("school.data", "course.data")
		reminder = True

	course_db = extract(course_fname) #unpickle course_dict, core to all operations
	school_db = extract(school_fname) #db == data base 

	#no conditional statements!
	functions = [#lambda solves problem of functions not being local to main
	lambda : addnew(course_db), 
	lambda : checkschool(course_db), 
	lambda : addnew(checkschool(course_db)), 
	lambda : remove_course(checkschool(course_db)),
	lambda : remove_school(course_db, school_db), 
	lambda : displayall(course_db), 
	lambda : usage(reminder) 
	]

	while True:
		print("What would you like to do?")
		for i, opt in enumerate(options): print(str(i+1)+'. '+opt)
		x = int(input("Please choose: "))
		functions[x - 1]()	
		print() #new line

	store(course_db, course_fname) #save changes to file
	store(school_db, school_fname)

if __name__ == '__main__':
	main()
