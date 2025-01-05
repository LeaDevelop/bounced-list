"""
MIT License

Copyright (c) 2025 LeaDevelop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os # OS interface, used for checking directory existence.
import glob # For global pattern matching, used for finding all *.eml files.
import sys # System specific parameters and functions, used for error handling sys.exit(1).
import re # Regular expression, used for extracting email addresses.

# Constants
DIRECTORY = r'C:\projects\dev\bouncedList\bounced-files' # TODO specify directory where you got all the bounced .eml files & update .gitignore.
EXCLUDED_EMAILS = ['noreply@example.com', 'test@example.com'] # TODO remove examples & replace with your no-reply email address.
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
OUTPUT_FILE = 'bounced-list.txt' # TODO specify file name where you want all unique bounced email addresses & update .gitignore.

def extract_email_recipients():
    # Check if directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' does not exist!")
        sys.exit(1)

    # Read all .eml files in the specified directory
    eml_files = glob.glob(os.path.join(DIRECTORY, '*.eml'))

    # Check if any .eml files exist
    if not eml_files:
        print(f"Error: No .eml files found in '{DIRECTORY}'")
        sys.exit(1)

    recipients = []

    # Process each .eml file
    for file_path in eml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Search for Delivered-To: and Original-Recipient: lines
                for line in content.split('\n'):
                    if line.startswith('Final-Recipient:'):
                        # Extract email using regex pattern
                        found_emails = re.findall(EMAIL_PATTERN, line)

                        for email in found_emails:
                            # Only add email if it's not in the excluded list
                            if email.lower() not in [e.lower() for e in EXCLUDED_EMAILS]:
                                recipients.append(email)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Remove duplicates while preserving order
    recipients = list(dict.fromkeys(recipients))

    # Write recipients to a .txt file
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
            for recipient in recipients:
                output_file.write(recipient + '\n')
        print(f"Successfully extracted {len(recipients)} unique recipients to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing to {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    extract_email_recipients()
