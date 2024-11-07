import os
import argparse
from . import generate_script


def init():
    secret_key = input("Enter your OpenAi API Key: ")
    config_dir = os.path.expanduser("~/.tsg")
    config_file = os.path.join(config_dir, "config")
    os.makedirs(config_dir, exist_ok=True)
    with open(config_file, "w") as f:
        f.write(secret_key)
    print("Config file created at: ", config_file)


def generate(branch):
    config_file = os.path.expanduser("~/.tsg/config")

    # Check if the config file exists
    if not os.path.isfile(config_file):
        print("Config file not found. Please run 'tsg init' first.")
        return

    # Read the secret key
    with open(config_file, "r") as f:
        secret_key = f.read().strip()

    generate_script.main(secret_key, branch)


def main():
    parser = argparse.ArgumentParser(
        prog='tsg', description='Kenny\'s Test Helper CLI Tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Init command
    parser_init = subparsers.add_parser(
        'init', help='Initialize with your secret key')

    # Generate command
    # Generate command
    parser_generate = subparsers.add_parser('generate', help='Generate output')
    parser_generate.add_argument(
        '-b', '--branch',
        type=str,
        default='master',  # Default branch is 'master'
        help='Target branch to compare with (default: master)'
    )

    args = parser.parse_args()

    if args.command == 'init':
        init()
    elif args.command == 'generate':
        generate(args.branch)


if __name__ == '__main__':
    main()
