#!/usr/bin/env bash
set -e
base="http://localhost:8080"
iterations=

echo "This script sends iterations of valid traffic to the server."

read -p "Please insert the amount of iterations (digit): " iterations

echo "Running $iterations amount of iterations"
for  ((i=1; i<=iterations; i++)) ; do
	curl "$base"/
	curl -d courseName="NewCourse$i" -d instructor="CourseInstructor$i" -d email="CourseEmail$i" "$base"/save
	curl "$base"/
	sleep 0.5
	curl -d courseName="NewCourse$RANDOM" -d id="$i" -d instructor="CourseInstructor$RANDOM" -d email="CourseEmail$RANDOM" "$base"/save
	curl "$base"/delete/"$i"
	sleep 1
done

