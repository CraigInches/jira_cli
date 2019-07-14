''' Main functions for jira_cli app '''
import os
import argparse
from .conf import Config, gen_config, get_file
from .jira import fetch_issue


def main():
    '''Core Functions'''
    instance = os.getenv('JIRA_PROFILE_NAME', default='JIRA')
    parser = argparse.ArgumentParser(description="CLI to JIRA")
    commands_parser = parser.add_subparsers(title="Available Commands", dest='command')
    issue_parser = commands_parser.add_parser("issue")
    issue_parser.add_argument("issue_id", help="Issue identifier")
    search_parser = commands_parser.add_parser("search")
    search_parser.add_argument("search_term", help="Search Term")
    args = parser.parse_args()
    if os.path.exists(get_file()):
        if args.command == "issue":
            print("issue is: " + args.issue_id)
            fetch_issue(args.issue_id, instance)
        elif args.command == "search":
            print("you searched for: " + args.search_term)
    else:
        print("Config File does not exist")
        print("do you want to create a template ~/.config/jira_cli")
        answer = input("Y/N")
        if answer.upper() == "Y":
            print("You Accepted")
            print("Enter a name for your instance")
            instance_name = input()
            gen_config(instance_name)
            print("Please edit " + get_file() + "as needed")
        else:
            print("Goodbye!")

if __name__ == '__main__.py':
    main()
