# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agent.py

import logging
from .task_manager import TaskManager
from .plugins.plugin_manager import PluginManager
from .modules.module_manager import ModuleManager
from .agents.agent_manager import AgentManager
from .tools.tool_manager import ToolManager
from .utils import load_json, setup_logging, download_nltk_resources
from typing import List, Union

logger = logging.getLogger(__name__)

class AgentSystem:
    def __init__(self, config_files: Union[str, List[str]]):
        """
        Initialize the AgentSystem with configuration, agent manager, plugin manager, and tool manager.

        :param config_files: Path(s) to the JSON configuration file(s).
        """
        setup_logging()
        download_nltk_resources()
        self.config = self.load_and_merge_configs(config_files)
        self.module_manager = ModuleManager(self.config.get('modules', []))
        self.agent_manager = AgentManager(self.config.get('agents', []), self.module_manager)
        self.plugin_manager = PluginManager(self.config.get('plugins', []))
        self.tool_manager = ToolManager(self.config.get('tools', []))
        self.task_manager = TaskManager(
            self.agent_manager,
            self.plugin_manager,
            self.tool_manager,
            self.config.get('tasks', [])
        )
        logger.info("AgentSystem initialized.")

    def load_and_merge_configs(self, config_files: Union[str, List[str]]) -> dict:
        """
        Load and merge multiple JSON configuration files.

        :param config_files: Path(s) to the JSON configuration file(s).
        :return: Merged configuration dictionary.
        """
        if isinstance(config_files, str):
            config_files = [config_files]
        
        merged_config = {}
        for file in config_files:
            config = load_json(file)
            merged_config = self.merge_dicts(merged_config, config)
            logger.info(f"Merged configuration from '{file}'.")
        
        return merged_config

    def merge_dicts(self, base: dict, new: dict) -> dict:
        """
        Recursively merge two dictionaries.

        :param base: The base dictionary.
        :param new: The new dictionary to merge into the base.
        :return: Merged dictionary.
        """
        for key, value in new.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = self.merge_dicts(base[key], value)
                elif isinstance(base[key], list) and isinstance(value, list):
                    base[key].extend(value)
                else:
                    base[key] = value
            else:
                base[key] = value
        return base

    def run(self):
        """
        Execute all tasks assigned to this agent system.
        """
        logger.info("AgentSystem started.")
        self.task_manager.execute_tasks()
        logger.info("AgentSystem finished execution.")


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
