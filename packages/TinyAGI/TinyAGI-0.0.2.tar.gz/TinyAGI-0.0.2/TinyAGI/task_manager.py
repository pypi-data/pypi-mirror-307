# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/task_manager.py

import logging
import json
import os

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, agent_manager, plugin_manager, tool_manager, tasks_config):
        """
        Initialize the TaskManager with the provided agent manager, plugin manager, tool manager, and tasks configuration.

        :param agent_manager: Instance of AgentManager.
        :param plugin_manager: Instance of PluginManager.
        :param tool_manager: Instance of ToolManager.
        :param tasks_config: List of task configurations from the JSON config.
        """
        self.agent_manager = agent_manager
        self.plugin_manager = plugin_manager
        self.tool_manager = tool_manager
        self.tasks = tasks_config

    def execute_tasks(self):
        """
        Iterate through all tasks defined in the configuration and execute them using the appropriate agents, plugins, and tools.
        """
        logger.debug(f"Available plugins: {list(self.plugin_manager.loaded_plugins.keys())}")
        logger.debug(f"Available agents: {list(self.agent_manager.loaded_agents.keys())}")
        logger.debug(f"Available tools: {list(self.tool_manager.loaded_tools.keys())}")

        for task in self.tasks:
            task_id = task.get('task_id')
            plugin_name = task.get('plugin')
            agent_name = task.get('agent')  # Specify which agent to use
            tool_name = task.get('tool')    # Specify which tool to use (optional)
            input_data = task.get('input', {})
            output_config = task.get('output', {})
            options = task.get('options', {})

            logger.info(f"Executing task: {task_id} using plugin: {plugin_name}, agent: {agent_name}, tool: {tool_name}")

            # Validate plugin
            if plugin_name not in self.plugin_manager.loaded_plugins:
                logger.error(f"Plugin '{plugin_name}' not found. Skipping task '{task_id}'.")
                continue
            plugin = self.plugin_manager.get_plugin(plugin_name)

            # Validate agent
            agent = self.agent_manager.get_agent(agent_name)
            if not agent:
                logger.error(f"Agent '{agent_name}' not found. Skipping task '{task_id}'.")
                continue

            # Validate tool if specified
            tool = None
            if tool_name:
                tool = self.tool_manager.get_tool(tool_name)
                if not tool:
                    logger.error(f"Tool '{tool_name}' not found. Skipping task '{task_id}'.")
                    continue

            # Execute the plugin with the specified agent and tool
            try:
                if plugin_name == "GenerateReferences":
                    # Specific logic for GenerateReferences plugin
                    # Fetch summary from Wikipedia
                    query = input_data.get('query', '')
                    summary = tool.get_page_summary(query)
                    if not summary:
                        logger.error(f"No summary found for query '{query}'. Skipping task '{task_id}'.")
                        continue

                    # Prepare the prompt for generating references
                    prompt = f"Extract references from the following summary:\n\n{summary}"

                    # Execute the GenerateReferences plugin
                    plugin_config = {
                        "text": summary
                    }
                    references = plugin.execute(agent, tool=None, input_data=plugin_config, options=options, stream=options.get('stream', False))
                    print(f"\nTask: {task_id} - Generated References:")
                    for ref in references:
                        print(f"{ref['id']}. {ref['source']}")

                elif plugin_name == "GenerateText":
                    # General logic for GenerateText plugin
                    response = plugin.execute(agent, tool, input_data, options, stream=options.get('stream', False))

                    if tool_name == "WikipediaTool":
                        # Task: Fetch and Rewrite Summary
                        print(f"\nTask: {task_id} - Rewritten Summary:\n")
                        print(response)
                        print('\n')
                    
                    elif not tool_name:
                        # Task: Rewrite References
                        print(f"\nTask: {task_id} - Rewritten References:\n")
                        print(response)
                        print('\n')
                    
                    else:
                        # Handle other GenerateText tasks if any
                        print(f"\nTask: {task_id} - Response:\n")
                        print(response)
                        print('\n')
                
                else:
                    # Handle other plugins if any
                    response = plugin.execute(agent, tool, input_data, options, stream=options.get('stream', False))
                    print(f"\nTask: {task_id} - Response:\n")
                    print(response)
                    print('\n')
                
            except Exception as e:
                logger.error(f"Error during task '{task_id}' execution: {e}")

    def save_output(self, data, output_config):
        """
        Save the output data based on the output configuration.

        :param data: Data to save.
        :param output_config: Dictionary containing output configuration.
        """
        try:
            file_path = output_config.get('file_path', 'output.json')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Output saved to '{file_path}'.")
        except Exception as e:
            logger.error(f"Error saving output to file: {e}")


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
