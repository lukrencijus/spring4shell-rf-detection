import requests
import random
import sys
from time import sleep

random_constant = 5000000
base="http://localhost:8080"

def walk_through_courses(i):
    page = i / 5
    requests.get(base+"/")
    requests.post(base+"/save", data = {
        "courseName": f"NewCourse{i}",
        "instructor": f"CourseInstructor{i}",
        "email": f"CourseEmail{i}"
    })
    requests.get(base+"/?sortField=courseName&sortDir=asc")
    requests.get(base+"/add")
    requests.post(base+"/save", data={
        "id": i,
        "courseName": f"NewCourse{random.randrange(1, random_constant)}",
        "instructor": f"CourseInstructor{random.randrange(1, random_constant)}",
        "email": f"CourseEmail{random.randrange(1, random_constant)}"
    })
    requests.get(base+f"/page/{page}?sortField=courseName&sortDir=desc")
    requests.delete(base+f"/delete/+{i}")

def walk_through_sutents(i):
    requests.post(base+"/students/save", data={
        "id": i,
        "fisrtName": f"RandomName{random.randrange(1, random_constant)}",
        "lastName": f"RandomLastName{random.randrange(1, random_constant)}",
        "studentId": f"S11666684486{random.randrange(1, random_constant)}",
        "major": f"SomeVeryInterestingMajor{random.randrange(1, random_constant)}"
    })
    requests.get(base+"/students/")
    requests.get(base+f"/students/update/{i}")
    requests.post(base+"/students/save", data={
        "fisrtName": f"RandomName{random.randrange(1, random_constant)}",
        "lastName": f"RandomLastName{random.randrange(1, random_constant)}",
        "studentId": f"S11666684486{random.randrange(1, random_constant)}",
        "major": f"SomeVeryInterestingMajor{random.randrange(1, random_constant)}"
    })
    delete=int(i/10)
    requests.delete(base+f"/students/delete/{delete}")

def walk_through_instructors(i):
    requests.post(base+"/instructors/save", data={
        "id": i,
        "instructorName": f"VeryNiceName{random.randrange(1, random_constant)}",
        "employeeId": f"S84894{random.randrange(1, random_constant)}",
        "email": f"{random.randrange(1, random_constant)}@mail.co",
        "officeLocation": f"OfficeAt{random.randrange(1, random_constant)}"
    })
    requests.get(base+"/instructors/")
    requests.get(base+f"/instructors/update{i}")
    requests.post(base+"/instructors/save", data={
        "instructorName": f"VeryNiceName{random.randrange(1, random_constant)}",
        "employeeId": f"S84894{random.randrange(1, random_constant)}",
        "email": f"{random.randrange(1, random_constant)}@mail.co",
        "officeLocation": f"OfficeAt{random.randrange(1, random_constant)}"
    })
    delete=int(i/10)
    requests.delete(base+f"/instructors/delete/{i}")

def walk_through_departments(i):
    requests.post(base+"/departments/save", data={
        "id": i,
        "departmentName": f"VeryBuilding{random.randrange(1, random_constant)}",
        "building": f"BuildingAtS84894{random.randrange(1, random_constant)}",
        "email": f"{random.randrange(1, random_constant)}@mail.co",
        "headOfDepartment": f"DepartmentOwner{random.randrange(1, random_constant)}"
    })
    requests.get(base+"/departments/")
    requests.get(base+f"/departments/update{i}")
    requests.post(base+"/departments/save", data={
        "departmentName": f"VeryBuilding{random.randrange(1, random_constant)}",
        "building": f"BuildingAtS84894{random.randrange(1, random_constant)}",
        "email": f"{random.randrange(1, random_constant)}@mail.co",
        "headOfDepartment": f"DepartmentOwner{random.randrange(1, random_constant)}"
    })
    delete=int(i/10)
    requests.delete(base+f"/departments/delete/{delete}")

def invalid_traffic():
    requests.get(base+"/root/incorrect")
    requests.post(base+"/more/incorrect")
    requests.put(base+"/where/am/i")
    requests.delete(base+"/very/interesting")

if len(sys.argv) != 2 or sys.argv[1].isdigit() is False:
    print("Program expects iteration amount to be passed as an argument.")
    print("Usage: python3 simulate_valid_traffic.py <number_of_iterations>")
    sys.exit(0)
else:
    if int(sys.argv[1]) > 0:
        rounds = int(sys.argv[1])
    else:
        print("Negative iterration amount, defaulting to 1")
        rounds = 1
try:
    for i in range(rounds):
        print(f"Loop: {i+1}/{rounds}")
        walk_through_courses(i)
        walk_through_departments(i)
        invalid_traffic()
        walk_through_instructors(i)
        walk_through_sutents(i)
        invalid_traffic()
        sleep(0.2)
except Exception as e:
    print("Something went wrong")
    print(e)