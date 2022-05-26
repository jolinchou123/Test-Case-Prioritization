import os
import gzip
import json
import random

first_time = bool(True)

total_stat = set()
stat_a = set()
stat_b = set()

temp_temp_total_branch = set()
temp_total_branch = set()
total_branch = set()
branch_a = set()
branch_b = set()
temp_temp_branch = 0
temp_branch = 0
branch = 0

stat_test_suite = []
branch_test_suite = []
random_testcase = [] #for Random prioritization

benchmarks = ['printtokens','printtokens2','replace','schedule','schedule2','tcas','totinfo']
#benchmarks = ['printtokens']

#check whether gcc or clang
os.system("gcc-11 --version")
os.chdir("benchmarks")

for benchmark in benchmarks:
	os.chdir(benchmark)

	#run gcov to collect information
	os.system("gcc-11 --coverage " + benchmark + ".c -c")
	os.system("gcc-11 --coverage " + benchmark + ".o")

	#open universe.txt to run test cases
	with open("universe.txt") as f:
		lines = f.readlines()

	##Statement coverage + Random prioritization / Branch coverage + Random prioritization
	for line in lines:
		random_testcase.append(line)

	random.shuffle(random_testcase)

	for testcase in random_testcase:
		file_exists = os.path.exists(benchmark + ".gcda")
		if file_exists == True:
			os.remove(benchmark + ".gcda")
		os.system("./a.out " + testcase)
		os.system("gcov-11 -b -c " + benchmark + ".c -j")

		#unzip file and read the content
		with gzip.open(benchmark + ".gcov.json.gz", "r") as f:
			data = json.loads(f.read())
			for i in data['files']:
				if first_time == True:
					for j in i['lines']:
						total_stat.add(j['line_number'])

						for q in j['branches']:
							branch += 1
							q['num'] = branch
							total_branch.add(q['num'])
						for w in j['branches']:
							if w['count'] > 0:
								branch_a.add(w['num'])

					for k in i['lines']:
						if k['count'] > 0:
							stat_a.add(k['line_number'])
						
					first_time = False
					stat_test_suite.append(testcase)
					branch_test_suite.append(testcase)
				else:
					for x in i['lines']:
						if x['count'] > 0:
							stat_b.add(x['line_number'])
						for y in x['branches']:
							temp_branch += 1
							y['num'] = temp_branch
							temp_total_branch.add(y['num'])
						for z in x['branches']:
							if z['count'] > 0:
								branch_b.add(z['num'])
					if stat_b.difference(stat_a) != set():
						stat_a.update(stat_b - stat_a)
						stat_test_suite.append(testcase)
					stat_b.clear()
					if branch_b.difference(branch_a) != set():
						branch_a.update(branch_b - branch_a)
						branch_test_suite.append(testcase)
					temp_branch = 0
					temp_total_branch.clear()
					branch_b.clear()

		if total_stat == stat_a:
			with open('random_statement_suite.txt', 'w') as f:
				for item in stat_test_suite:
					f.write("%s\n" % item)
					break
		if total_branch == branch_a:
			with open('random_branch_suite.txt', 'w') as f:
				for item in branch_test_suite:
					f.write("%s\n" % item)
					break

	textfile = open("random_statement_suite.txt", "w")
	for item in stat_test_suite:
		textfile.write(item)
	textfile.close()

	textfile = open("random_branch_suite.txt", "w")
	for item in branch_test_suite:
		textfile.write(item)
	textfile.close()

	first_time = True
	total_stat.clear()
	stat_a.clear()
	stat_b.clear()
	temp_total_branch = set()
	total_branch = set()
	branch_a = set()
	branch_b = set()
	temp_branch = 0
	branch = 0
	stat_test_suite.clear()
	branch_test_suite.clear()
	random_testcase.clear()


	##Statement coverage + Total Coverage prioritization / Branch coverage + Total Coverage prioritization
	for line in lines:
		file_exists = os.path.exists(benchmark + ".gcda")
		if file_exists == True:
			os.remove(benchmark + ".gcda")
		os.system("./a.out " + line)
		os.system("gcov-11 -b -c " + benchmark + ".c -j")

		#unzip file and read the content
		with gzip.open(benchmark + ".gcov.json.gz", "r") as f:
			data = json.loads(f.read())
			for i in data['files']:
				if first_time == True:
					for j in i['lines']:
						total_stat.add(j['line_number'])

						for q in j['branches']:
							branch += 1
							q['num'] = branch
							total_branch.add(q['num'])
						for w in j['branches']:
							if w['count'] > 0:
								branch_a.add(w['num'])

					for k in i['lines']:
						if k['count'] > 0:
							stat_a.add(k['line_number'])

					first_time = False
					stat_test_suite.append(line)
					branch_test_suite.append(line)
				else:
					for x in i['lines']:
						if x['count'] > 0:
							stat_b.add(x['line_number'])

						for y in x['branches']:
							temp_branch += 1
							y['num'] = temp_branch
							temp_total_branch.add(y['num'])
						for z in x['branches']:
							if z['count'] > 0:
								branch_b.add(z['num'])

					if stat_b.difference(stat_a) != set():
						stat_a.update(stat_b - stat_a)
						stat_test_suite.append(line)
					stat_b.clear()

					if branch_b.difference(branch_a) != set():
						branch_a.update(branch_b - branch_a)
						branch_test_suite.append(line)
					temp_branch = 0
					temp_total_branch.clear()
					branch_b.clear()

		if total_stat == stat_a:
			with open('total_statement_suite.txt', 'w') as f:
				for item in stat_test_suite:
					f.write("%s\n" % item)
					break
		if total_branch == branch_a:
			with open('total_branch_suite.txt', 'w') as f:
				for item in branch_test_suite:
					f.write("%s\n" % item)
					break

	textfile = open("total_statement_suite.txt", "w")
	for item in stat_test_suite:
		textfile.write(item)
	textfile.close()

	textfile = open("total_branch_suite.txt", "w")
	for item in branch_test_suite:
		textfile.write(item)
	textfile.close()

	first_time = True
	total_stat.clear()
	stat_a.clear()
	stat_b.clear()
	temp_total_branch = set()
	total_branch = set()
	branch_a = set()
	branch_b = set()
	temp_branch = 0
	branch = 0
	stat_test_suite.clear()
	branch_test_suite.clear()
	random_testcase.clear()


	##Statement coverage + Additional Coverage prioritization / Branch coverage + Additional Coverage prioritization
	#(i) select a test case that yields the greatest additional statement/branch coverage
	for line in lines:
		file_exists = os.path.exists(benchmark + ".gcda")
		if file_exists == True:
			os.remove(benchmark + ".gcda")
		os.system("./a.out " + line)
		os.system("gcov-11 -b -c " + benchmark + ".c -j")
		
		#unzip file and read the content
		with gzip.open(benchmark + ".gcov.json.gz", "r") as f:
			data = json.loads(f.read())
			for i in data['files']:
				if first_time == True:
					for j in i['lines']:
						total_stat.add(j['line_number'])

						for q in j['branches']:
							branch += 1
							q['num'] = branch
							total_branch.add(q['num'])
						for w in j['branches']:
							if w['count'] > 0:
								branch_a.add(w['num'])

					for k in i['lines']:
						if k['count'] > 0:
							stat_a.add(k['line_number'])
					first_time = False
					stat_test_suite.append(line)
					branch_test_suite.append(line)
				else:
					for x in i['lines']:
						if x['count'] > 0:
							stat_b.add(x['line_number'])

						for y in x['branches']:
							temp_branch += 1
							y['num'] = temp_branch
							temp_total_branch.add(y['num'])
						for z in x['branches']:
							if z['count'] > 0:
								branch_b.add(z['num'])

					if len(stat_b) > len(stat_a):
						stat_a.clear()
						stat_a.update(stat_b)
						stat_test_suite.clear()
						stat_test_suite.append(line)
					stat_b.clear()
					
					if len(branch_b) > len(branch_a):
						branch_a.clear()
						branch_a.update(branch_b)
						branch_test_suite.clear()
						branch_test_suite.append(line)
					temp_branch = 0
					temp_total_branch.clear()
					branch_b.clear()

	#(ii) then adjust the coverage information on subsequent test cases to indicate their coverage of statements/branches not yet covered by a test already chosen for the suite
	for line in lines:
		file_exists = os.path.exists(benchmark + ".gcda")
		if file_exists == True:
			os.remove(benchmark + ".gcda")
		os.system("./a.out " + line)
		os.system("gcov-11 -b -c " + benchmark + ".c -j")

		#unzip file and read the content
		with gzip.open(benchmark + ".gcov.json.gz", "r") as f:
			data = json.loads(f.read())
			for a in data['files']:
				for b in a['lines']:
					if b['count'] > 0:
						stat_b.add(b['line_number'])

					for c in b['branches']:
						temp_temp_branch += 1
						c['num'] = temp_temp_branch
						temp_temp_total_branch.add(c['num'])
					for d in b['branches']:
						if d['count'] > 0:
							branch_b.add(d['num'])


				if stat_b.difference(stat_a) != set():
					stat_a.update(stat_b - stat_a)
					stat_test_suite.append(line)
				stat_b.clear()
					
				if branch_b.difference(branch_a) != set():
					branch_a.update(branch_b - branch_a)
					branch_test_suite.append(line)
			temp_temp_branch = 0
			temp_temp_total_branch.clear()
			branch_b.clear()
		
		if total_stat == stat_a:
			with open('addition_statement_suite.txt', 'w') as f:
				for item in stat_test_suite:
					f.write("%s\n" % item)
					break

		if total_branch == branch_a:
			with open('addition_branch_suite.txt', 'w') as f:
				for item in branch_test_suite:
					f.write("%s\n" % item)
					break

	textfile = open("addition_statement_suite.txt", "w")
	for item in stat_test_suite:
		textfile.write(item)
	textfile.close()

	textfile = open("addition_branch_suite.txt", "w")
	for item in branch_test_suite:
		textfile.write(item)
	textfile.close()

	first_time = True
	total_stat.clear()
	stat_a.clear()
	stat_b.clear()
	temp_temp_total_branch.clear()
	temp_total_branch.clear()
	total_branch.clear()
	branch_a.clear()
	branch_b.clear()
	temp_temp_branch = 0
	temp_branch = 0
	branch = 0
	stat_test_suite.clear()
	branch_test_suite.clear()
	random_testcase.clear()

	os.chdir("..")

