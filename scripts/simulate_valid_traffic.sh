#!/usr/bin/env bash
set -e
base="http://localhost:8080"
iterations=

walk_through_courses(){
	i=$1
	page=$((i/5))
	curl "$base"/
	curl -d courseName="NewCourse$i" -d instructor="CourseInstructor$i" -d email="CourseEmail$i" "$base"/save
	curl "$base"/"?sortField=courseName&sortDir=asc"
	curl "$base"/add
	curl -d courseName="NewCourse$RANDOM" -d id="$i" -d instructor="CourseInstructor$RANDOM" -d email="CourseEmail$RANDOM" "$base"/save
	curl "$base"/page/"$page""?sortField=courseName&sortDir=desc"
	curl "$base"/delete/"$i"
}

walk_through_students(){
	i=$1
	curl "$base"/students/save -d id="$i" -d firstName="$RANDOM" -d lastName="$RANDOM" -d studentId="S158489$RANDOM" -d major="SomeVeryInterestingMajor$RANDOM"
	curl "$base"/students/
	curl "$base"/students/update/"$i"
	curl "$base"/students/save -d firstName="$RANDOM" -d lastName="$RANDOM" -d studentId="S158489$RANDOM" -d major="SomeVeryInterestingMajor$RANDOM"
	del=$((i/10))
	curl "$base"/studends/delete/"$del"
}

walk_through_departments(){
	i=$1
	curl "$base"/departments/save -d id="$i" -d departmentName="$RANDOM" -d building="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d headOfDepartment="DepartmentOwner$RANDOM"
	curl "$base"/departments/
	curl "$base"/departments/update/"$i"
	curl "$base"/departments/save -d departmentName="$RANDOM" -d building="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d headOfDepartment="DepartmentOwner$RANDOM"
	del=$((i/10))
	curl "$base"/departments/delete/"$del"
}

walk_through_instructors(){
	i=$1
	curl "$base"/instructors/save -d id="$i" -d instructorName="$RANDOM" -d employeeId="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d officeLocation="OfficeAt$RANDOM"
	curl "$base"/instructors/
	curl "$base"/instructors/update/"$i"
	curl "$base"/instructors/save -d instructorName="$RANDOM" -d employeeId="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d officeLocation="OfficeAt$RANDOM"
	del=$((i/10))
	curl "$base"/instructors/delete/"$del"
}

invalid_traffic(){
	curl "$base"/courses
	curl "$base"/courses?not!existing
	curl "$base"/more/non/existing#traffic
}

echo "This script sends iterations of valid traffic to the server."
read -p "Please insert the amount of iterations (digit): " iterations

echo "Running $iterations amount of iterations"
for ((i=1; i<=iterations; i++)) ; do
	echo "Loop: "$i"/"$iterations""
	walk_through_courses "$i" &> /dev/null
	invalid_traffic &> /dev/null
	walk_through_departments "$i" &> /dev/null
	walk_through_instructors "$i" &> /dev/null
	invalid_traffic &> /dev/null
	walk_through_students "$i" &> /dev/null
	sleep 0.2
done

