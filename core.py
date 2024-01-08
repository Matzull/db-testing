import os
from db_connection import Connection
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class CoreTester:
    def __init__(self, db_url):
        self.connection = Connection(db_url)
        self.test_queries = {}
        self.load_queries_from_dir("tests")
        self.test_results = {}

    def load_queries_from_dir(self, directory):
        for table in os.listdir(directory):
            table_path = os.path.join(directory, table)
            if os.path.isdir(table_path):
                self.test_queries[table] = []
                for file in os.listdir(table_path):
                    if file.endswith(".sql"):
                        with open(os.path.join(table_path, file), "r") as f:
                            query = f.read().strip()
                            self.test_queries[table].append(query)

    def print_test_queries(self):
        for table, queries in self.test_queries.items():
            print(f"Table: {table}")
            for query in queries:
                print(query)
            print("")

    def run_tests(self, verbose=False):
        all_passed = True
        for table, queries in tqdm(self.test_queries.items()):
            self.test_results[table] = []
            for query in queries:
                if verbose:
                    print(f"Running test for {table}: {query}")
                formatted_query = query.format(table=table)
                try:
                    exception = False
                    result = self.connection.execute_query(formatted_query)
                except Exception as e:
                    result = e
                    exception = True
                if result:
                    # Test failed if result is not empty
                    self.test_results[table].append(
                        (formatted_query, "Failed", result, exception)
                    )
                    all_passed = False
                else:
                    # Test passed if result is empty
                    self.test_results[table].append((formatted_query, "Passed", [], 0))
        return all_passed
    

    def generate_report(self, file=None, verbose=False):
        if file is None:
            RED = "\033[91m"
            GREEN = "\033[92m"
            RESET = "\033[0m"
            BOLD = "\033[1m"
        else:
            RED = ""
            GREEN = ""
            RESET = ""
            BOLD = ""

        report_lines = []
        total_passed = 0
        total_failed = 0
        for table, results in self.test_results.items():
            table_report = []
            passed = sum(1 for _, status, _, _ in results if status == "Passed")
            total_passed += passed
            failed = sum(1 for _, status, _, _ in results if status == "Failed")
            total_failed += failed
            table_report.append(f"{BOLD}Report for table: {table}{RESET}")
            table_report.append(
                f"Tests Passed: {GREEN}{passed}{RESET}, Tests Failed: {RED}{failed}{RESET}"
            )
            if verbose:
                for query, status, data, _ in results:
                    color = GREEN if status == "Passed" else RED
                    test_number = query.split(" ")[2]
                    query = query.split("\n")[1]
                    
                    if data:
                        table_report.append(
                            f'Test {test_number}{RESET}: "{query} {RED}{status}"\n{RESET}'
                        )
                        table_report.append(f"Data: {data}")
                    else:
                        table_report.append(
                        f'Test Query: {test_number}\nQuery: "{query}"\nStatus: {color}{status}{RESET}'
                    )
                    table_report.append("")
            else:
                for query, status, data, ex in results:
                    if status == "Failed":
                        test_number = query.split(" ")[2]
                        failed_query = query.split("\n")[1]
                        table_report.append(
                            f'Test {test_number}{RESET}: "{failed_query}" {RED}{status}\n{RESET}'
                        )
                        if data and ex:
                            table_report.append(f"Data: {data}")
            if failed:
                report_lines.extend(table_report)
            else:
                tmp = report_lines
                report_lines = table_report
                report_lines.extend(tmp)
                
        report_lines.append(
                f"{BOLD}Total tests runned: {total_failed + total_passed} Total tests Passed: {GREEN}{total_passed}{RESET}{BOLD}, Total tests Failed: {RED}{total_failed}{RESET}"
            )
        report = "\n".join(report_lines)
        if file is not None:
            with open(f"{file}.txt", "w") as file:
                file.write(report)
        else:
            print("\n----------------------- Test Report -----------------------\n\n")
            print(report)
            print("\n-----------------------------------------------------------\n\n")