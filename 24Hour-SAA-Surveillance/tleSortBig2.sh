#take each satellite, one by one, three lines at a time.

#put it in the workspace. If it has an inclination in the range, write it to the
#list and clear the workspace.

#!/bin/bash
echo "Jacob Showman 2025"
#We'll need these to filter candidates based on inclination and sm-mj axis
declare inc=0			#inclination, degrees
cp data2 data
rm workspace
rm list

while read line ;
do
	inc=$(sed '3!d' data | cut -d' ' -f3 | bc)
	inc=$(bc <<< "$inc/1")
	head -1 data
	if [[(($inc -le 40)) && (($inc -ge 15))]]
	then
		head -1 data >> list
	fi
	sed -i '1,3d' data
done < data
