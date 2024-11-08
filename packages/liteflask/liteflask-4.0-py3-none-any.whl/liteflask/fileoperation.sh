#!/bin/bash
mkdir ~/project_files

touch ~/project_files/notes.txt ~/project_files/tasks.txt ~/project_files/summary.txt

echo "This is a test file" >> ~/project_files/notes.txt
echo "This is a test file" >> ~/project_files/tasks.txt
echo "This is a test file" >> ~/project_files/summary.txt

ls ~/project_files > ~/project_files/file_list.txt
