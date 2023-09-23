import argparse
from app import TableMatcher



def main():
    # Command-line arguments parsing
    parser = argparse.ArgumentParser(description="Match and convert table columns.")
    parser.add_argument("--source", required=True, help="Path to the source table.")
    parser.add_argument("--template", required=True, help="Path to the template table.")
    parser.add_argument("--target", required=True, help="Path to save the matched table.")
    parser.add_argument("--api_key", required=True, help="OpenAI API key.")

    args = parser.parse_args()

    # Create an instance of the TableMatcher class
    matcher = TableMatcher(args.template, args.source, args.api_key)

    # Get the matched table using the defined method
    matched_table = matcher.get_matched_table()

    # Save the matched table to the specified target path
    matched_table.to_csv(args.target, index=False)
    print(f"Matched table saved to {args.target}")

if __name__ == "__main__":
    # Entry point of the script
    main()