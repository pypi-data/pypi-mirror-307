#!/usr/bin/env python3

import sys
import argparse
import os
from pathlib import Path
from langgraph_codegen.gen_graph import gen_graph, gen_nodes, gen_state,gen_conditions, validate_graph
from colorama import init, Fore, Style
from rich import print as rprint
from rich.syntax import Syntax

# Initialize colorama (needed for Windows)
init()


def print_python_code(code_string, show_line_numbers=False):
    """
    Print Python code with syntax highlighting to the terminal
    
    Args:
        code_string (str): The Python code to print
        show_line_numbers (bool): Whether to show line numbers in the output
    """
    # Create a Syntax object with Python lexer
    syntax = Syntax(code_string, "python", theme="monokai", line_numbers=show_line_numbers)
    
    # Print the highlighted code
    rprint(syntax)

def get_example_path(filename):
    """Get the full path to an example file."""
    try:
        # Get the package directory
        import langgraph_codegen
        package_dir = Path(os.path.dirname(langgraph_codegen.__file__))
        if '.' not in filename:
            filename = filename + '.graph'
        example_path = package_dir / 'data' / 'examples' / filename
        
        if example_path.exists():
            return str(example_path)
        return None
    except Exception as e:
        print(f"Error finding example: {str(e)}", file=sys.stderr)
        return None

def list_examples():
    """List all available example graph files."""
    print(f"\n{Fore.LIGHTBLACK_EX}Example graphs (these are text files):{Style.RESET_ALL}\n")
    
    examples = get_available_examples()
    if not examples:
        print(f"{Fore.YELLOW}No examples found{Style.RESET_ALL}")
        return
        
    for example in sorted(examples):
        name = example.split('/')[-1]  # Get just the filename
        print(f" {Fore.BLUE}{name}{Style.RESET_ALL}")
    
    print(f"\n{Fore.LIGHTBLACK_EX}View a graph with: {Fore.BLUE}lgcodegen <graph_name>{Style.RESET_ALL}\n")

def show_example_content(example_name):
    """Show the content of an example graph file."""
    example_path = get_example_path(example_name)
    if not example_path:
        print(f"{Fore.RED}Error: Example '{example_name}' not found{Style.RESET_ALL}", file=sys.stderr)
        print(f"{Fore.YELLOW}Use --list-examples to see available examples{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(example_path, 'r') as f:
            content = f.read()
        print(f"{Fore.BLUE}{content}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading example: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

def get_available_examples():
    """Get a list of available example files."""
    try:
        import langgraph_codegen
        package_dir = Path(os.path.dirname(langgraph_codegen.__file__))
        examples_dir = package_dir / 'data' / 'examples'
        
        if not examples_dir.exists():
            return []
            
        # Get all files in the examples directory
        examples = []
        for file in examples_dir.glob('*'):
            if file.is_file():
                examples.append(str(file))
        return examples
    except Exception as e:
        print(f"{Fore.RED}Error listing examples: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Generate LangGraph code from graph specification")
    
    # Add the options
    parser.add_argument('--list', action='store_true', help='List available example graphs')
    parser.add_argument('--graph', action='store_true', help='Generate graph code')
    parser.add_argument('--nodes', action='store_true', help='Generate node code')
    parser.add_argument('--conditions', action='store_true', help='Generate condition code')
    parser.add_argument('--state', action='store_true', help='Generate state code')
    parser.add_argument('--code', action='store_true', help='Generate complete runnable script')
    parser.add_argument('-l', '--line-numbers', action='store_true', help='Show line numbers in generated code')
    
    # Single required argument
    parser.add_argument('graph_file', nargs='?', help='Path to the graph specification file')

    args = parser.parse_args()

    if args.list:
        list_examples()
        return

    # If no graph file provided, show help
    if not args.graph_file:
        parser.print_help()
        sys.exit(1)

    try:
        # First try to find the file as an example
        example_path = get_example_path(args.graph_file)
        file_path = example_path if example_path else args.graph_file
            
        # Read the specification file
        with open(file_path, 'r') as f:
            graph_spec = f.read()

        # If no generation flags are set, just show the file contents
        if not (args.graph or args.nodes or args.conditions or args.state or args.code):
            print(f"{Fore.BLUE}{graph_spec}{Style.RESET_ALL}")
            return
            
        # Get graph name from file name (without extension)
        graph_name = Path(args.graph_file).stem
        
        # Validate the graph specification
        validation_result = validate_graph(graph_spec)
        if "error" in validation_result:
            print(f"{Fore.RED}Error in graph specification:{Style.RESET_ALL}\n{validation_result['error']}", file=sys.stderr)
            print(f"\n{Fore.YELLOW}Suggested solutions:{Style.RESET_ALL}\n{validation_result['solution']}", file=sys.stderr)
            sys.exit(1)

        # Generate the requested code
        graph = validate_graph(graph_spec)
        
        if args.code:
            # Collect all code components
            complete_code = []
            
            # Add imports
            complete_code.append("""from typing import Dict, TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, Graph
from langchain_core.messages.tool import ToolMessage
from langchain_core.runnables.config import RunnableConfig
from operator import itemgetter
""")
            
            # Add components in specific order
            if 'graph' in graph:
                complete_code.append(gen_state(graph_spec))
                complete_code.append(gen_nodes(graph['graph']))
                complete_code.append(gen_conditions(graph_spec))
                complete_code.append(gen_graph(graph_name, graph_spec))
                
                # Add main section
                main_section = f"""
import random
def random_one_or_zero():
    return random.choice([False, True])

if __name__ == "__main__":
    import sys
    
    # Create the graph
    workflow = {graph_name}
    
    # Run the graph
    config = {{"last_state": "starting..."}}
    for output in workflow.stream(config):
        print(f"\\n    {{output}}\\n")
"""
                complete_code.append(main_section)
                
                # Join all code components and print
                full_code = "\n\n".join(complete_code)
                print_python_code(full_code, args.line_numbers)
                return
                
        # Handle individual component generation as before
        if args.graph:
            print_python_code(gen_graph(graph_name, graph_spec), args.line_numbers)
        if args.nodes:
            if 'graph' in graph:
                print_python_code(gen_nodes(graph['graph']), args.line_numbers)
        if args.conditions:
            if 'graph' in graph:
                print_python_code(gen_conditions(graph_spec), args.line_numbers)
        if args.state:
            if 'graph' in graph:
                print_python_code(gen_state(graph_spec), args.line_numbers)
        if 'errors' in graph:
            print(f"{Fore.RED}Errors in graph specification: \n\n{graph['errors']}\n\n{Fore.RESET}", file=sys.stderr)
            
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found: {args.graph_file}{Style.RESET_ALL}", file=sys.stderr)
        print(f"{Fore.YELLOW}Use --list-examples to see available example graphs{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()