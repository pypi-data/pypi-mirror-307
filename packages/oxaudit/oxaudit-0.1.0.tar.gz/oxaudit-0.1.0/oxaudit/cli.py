import argparse
from .scan import scan_contract

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scan a Solidity contract using Oxaudit.")
    parser.add_argument("contract", help="Path to the Solidity contract file to scan.")
    args = parser.parse_args()

    # Run the scan and get the result
    result = scan_contract(args.contract)

    # If there are results, print them
    if result:
        print("Oxaudit Results:")
        if 'status' in result and result['status'] == "success":
            for detector in result.get('vulnerabilities', []):
                for issue in detector:
                    print(f"Description: {issue['description']}")
                    print(f"Location: {issue['location']}")
                    print("-" * 40)
        else:
            print("No vulnerabilities detected or error occurred.")
    else:
        print("Failed to retrieve results.")

if __name__ == "__main__":
    main()
