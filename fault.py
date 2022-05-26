import os
import subprocess as sp
import filecmp
import csv

test_cases = []
original_output = []
faulty_output = []
fault_exposed = 0

test_suites = ["random_statement_suite", "total_statement_suite", "addition_statement_suite", "random_branch_suite", "total_branch_suite", "addition_branch_suite"]
benchmarks = ['printtokens','schedule','schedule2','tcas','totinfo']
#test_suites = ["random_statement_suite"]
#benchmarks = ['printtokens2', 'replace']
versions = []

store = []

fault_info = ['benchmark', 'test_suite', 'fault_exposed']

os.chdir("benchmarks")

for benchmark in benchmarks:
	os.chdir(benchmark)

	versions.clear()

	#get number of faulty versions
	for file in os.listdir(os.getcwd()):
		if file.startswith("v"):
			versions.append(file)
			versions.sort()

	for test_suite in test_suites:

		os.system("gcc-11 -Wno-return-type -g -o " + benchmark + " " + benchmark + ".c")

		original = os.getcwd()		
		#open universe.txt to run test cases
		with open(test_suite + ".txt") as f:
			lines = f.readlines()
		
		for line in lines:
			test_cases.append(line)

		#save the original output to a .txt file
		for test_case in test_cases:
			output = sp.getoutput("./" + benchmark + " " + test_case)
			original_output.append(output)

		with open(test_suite + '_original_output.txt', 'w') as f:
			for item in original_output:
				f.write("%s\n" % item)

		for version in versions:
	
			#compile faulty versions' files
			os.chdir(version)
			os.system("gcc-11 -Wno-return-type -g -o " + benchmark + " " + benchmark + ".c")

			#save the faulty output to a .txt file
			for test_case in test_cases:
				os.chdir("..")
				output = sp.getoutput("./" + version + "/" + benchmark + " " + test_case)
				faulty_output.append(output)
				os.chdir(version)
		
			with open(version + "_" + test_suite + '_faulty_output.txt', 'w') as f:
				for item in faulty_output:
					f.write("%s\n" % item)

			os.chdir("..")
			faulty_output.clear()

			#compare between original and faulty versions
			path = os.getcwd()

			f1 = path + "/" + test_suite + "_original_output.txt"
			f2 = path + "/" + version + "/" + version + "_" + test_suite + "_faulty_output.txt"
			result = filecmp.cmp(f1, f2)
			if result == False:
				fault_exposed += 1

		store.append({'benchmark': benchmark, 'test_suite': test_suite, 'fault_exposed': fault_exposed})
		fault_exposed = 0

		test_cases.clear()
		original_output.clear()

	os.chdir("..")

print(store)
#save the information of faults exposed to .csv file
os.chdir("..")
with open('faults_exposed.csv', 'w') as csvfile:
    i = csv.DictWriter(csvfile, fieldnames = fault_info)
    i.writeheader()
    i.writerows(store)
