from test_builder import SqlTestBuilderInteractive
from core import CoreTester

database_url = "sqlite:///chinook.db"


def main():
    print("\033[2J\033[H", end="")
    if input("Do you want to run the test builder? y/n\n") == "y":
        builder = SqlTestBuilderInteractive(database_url)
        builder.create_tests()
    tester = CoreTester(database_url)
    tester.run_tests()
    tester.generate_report()


if __name__ == "__main__":
    main()
