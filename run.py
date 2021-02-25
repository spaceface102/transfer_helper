#!/usr/bin/python3
import sys
import pickle #used to serialize data for later use; store dicts in bytes

def store(data, fname, relative = "./data/"): #changes the path from curr dir
	"pickle data and store into fname"
	with open(relative+fname, "wb") as f:
		pickle.dump(data, f)


def extract(fname, relative = "./data/"):
	"unpickle data and return if for use in other funcs"
	try:
		with open(relative+fname, "rb") as f:
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
	name = name.replace('_', '')
	return name.upper()


def display_name(name):
	"Make the course look prettier when outputing"
	'''capatilized since proccess_name() will have touched 
	'name' before hand, therefore making upper case.
	have to add this manually to have more prefixes '''
	prefix = ["CS", "CIS"] 
	for pre in prefix:
		name_pre = name[:len(pre)]
		if name_pre.find(pre) >= 0:
			return pre + ' ' + name[len(pre):]


def addnew(course_dict, school_db, name = None): 
	"add a new school's transfer requirments"
	print("\n")#spacer
	if not name:
		name = process_name(input("What is the name of the instituion: "))
	print("Please input the courses related with this institution")
	print("Enter 'q' when you are finished")
	print("NOTE: If you made a mistake on the course name, USE: 'b'!")	

	#at this point, school_db should already be a dict() (configured in main)
	if name not in school_db:
		#use set to ensure no duplicates and fast searching
		school_db[name] = set()

	prev_courses = list()
	rem_courses = set() #removed courses
	count = 1
	while((c := input("%d: " %(count))) != 'q'):
		if c == 'b' and input("Are you sure?(y/n): ").lower()[0] == 'y':
			if len(prev_courses):	
				#use sets to avoid duplicates!
				rem_courses.add(prev_courses[-1])
				c = prev_courses.pop() #remove to not repeate and go on to the next course
				print("Removed %s from %s's course list!" %(c, name)) 
			else:	
				print("You don't have any courses left to remove!")
			continue

		c = process_name(c)
		if c in course_dict:
			course_dict[c].add(name)
		else:
			prev_courses.append(c)
			course_dict[c] = {name} #init as set to ensure no repeats
		school_db[name].add(c)
		count += 1

	cleanup(course_dict, school_db, name, rem_courses)


def addcourse(course_dict, school_db):
	names = set(school_db.keys())
	name = checkschool(course_dict, school_db)
	if name in names:
		'''case where try to add course even though there is no course yet!
		Have to do this bc checkschool will use addnew() func if course
		does not exist. This avoids a repeat call to addnew()'''
		addnew(course_dict, school_db, name = name)

def checkschool(course_dict, school_db):
	"print all the courses related with a specific course"
	print("\n")#spacer
	print("Please choose a school:")
	displayall_schools(school_db)	
	name = process_name(input("School: "))
	print(f"These are the courses related to {name}:")

	if name in school_db:
		for course in school_db[name]:
			print(display_name(course))
	else:	
		print(f"It seems like {name} is not a school we have on file :(")
		x = input("Don't fret, would you like to add the school(y/n): ")
		if 'y' ==  x[0].lower():
			addnew(course_dict, school_db, name = name)
	return name 


def cleanup(course_dict, school_db, school_name, courses):
	"If remove any course data, have to do clean up!"
	for course in courses:
		course_dict[course].discard(school_name)
		school_db[school_name].discard(course)
		if not len(course_dict[course]): #course has no schools, throw that shit out
			course_dict.pop(course)
	if not len(school_db[school_name]): #school has no courses, throw that shit out
		school_db.pop(school_name)


def remove_course(course_dict, school_db, name = None):
	"remove school name from the set related to key==course in course_dict"
	print("\n")#spacer
	displayall_schools(school_db)
	name = checkschool(course_dict, school_db) 
	print("\nPlease choose a course to remove from the list above!")
	print("Enter 'q' when you are done removing courses")

	rem_courses = set()
	while((c := input("Course Name: ")) != 'q'):
		if input("Are you sure?(y/n): ").lower()[0] == 'y':
			c = proccess_name(c)
			if c in rem_courses: #not necessary, but nice for user
				print(f"You have already removed {c}!!!")
				continue
			elif c in course_dict:
				rem_courses.add(c)
				print(f"You just removed {c} from {name}'s course list!")
				continue
			else:
				print("Please make sure the course name is typed correctly!")
				continue

	cleanup(course_dict, school_db, name, rem_courses)


def remove_school(course_dict, school_db, name = None):
	"remove school from each set related with the course in course_dict"
	print("\n")#spacer
	print("These are the schools that you have in the database:")
	displayall_schools(school_db)
	if not name:
		name = process_name(input("\nWhich school do you wish to COMPLETLY remove: "))
	
	if input("Are you sure?(y/n): ").lower()[0] == 'y':
		if name in school_db:
			cleanup(course_dict, school_db, name, school_db[name])
		else:
			print("Please make sure to choose from the schools above!!!")
			print("Done")


def displayall_schools(school_db):
	"displays all the schools with the school_db dictionary"
	for school in school_db.keys():
		print(school)


def displayall(course_dict):
	"displayall the courses and their related schools."
	print("\n")#spacer
	print("These are all the course!")

	for course, schools in course_dict.items():
		print(f"Course: {display_name(course)}", end = "\t|    ")
		print("Schools: ", end = '')
		for school in schools: print(school, end = '  ')
		print() #new line


def quit(reminder, course_db, course_fname, school_db, school_fname):
	"quits and reminds user they can change data bases"
	if reminder:
		print("\n\nIf you want to make another data base with out ")
		print("reseting the current one, you can do it with args!")
		print(f"Usage: {sys.argv[0]} <course_fname> <school_fname>")
	print("Please come again!")
	store(course_db, course_fname) #save changes to file
	store(school_db, school_fname)
	exit()


def main():
	"driver code"
	if len(sys.argv) > 2:
		course_fname, school_fname = sys.argv[1:3]
		reminder = False 
	else:
		#defualts!
		course_fname, school_fname = ("course.data", "school.data")
		reminder = True #inform user can make new data base 

	course_db = extract(course_fname) #unpickle course_dict, core to all operations
	school_db = extract(school_fname) #db == data base 

	options = [
	"Add new school add its courses", 
	"Check course related to a school",
	"Add course to exisiting school",
	"Remove course from a school",
	"Remove a school from data base",
	"Display all courses and their related schools", 
	"Quit"]
	
	#no conditional statements!
	functions = [#lambda solves problem of functions not being local to main
	lambda : addnew(course_db, school_db), 
	lambda : checkschool(course_db, school_db), 
	lambda : addcourse(course_db, school_db), 
	lambda : remove_course(course_db, school_db),
	lambda : remove_school(course_db, school_db), 
	lambda : displayall(course_db), 
	lambda : quit(reminder, course_db, course_fname, school_db, school_fname) 
	]

	num_funcs = len(functions)
	while True:
		print("What would you like to do?")
		for i, opt in enumerate(options): print(str(i+1)+'. '+opt)
		x = input("Please choose: ")
		if x.isnumeric() and (x := int(x)) >= 1 and x <= num_funcs:
			functions[int(x) - 1]()	
		else:
			print(f"Please choose one of the options!(1-{len(functions)})\n")
		print() #new line
#EOMain


if __name__ == '__main__':
	main()
