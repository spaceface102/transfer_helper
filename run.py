#!/usr/bin/python3
import sys
import pickle #used to serialize data for later use; store dicts in bytes

def store(data, fname = "course.data"):
	"pickle data and store into fname"
	with open(fname, "wb") as f:
		pickle.dump(data, f)


def extract(fname = "course.data"):
	"unpickle data and return if for use in other funcs"
	try:
		with open(fname, "rb") as f:
			temp = pickle.load(f) 
	except:
		print(f"Initilizing... {fname}\n")
		store(dict())
		return extract()
	else:
		return temp


def process_name(name):
	"make sure that course is easily found in set, even with small variations"
	name = name.replace(' ', '')
	name = name.replace('\t', '')
	name = name.replace('-', '')
	return name.upper()


def addnew(name = None): 
	"add a new school's transfer requirments"
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
	print("Done!")



def checkschool(name = None):
	"print all the courses related with a specific course"
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
		else:
			print("Done!")
	#for "add_course" and "remove_course" action, use return value to pipe to addnew()
	return name 

def displayall():
	"display all the courses and the related institutions"
	course_dict = extract()
	print("\n")#spacer
	print("These are all the course!")

	for course, schools in course_dict.items():
		print(f"Course: {course}", end = "\t|    ")
		print("Schools: ", end = '')
		for school in schools: print(school, end = '  ')
		print() #new line
	print("Done!")





def main():
	print("What would you like to do?")
	options = [
	"Add new school", 
	"Check school",
	"Add course to exisiting school",
	"Remove course from a school",
	"Display all courses", 
	"Remove a school",
	"Quit"]
	#no conditional statements!
	functions = [#lambda solves problem of functions not being local to main
	lambda : addnew(), 
	lambda : checkschool(), 
	lambda : addnew(checkschool()), 
	lambda : addnew(checkschool()),
	lambda : displayall(), 
	lambda : remove_school(), 
	lambda : sys.exit("Please come again!")]			

	while True:
		for i, opt in enumerate(options): print(str(i+1)+'. '+opt)
		x = int(input("Please choose: "))
		functions[x - 1]()	
	

if __name__ == '__main__':
	main()
