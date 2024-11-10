import sys
import os

details = {
    'version': '0.1.0
}

if sys.argv[1] == '-V':
    print(f"You currently have eouTools version {details['version']}")
    sys.exit(0)
elif sys.argv[1] == '--install-requirements':
    print("This operation will install all requirements. Are you sure you wish to proceed?")
    choice = input("(y/n) ")
    if choice[0].lower() != 'y':
        sys.exit(0)
    os.system("python -m pip install --upgrade numpy<=1.26.4 Deprecated")
elif sys.argv[1] == '--upgrade':
    print("This operation will require re-installation of eouTools. Are you sure you wish to proceed?")
    choice = input("(y/n) ")
    if choice[0].lower() != 'y':
        sys.exit(0)
    os.system("python -m pip install --upgrade eouTools")
else:
    print(f"{sys.argv[1]} is not a valid command!", file = sys.stderr)
    sys.exit(9009)
