import sys
import argparse
from .web_server import run_server

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='CLI2Web - Web interface for command line tools')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the web server on')
    parser.add_argument('--host', type=str, default='localhost', help='Host to run the web server on')
    parser.add_argument('command', help='Command to run')
    parser.add_argument('args', nargs='*', help='Command arguments')

    # Parse known args to handle our flags, leaving the rest for the command
    args, unknown = parser.parse_known_args()
    
    # Combine command and its args
    command = args.command
    if args.args:
        command = f"{command} {' '.join(args.args)}"
    if unknown:
        command = f"{command} {' '.join(unknown)}"

    # Run server with specified port
    run_server(
        host=args.host,
        port=args.port,
        cmd_name=command
    )

if __name__ == "__main__":
    main() 