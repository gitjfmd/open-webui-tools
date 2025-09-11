# OpenWebUI-Tools 🔧🚀

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

> Your ultimate toolkit for supercharging **Open WebUI**. A collection of powerful, open-source custom tools, scripts, and integrations built by and for the community.

**Unleash the full potential of your local AI interface.** This repository is home to community-built extensions that add new functionalities, streamline workflows, and connect Open WebUI to the wider ecosystem.

---

## ✨ Featured Tool Categories

Dive into a growing arsenal of tools designed to enhance your Open WebUI experience. Click on a category to jump to its section.

| | Category | Description |
| :--- | :--- | :--- |
| 🧠 | [**Workspace Tools**](#-workspace-tools) | Tools that run directly in OpenWebUI's Python sandbox. |
| 🌐 | [**API Integrations**](#-api-integrations) | Connect OWUI to external services and APIs. |
| 🔄 | [**Workflows**](#-workflows) | Pre-configured chains for complex tasks. |
| 🎨 | [**UI Extensions**](#-ui-extensions) | Enhance the look and feel of the interface. |
| ⚙️ | [**System Utilities**](#-system-utilities) | Scripts for management and customization. |
| 🧪 | [**Experimental**](#-experimental) | Cutting-edge features and proof-of-concepts. |

---

## 🧠 Workspace Tools

These tools run directly in OpenWebUI's Python environment and can be easily added through the Admin Panel. They empower your assistants with new capabilities.

**📦 Installation:**
1.  Navigate to **Workspace** → **Tools** → **Create Tool**. or Navigate to **Admin Panel** → **External Tools** → **Create Tool**. Depends on the tool. Follow the guides for each tool. 
2.  Copy and paste the Python code from a tool's `.py` file in this repo.
3.  Save, enable it for your models, and you're done!

**🎯 Examples:**
- `Web Search with SearXNG` - Enhanced internet browsing capabilities.
- `PDF & Document Analyzer` - Extract and summarize text from uploaded files.
- `Code Interpreter` - Write, execute, and debug code in multiple languages.
- `Data Visualizer` - Generate charts and graphs from data.

*Each tool includes a detailed README with specific setup and usage instructions.*
**[Browse all Workspace Tools →](./tools/workspace-tools)*

---

## 🌐 API Integrations

Connect your OpenWebUI instance to the world. These integrations give your AI access to real-time data and the ability to interact with other platforms.

**🎯 Examples:**
- **Cloud Storage:** Google Drive, Dropbox sync for file management.
- **Productivity:** Notion, Trello, Calendar assistants for task management.
- **Communication:** Discord, Slack bots for team collaboration.
- **Data Services:** Real-time weather, stock prices, and news feeds.

*Most integrations require API keys, which are securely managed via environment variables.*
**[Browse all API Integrations →](./tools/api-integrations)*

---

## 🔄 Workflows

Why use one tool when you can chain them together? Workflows automate multi-step processes, turning your assistant into a powerful productivity engine.

**🎯 Examples:**
- `Research Agent`: `Web Search` → `Summarize` → `Generate Report`.
- `Content Creator`: `Draft Blog Post` → `Find Images` → `Post to CMS`.
- `Data Analyst`: `Load Dataset` → `Clean Data` → `Analyze` → `Visualize`.

---

## 🎨 UI Extensions

Customize and personalize your OpenWebUI experience. Change how it looks and feels without touching the core code.

**🎯 Examples:**
- **Themes:** Light, dark, solarized, and custom color schemes.
- **Layouts:** Alternate arrangements for chats, settings, and menus.
- **Custom CSS:** Inject your own styles for ultimate control.

---

## ⚙️ System Utilities

Essential scripts for maintaining, managing, and getting the most out of your OpenWebUI deployment.

**🎯 Examples:**
- `Bulk Chat Exporter` - Back up or migrate your conversations.
- `Model Manager` - Easily download, switch, and manage your AI models.
- `Backup & Restore` - Scripts to safeguard your entire instance.

---

## 🧪 Experimental

This is the cutting edge. Here you'll find beta features, proof-of-concepts, and tools that push the boundaries of what's possible.

**⚠️ Note:** These tools may be unstable. Use with caution and provide feedback!
**🎯 Examples:** Autonomous AI agents, advanced reasoning systems.

---

## 🚀 Quick Start

### Prerequisites
- A running instance of [Open WebUI](https://github.com/open-webui/open-webui).
- Basic familiarity with terminal/command line (for some utilities).

### Method 1: Clone the Entire Repository
```bash
git clone https://github.com/gitjfmd/open-webui-tools.git
cd open-webui-tools
