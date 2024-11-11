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
                # Skip detections containing the phrase "It is used by:"
                if "It is used by:" in detector["description"]:
                    continue

                # Set color based on risk level
                if detector["risk"].lower() == "high":
                    color = "\033[91m"  # Red for high risk
                elif detector["risk"].lower() == "medium":
                    color = "\033[38;2;255;165;0m"  # Orange for medium risk
                else:
                    color = "\033[93m"  # Yellow for low risk or other

                reset_color = "\033[0m"  # Reset color to default


                # Print colored text based on risk level
                print(f"{color}Detection Risk: {detector['risk']}{reset_color}")
                print(f"Description: {detector['description']}")
                print("-" * 40)
        else:
            print("No vulnerabilities detected or error occurred.")
    else:
        print("Failed to retrieve results.")

if __name__ == "__main__":
    main()
