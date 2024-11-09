<p align="center">
  <img src="https://raw.githubusercontent.com/SullyGreene/TinyAGI/refs/heads/main/Static/logo.png" alt="TinyAGI Logo">
</p>


# 🧠 TinyAGI (Preview Version)

**TinyAGI** is a modular, extensible, and lightweight framework for building Artificial General Intelligence (AGI) systems. TinyAGI allows you to create and manage AI agents, plugins, modules, and tools within a flexible, scalable architecture, supporting multiple model backends like OpenAI, Llama.cpp, Ollama, AlpacaX, and Tabitha.

**Disclaimer:** This is a **preview release** (version 0.0.2). TinyAGI is currently under active development, and this version is intended for testing, feedback, and early experimentation. Expect frequent updates and potential changes to the API.

[![License](https://img.shields.io/github/license/SullyGreene/TinyAGI)](https://github.com/SullyGreene/TinyAGI/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/TinyAGI.svg)](https://pypi.org/project/TinyAGI/)

---

## 🧩 Key Features

- **Multi-Model Support**: Integrate with OpenAI, Llama.cpp, Ollama, AlpacaX, and Tabitha, providing flexibility for various tasks.
- **Modular Architecture**: Add, update, or remove agents and plugins with ease.
- **Dynamic Plugin System**: Extend functionality with plugins for tasks like text summarization, content formatting, and more.
- **CLI and API Interfaces**: Interact with TinyAGI using the command-line interface or RESTful API.
- **AgentX System**: Manage multiple AI agents with unique configurations and specialized behaviors.
- **Task Automation**: Orchestrate agents, plugins, and tools to automate complex workflows.

---

## 📦 Installation

Install TinyAGI with pip (Python 3.8 or higher required):

```bash
pip install TinyAGI
```

For the latest development version, you can clone the repository:

```bash
git clone https://github.com/SullyGreene/TinyAGI.git
cd TinyAGI
pip install -e .
```

---

## 🚀 Getting Started

1. **Create a Configuration File**: Define your agent and model parameters in a JSON file.
   
   ```json
   {
     "agent": {
       "name": "TinyAGI Agent",
       "version": "0.0.2"
     },
     "model": {
       "type": "llama_cpp",
       "name": "Llama-2-7B",
       "parameters": {
         "model_path": "models/llama-2-7b.ggmlv3.q4_0.bin",
         "temperature": 0.7,
         "max_tokens": 512
       }
     }
   }
   ```

2. **Run the Agent**: Create a Python script to initialize and run the agent.

   ```python
   from TinyAGI.agent import Agent

   if __name__ == '__main__':
       agent = Agent(config_file='config/agent_config.json')
       agent.run()
   ```

3. **Interact with Your Agent**: Use the command-line interface or API to execute tasks, generate text, and more.

---

## 🛠 Example Use Cases

- **Content Generation**: Generate articles, summaries, or encyclopedia entries using specialized plugins.
- **Data Analysis**: Automate data processing, summarization, and report generation.
- **Interactive Chatbots**: Create engaging chatbots that integrate knowledge retrieval and sentiment analysis.

---

## 📝 Contributing

Contributions are welcome! Please see our [contribution guidelines](https://github.com/SullyGreene/TinyAGI) to get started. TinyAGI Hub is also available for community plugins, agents, and tools at [TinyAGI Hub](https://github.com/SullyGreene/TinyAGI-Hub).

---

## 🛡 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/SullyGreene/TinyAGI/blob/main/LICENSE) file for details.

---

## **Disclaimer**

This release is version 0.0.2 and is a **preview** for testing and feedback. The framework is in active development, so expect frequent updates and possible changes to the API and functionality.

---

**Ready to experiment?** Install TinyAGI today and help shape the future of AGI development! 🚀