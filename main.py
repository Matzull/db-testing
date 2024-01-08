import argparse
from config import database_url
from test_builder import SqlTestBuilderInteractive
from core import CoreTester


def main():
    # Create argument parser with a detailed description
    parser = argparse.ArgumentParser(
        description="Database Testing Tool - A utility for building, running tests, and generating reports for databases.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Adding arguments
    parser.add_argument(
        "--builder",
        action="store_true",
        help="Run the test builder to create new tests.",
    )
    parser.add_argument(
        "--run_tests",
        action="store_true",
        default=True,
        help="Execute tests against the database.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        default=True,
        help="Generate and display a test report.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for more detailed information.",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Specify an output file for the test report.",
    )
    
    

    # Parse arguments
    args = parser.parse_args()

    # Clear the screen
    print("\033[2J\033[H", end="")

    # Execute the test builder if --builder is specified
    if args.builder:
        print("Running test builder...")
        builder = SqlTestBuilderInteractive(database_url)
        builder.create_tests(gui=True)

    # Create CoreTester instance
    tester = CoreTester(database_url)

    # Execute tests if --run_tests is specified
    if args.run_tests:
        print("Running tests...")
        success = tester.run_tests(verbose=args.verbose)

    # Generate a report if --report is specified
    if args.report:
        print("Generating test report...")
        print("\033[2J\033[H", end="")
        tester.generate_report(verbose=args.verbose, file=args.file)

    if not success:
        raise Exception("Tests failed.")


if __name__ == "__main__":
    main()
