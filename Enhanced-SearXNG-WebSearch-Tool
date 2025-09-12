# Enhanced SearXNG Web Search Tool

![Version](https://img.shields.io/badge/version-1.4.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenWebUI](https://img.shields.io/badge/OpenWebUI-0.4.0+-orange)

A powerful web search tool for OpenWebUI that connects to SearXNG instances to provide secure, private, and comprehensive web search capabilities directly within your chat interface.

## Features

- **Multiple Search Engines**: Uses Google, Brave, DuckDuckGo, GitHub, Reddit, Wikidata, Mojeek, and Qwant
- **Automatic Fallbacks**: If your local SearXNG instance fails, automatically tries public instances
- **Rate Limit Protection**: Smart handling of rate limits with automatic retries and exponential backoff
- **Security Enhancements**: Input validation, sanitization, and protection against common vulnerabilities
- **Flexible Configuration**: Easily adjust settings through the Valves interface
- **Multiple Output Formats**: Supports both HTML and JSON responses from SearXNG
- **Domain Flexibility**: Works with both internal Docker networks and external domains

## Requirements

- OpenWebUI v0.4.0 or higher
- A SearXNG instance (local or remote)
- Python packages: `requests`, `beautifulsoup4` (automatically installed by OpenWebUI)

## Installation in OpenWebUI

1. **Log into your OpenWebUI** as admin
2. **Navigate to Workspace**
3. **Select Tools** from the sidebar
4. **Click "Create Tool"** button
5. **Copy the tool code** from `web_search_tool_v1.0.py` in this repository
6. **Paste the code** into the editor
7. **Click Save**
8. **Enable the tool** for your models:
   - Go to Workspace → Models
   - Select your model and click edit (✏️)
   - Check "Enhanced SearXNG Web Search" in the Tools section
   - Save changes

## Configuration

The tool is pre-configured with optimal settings, but you can adjust these through the Valves interface:

| Setting | Description | Default |
|---------|-------------|---------|
| `searxng_url` | Your SearXNG instance URL | `http://searxng:8085` |
| `search_path` | Search path | `/search` |
| `max_results` | Number of results to return | `5` |
| `rate_limit_requests` | Maximum requests per minute | `20` |
| `enabled_engines` | Which search engines to use | `google,brave,duckduckgo,github,reddit,wikidata,mojeek,qwant` |
| `output_format` | Response format (html or json) | `html` |
| `use_fallback_instances` | Whether to use public instances as fallbacks | `true` |

## Docker Setup

If you're running OpenWebUI in Docker and want to use a local SearXNG instance, make sure both containers are on the same network:

```bash
# Create a shared network if you don't have one
docker network create ai-network

# Run SearXNG
docker run -d --name searxng --network ai-network -p 8085:8080 searxng/searxng

# Run OpenWebUI (ensure it's on the same network)
docker run -d --name openwebui --network ai-network -p 8080:8080 openwebui/openwebui
```

Then in the tool configuration, set `searxng_url` to `http://searxng:8080`.

## Usage

Once installed and enabled, you can use the tool in two ways:

### 1. Direct Usage

```
Search for information about Docker containers
```

### 2. Specific Queries

```
Search for "machine learning best practices" site:github.com
```

### 3. Advanced Operators

The tool supports various search operators:
- `site:example.com` - Limit results to a specific domain
- `"exact phrase"` - Search for an exact phrase
- `filetype:pdf` - Search for specific file types
- `+must +include` - Terms that must be included
- `-exclude` - Terms to exclude

## How It Works

This tool connects to your SearXNG instance (a privacy-focused metasearch engine) and sends search queries to it. SearXNG then aggregates results from multiple search engines and returns them to OpenWebUI. The tool formats these results nicely and presents them in your chat.

If your primary SearXNG instance is unavailable or rate-limited, the tool automatically tries public instances to ensure you always get search results.

## Security Features

- **Input Validation**: Prevents injection attacks
- **Rate Limiting**: Prevents abuse and API lockouts
- **Domain Whitelisting**: Prevents SSRF attacks
- **Content Filtering**: Removes potentially malicious content
- **Error Handling**: Prevents information disclosure

## Fallback Instances

If your primary SearXNG instance fails, the tool will automatically try these public instances:

1. searx.stream
2. search.rhscz.eu
3. searx.tiekoetter.com
4. searx.dresden.network
5. search.mdosch.de

## License

This tool is licensed under the MIT License.

## Credits

- Uses [SearXNG](https://github.com/searxng/searxng) as the search backend
- Developed for the OpenWebUI community

