#!/usr/bin/env bash
set -e
base="http://localhost:8080"
iterations=

walk_through_courses(){
	agent=$1
	i=$2
	page=$((i/5))
	curl -A "$agent" "$base"/
	curl -A "$agent" -d courseName="NewCourse$i" -d instructor="CourseInstructor$i" -d email="CourseEmail$i" "$base"/save
	curl -A "$agent" "$base"/"?sortField=courseName&sortDir=asc"
	curl -A "$agent" "$base"/add
	curl -A "$agent" -d courseName="NewCourse$RANDOM" -d id="$i" -d instructor="CourseInstructor$RANDOM" -d email="CourseEmail$RANDOM" "$base"/save
	curl -A "$agent" "$base"/page/"$page""?sortField=courseName&sortDir=desc"
	curl -A "$agent" "$base"/delete/"$i"
}

walk_through_students(){
	agent=$1
	i=$2
	curl -A "$agent" "$base"/students/save -d id="$i" -d firstName="$RANDOM" -d lastName="$RANDOM" -d studentId="S158489$RANDOM" -d major="SomeVeryInterestingMajor$RANDOM"
	curl -A "$agent" "$base"/students/
	curl -A "$agent" "$base"/students/update/"$i"
	curl -A "$agent" "$base"/students/save -d firstName="$RANDOM" -d lastName="$RANDOM" -d studentId="S158489$RANDOM" -d major="SomeVeryInterestingMajor$RANDOM"
	del=$((i/10))
	curl -A "$agent" "$base"/studends/delete/"$del"
}

walk_through_departments(){
	agent=$1
	i=$2
	curl -A "$agent" "$base"/departments/save -d id="$i" -d departmentName="$RANDOM" -d building="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d headOfDepartment="DepartmentOwner$RANDOM"
	curl -A "$agent" "$base"/departments/
	curl -A "$agent" "$base"/departments/update/"$i"
	curl -A "$agent" "$base"/departments/save -d departmentName="$RANDOM" -d building="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d headOfDepartment="DepartmentOwner$RANDOM"
	del=$((i/10))
	curl -A "$agent" "$base"/departments/delete/"$del"
}

walk_through_instructors(){
	agent=$1
	i=$2
	curl -A "$agent" "$base"/instructors/save -d id="$i" -d instructorName="$RANDOM" -d employeeId="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d officeLocation="OfficeAt$RANDOM"
	curl -A "$agent" "$base"/instructors/
	curl -A "$agent" "$base"/instructors/update/"$i"
	curl -A "$agent" "$base"/instructors/save -d instructorName="$RANDOM" -d employeeId="BuildingAt$RANDOM" -d email="$RANDOM@mail" -d officeLocation="OfficeAt$RANDOM"
	del=$((i/10))
	curl -A "$agent" "$base"/instructors/delete/"$del"
}

invalid_traffic(){
	agent=$1
	curl -A "$agent" "$base"/courses
	curl -A "$agent" "$base"/courses?not!existing
	curl -A "$agent" "$base"/more/non/existing#traffic
}

echo "This script sends iterations of valid traffic to the server."

read -p "Please insert the amount of iterations (digit): " iterations

echo "Running $iterations amount of iterations"
user_agents=(
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3"
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
	"Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
	"PostmanRuntime/7.41.0"
	"python-requests/2.32.3"
)
for ((i=1; i<=iterations; i++)) ; do
	echo "Loop: "$i"/"$iterations""
	agent="${user_agents[$(( RANDOM % ${#user_agents[@]} ))]}"
	walk_through_courses "$agent" "$i" &> /dev/null
	invalid_traffic "$agent" &> /dev/null
	walk_through_departments "$agent" "$i" &> /dev/null
	walk_through_instructors "$agent" "$i" &> /dev/null
	invalid_traffic "$agent" &> /dev/null
	walk_through_students "$agent" "$i" &> /dev/null
	sleep 0.2
done

