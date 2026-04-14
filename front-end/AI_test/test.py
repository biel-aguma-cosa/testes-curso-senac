import argparse
import sys

def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Example script that accepts command-line arguments."
    )

    # Add arguments
    parser.add_argument(
        "name",  # positional argument
        type=str,
        help="Your name"
    )
    parser.add_argument(
        "age",  # positional argument
        type=int,
        help="Your age"
    )
    parser.add_argument(
        "-v", "--verbose",  # optional argument
        action="store_true",
        help="Enable verbose output"
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate age
    if args.age < 0:
        print("Error: Age cannot be negative.", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.verbose:
        print(f"Verbose mode ON: Received name='{args.name}', age={args.age}")
    else:
        print(f"Hello {args.name}, you are {args.age} years old.")

if __name__ == "__main__":
    main()
