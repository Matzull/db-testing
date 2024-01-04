import os
from db_connection import Connection
from tqdm import tqdm


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

    def run_tests(self):
        for table, queries in tqdm(self.test_queries.items()):
            self.test_results[table] = []
            for query in queries:
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
                else:
                    # Test passed if result is empty
                    self.test_results[table].append((formatted_query, "Passed", [], 0))

    def generate_report(self, to_file=False, verbose=False):
        RED = "\033[91m"
        GREEN = "\033[92m"
        RESET = "\033[0m"
        BOLD = "\033[1m"

        report_lines = []
        for table, results in self.test_results.items():
            passed = sum(1 for _, status, _, _ in results if status == "Passed")
            failed = sum(1 for _, status, _, _ in results if status == "Failed")
            report_lines.append(f"{BOLD}Report for table: {table}{RESET}")
            report_lines.append(
                f"Tests Passed: {GREEN}{passed}{RESET}, Tests Failed: {RED}{failed}{RESET}"
            )
            if verbose:
                for query, status, data, _ in results:
                    color = GREEN if status == "Passed" else RED
                    report_lines.append(
                        f"Test Query: {query}\nStatus: {color}{status}{RESET}"
                    )
                    if data:
                        report_lines.append(f"Data: {data}")
                    report_lines.append("")
            else:
                for query, status, data, ex in results:
                    if status == "Failed":
                        test_number = query.split(" ")[2]
                        failed_query = query.split("\n")[1]
                        report_lines.append(
                            f'Failed test {test_number}\nQuery: "{failed_query}"\nStatus: {RED}{status}{RESET}'
                        )
                        if data and ex:
                            report_lines.append(f"Data: {data}")

        report = "\n".join(report_lines)
        if to_file:
            with open("test_report.txt", "w") as file:
                file.write(report)
        else:
            print(
                "\n\n\n----------------------- Test Report -----------------------\n\n"
            )
            print(report)
