# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/server_manager.py

from flask import Flask, request, jsonify, Response
from ..agent import AgentSystem
from ..utils import setup_logging
import logging

logger = logging.getLogger(__name__)

# Global variables to hold the agent system and related components
agent_system = None
agent = None
config = None
plugin_manager = None
task_manager = None
tool_manager = None

# Default agent name (ensure this matches an agent defined in your configuration)
default_agent_name = 'default_agent'

def create_app():
    """
    Create and configure the Flask application.

    :return: Configured Flask app
    """
    app = Flask(__name__)
    setup_logging()

    global agent_system, agent, config, plugin_manager, task_manager, tool_manager

    # Initialize AgentSystem
    agent_system = AgentSystem(config_file='config/agent_config.json')
    agent_manager = agent_system.agent_manager
    tool_manager = agent_system.tool_manager

    # Get configuration from AgentSystem
    config = agent_system.config

    # Get the default agent
    agent = agent_manager.get_agent(default_agent_name)
    if not agent:
        logger.error(f"Default agent '{default_agent_name}' not found.")
        raise ValueError(f"Agent '{default_agent_name}' is not available.")

    # PluginManager and TaskManager are initialized within AgentSystem
    plugin_manager = agent_system.plugin_manager
    task_manager = agent_system.task_manager

    @app.route('/chat', methods=['POST'])
    def chat():
        """
        Handle chat requests.
        """
        data = request.get_json()
        messages = data.get('messages')
        inference_params = data.get('inference_params', {})
        stream = data.get('stream', False)

        if not messages:
            return jsonify({'error': 'Messages are required'}), 400

        # Build prompt from messages
        prompt = ''
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role.capitalize()}: {content}\n"

        prompt += "Assistant:"

        try:
            if stream:
                def generate():
                    for chunk in agent.generate_text(prompt, stream=True):
                        yield chunk
                return Response(generate(), mimetype='text/plain')
            else:
                generated_text = agent.generate_text(prompt)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/generate', methods=['POST'])
    def generate():
        """
        Handle text generation requests.
        """
        data = request.get_json()
        prompt = data.get('prompt')
        inference_params = data.get('inference_params', {})
        stream = data.get('stream', False)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        try:
            if stream:
                def generate_stream():
                    for chunk in agent.generate_text(prompt, stream=True):
                        yield chunk
                return Response(generate_stream(), mimetype='text/plain')
            else:
                generated_text = agent.generate_text(prompt)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/embed', methods=['POST'])
    def embed():
        """
        Handle embedding requests.
        """
        data = request.get_json()
        input_data = data.get('input')

        if not input_data:
            return jsonify({'error': 'Input text is required'}), 400

        try:
            embeddings = agent.embed(input_data)
            return jsonify({'embedding': embeddings})
        except Exception as e:
            logger.error(f"Error during embedding: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/reload', methods=['POST'])
    def reload_model():
        """
        Reload the model with new configuration.
        """
        data = request.get_json()
        config_file = data.get('config_file')
        if not config_file:
            return jsonify({'error': 'Config file path is required'}), 400

        try:
            global agent_system, agent, plugin_manager, task_manager, config, tool_manager

            # Re-initialize AgentSystem with the new configuration file
            agent_system = AgentSystem(config_file=config_file)
            agent_manager = agent_system.agent_manager
            tool_manager = agent_system.tool_manager

            # Update configuration
            config = agent_system.config

            # Update the default agent
            agent = agent_manager.get_agent(default_agent_name)
            if not agent:
                logger.error(f"Default agent '{default_agent_name}' not found after reload.")
                return jsonify({'error': f"Agent '{default_agent_name}' is not available after reload."}), 400

            # Update PluginManager and TaskManager
            plugin_manager = agent_system.plugin_manager
            task_manager = agent_system.task_manager

            logger.info("Model and configuration reloaded successfully.")
            return jsonify({'message': 'Model reloaded successfully'}), 200
        except Exception as e:
            logger.error(f"Error during model reload: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/config', methods=['GET'])
    def get_config():
        """
        Retrieve the current configuration.
        """
        return jsonify(config), 200

    return app

def run_server():
    """
    Run the Flask server.
    """
    app = create_app()
    app.run(debug=True)


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
