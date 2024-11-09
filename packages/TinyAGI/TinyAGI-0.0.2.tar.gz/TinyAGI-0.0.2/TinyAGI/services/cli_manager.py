# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/cli_manager.py

import argparse
import sys
import json
import logging
from ..agent import AgentSystem
from ..utils import setup_logging

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='TinyAGI CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    parser_generate = subparsers.add_parser('generate', help='Generate text from a prompt')
    parser_generate.add_argument('--prompt', '-p', required=True, help='Prompt text')
    parser_generate.add_argument('--config', '-c', help='Path to config file')
    parser_generate.add_argument('--stream', '-s', action='store_true', help='Stream output')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_logging()
    config_file = args.config if args.config else 'config/agent_config.json'
    agent_system = AgentSystem(config_file)
    agent_manager = agent_system.agent_manager
    plugin_manager = agent_system.plugin_manager
    tool_manager = agent_system.tool_manager

    # Execute tasks defined in the configuration
    if args.command == 'generate':
        try:
            # Find the task that matches the prompt
            task = next((t for t in agent_system.config.get('tasks', []) if t['input'].get('prompt') == args.prompt), None)
            if not task:
                logger.error(f"No task found matching the prompt: {args.prompt}")
                sys.exit(1)
            
            plugin = plugin_manager.get_plugin(task['plugin'])
            agent = agent_manager.get_agent(task['agent'])
            tool = tool_manager.get_tool(task['tool'])

            if not plugin or not agent:
                logger.error("Required plugin or agent not found.")
                sys.exit(1)

            input_data = task.get('input', {})
            options = task.get('options', {})

            # Override stream option if provided
            if args.stream:
                options['stream'] = True

            response = plugin.execute(agent, tool, input_data, options, stream=args.stream)
            if args.stream and response:
                for chunk in response:
                    print(chunk, end='', flush=True)
            else:
                print(response)
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            sys.exit(1)

def run_cli():
    """
    Run the CLI manager.
    """
    main()


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
