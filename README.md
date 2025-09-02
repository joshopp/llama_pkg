# LLM Component - llama_pkg
A Python library for handling Large Language Model (LLM) operations in a multimodal brick manipulation system using gaze and speech input. This component manages tool calling and intention alignment by leveraging Llama 3.3 70B. The component runs on an external server and communicates via ZeroMQ.

## Overview
This library is one of three components in a complete multimodal manipulation system developed for a Bachelor's thesis. It specifically handles:
- LLM-based tool calling functionality
- LLM-based intention alignment processing  
- Communication via ZeroMQ

## Requirements
- Python 3.8+
- Additional dependencies listed in `requirements.txt`
- Llama 3.3 70B Instruct (downloadable [HERE](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/joshopp/llama_pkg.git
cd llama_pkg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Setup SSH Tunnel (Required)
For correct communication with the rest of the pipeline via ZMQ:
```bash
ssh -L 8000:localhost:8000 [your-server]
```

### 2. Start the LLM Server
```bash
cd src
python3 llm_server.py
```
Choose your desired models from the interactive menu. The server will handle LLM calls and communicate via ZeroMQ.


## Configuration

### Models
- Custom models can be added at the top of `chatbot.py`
- Model paths for alternative setups need to be changed in `chatbot.py`
- Make sure to import new model options in other scripts

### Prompts and Tools
- Setup prompts are saved in `setup.py` and can be modified there
- Tools are specified in `tool_definitions.py`
- **Important**: Any tool additions need to be made in both `tool_definitions.py` AND the setup prompt

### Communication
- Server runs on port 8000 by default
- ZMQ communication endpoint: `tcp://localhost:8000`
- SSH tunnel required for pipeline integration

## Core Components

### Main Scripts
- **`llm_server.py`**: Main server script - run this to start the LLM service
- **`chatbot.py`**: Contains model definitions and LLM interaction logic
- **`setup.py`**: Stores setup prompts for the system
- **`tool_definitions.py`**: Defines available tools for the LLM
- **`llm_utils.py`**: outsources commonly used functions in LLM interaction

### Benchmarking
Run benchmarking with the `llm_benchmark_*.py` scripts:

**Important Notes:**
- Activate/deactivate models to benchmark at the top of benchmark scripts
- Change iterations and filepath for custom output
- Resources are not freed after initialization - multiple iterations might fail for large models
- Benchmark commands can be modified in `experiment_prompts_*.py`

**For GPT-4 Testing:**
Add your personal API key in `llm_utils.py` → `initialize_openai()` function


## Architecture

This component operates as part of a three-part system:

1. **[Multimodal data streaming component](https://github.com/joshopp/aria_pkg)**: Streams and processes data from the Meta Aria glasses
2. **[Robot Component](https://github.com/joshopp/robot_pkg)**: Handles robot control
3. **LLM Component (this package)**: Manages language understanding and tool calling

The components communicate through a distributed architecture using ZeroMQ for efficient inter-process communication.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Academic Context

This work was developed as part of a Bachelor's thesis on multimodal manipulation systems. If you use this work in academic research, please cite appropriately.

## Contact

**Author**: joshopp  
**Project Link**: [https://github.com/joshopp/llama_pkg](https://github.com/joshopp/llama_pkg)
