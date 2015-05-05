
for file in "instances/*" do
	if [[-f $file ]]; then
		python validator.py $file
	fi
