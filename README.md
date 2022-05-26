# Test-Case-Prioritization

## File Discription
1. name.txt - contain the information: Name, Email, SID <br />
2. report/CS206_Project_Report.pdf - including experimental results and observations <br />
3. main.py - implement 6 different test suites in each benchmark  <br />
          (coverage criteria: statement/branch + test case prioritization: random/total coverage/additional coverage) <br />
4. fault.py - evaulate the fault-exposing potential of each test suite <br />
  - faults_exposed.csv - collect the results above and save it in a .csv file <br />
5. fault_original - evaulate the fault-exposing potential of original test cases <br />
  - faults_exposed_original.csv - collect the results above and save it in a .csv file <br />

## How to Run the Program
To run the programs (main.py, fault.py and fault_original.py), just type "python3 <program_name>" and it will generate the results <br />

## More Details
- when runnig main.py, it will generate test suites in .txt files named (e.g. random_statement_suite.txt), and it will have the same format as the universe.txt <br />
- when running fault.py, it will collect terminal output with original version and faulty versions, then it will store in .txt files named (e.g. random_statement_suite_original_output.txt,  v1_random_statement_suite_faulty_output.txt) <br />
- all the files generated above will be stored in each benchmark directory <br />
