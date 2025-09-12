"""
title: Enhanced SearXNG Web Search
author: Secure Search Integration
description: Secure web search using SearXNG with top engines, domain flexibility, and multiple output formats
required_open_webui_version: 0.4.0
requirements: requests, beautifulsoup4
version: 1.3.0
license: MIT
"""

import os
import re
import json
import time
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote_plus
from typing import Dict, List, Optional, Any, Union
import concurrent.futures
import random

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        """Initialize the SearXNG Web Search Tool."""
        self.valves = self.Valves()
        self.help_functions = SecureHelpFunctions()
        # Track SearXNG rate limit status
        self.searxng_rate_limited = False
        self.searxng_cooldown_until = 0

    class Valves(BaseModel):
        """Configuration valves for the SearXNG web search tool."""
        searxng_url: str = Field(
            default="http://searxng:8085",
            description="SearXNG base URL (e.g., http://searxng:8085 or https://example.com)"
        )
        search_path: str = Field(
            default="/search",
            description="Search path (e.g., /search)"
        )
        max_results: int = Field(
            default=5, 
            description="Maximum number of search results to return (1-20)"
        )
        rate_limit_requests: int = Field(
            default=20,
            description="Maximum requests per minute (1-60)"
        )
        request_timeout: int = Field(
            default=15,
            description="Request timeout in seconds (5-30)"
        )
        search_categories: str = Field(
            default="general",
            description="Comma-separated search categories (general,images,news,etc)"
        )
        search_language: str = Field(
            default="en-US",
            description="Search language (e.g., en-US, fr-FR, de-DE)"
        )
        search_delay: float = Field(
            default=1.0,
            description="Delay in seconds between searches (0-5)"
        )
        auto_retry: bool = Field(
            default=True,
            description="Automatically retry rate-limited searches with backoff"
        )
        max_retries: int = Field(
            default=3,
            description="Maximum number of retries for rate-limited searches (0-5)"
        )
        retry_delay: int = Field(
            default=5,
            description="Base delay in seconds between retries (will increase with backoff)"
        )
        # Top engines to prioritize in SearXNG
        enabled_engines: str = Field(
            default="wikipedia,duckduckgo,wikidata,currency,deviantart",
            description="Comma-separated list of engines to enable in SearXNG"
        )
        # Output format
        output_format: str = Field(
            default="html",
            description="Output format from SearXNG (html or json)"
        )

    def search_web(self, query: str, __user__: Optional[dict] = None) -> str:
        """
        Perform a web search using SearXNG instance with improved rate limit handling.
        
        :param query: The search query to execute
        :param __user__: User information (injected by OpenWebUI)
        :return: Formatted search results or error message
        """
        
        # Get user identifier for rate limiting
        user_id = __user__.get("id", "anonymous") if __user__ else "anonymous"
        
        # Check if SearXNG is in cooldown period
        now = time.time()
        if self.searxng_rate_limited and now < self.searxng_cooldown_until:
            cooldown_remaining = int(self.searxng_cooldown_until - now)
            return f"⚠️ **SearXNG Rate Limited:** Please wait {cooldown_remaining} seconds before searching again."
        
        # Reset rate limit status if cooldown period has passed
        if self.searxng_rate_limited and now >= self.searxng_cooldown_until:
            self.searxng_rate_limited = False
        
        # Rate limiting check for this user
        if not self.help_functions.check_rate_limit(user_id, self.valves.rate_limit_requests):
            return "⚠️ **Rate limit exceeded.** Please wait a moment before making another search request."
        
        # Validate search query
        query_validation = self.help_functions.validate_search_query(query)
        if not query_validation["valid"]:
            return f"❌ **Invalid query:** {query_validation['error']}"
        
        sanitized_query = query_validation["sanitized_query"]
        
        # Add configurable delay to prevent overwhelming SearXNG
        if self.valves.search_delay > 0:
            # Add a small random component to avoid synchronized requests
            actual_delay = self.valves.search_delay * (0.8 + 0.4 * random.random())
            time.sleep(actual_delay)
        
        # Track retries
        retries = 0
        max_retries = self.valves.max_retries if self.valves.auto_retry else 0
        
        while retries <= max_retries:
            try:
                # Build SearXNG URL
                searxng_base_url = self.valves.searxng_url.rstrip('/')
                search_path = self.valves.search_path.lstrip('/')
                
                # Parse categories
                categories = [cat.strip() for cat in self.valves.search_categories.split(',')]
                categories_param = "&".join([f"category_{cat}=on" for cat in categories])
                
                # Parse engines
                engines = [eng.strip() for eng in self.valves.enabled_engines.split(',')]
                engines_param = "&".join([f"engine_{eng}=on" for eng in engines])
                
                # Determine output format
                output_format = self.valves.output_format.lower()
                if output_format not in ["html", "json"]:
                    output_format = "html"  # Default to HTML if invalid format
                
                # Build search URL
                search_url = f"{searxng_base_url}/{search_path}?q={quote_plus(sanitized_query)}&{categories_param}&{engines_param}&language={self.valves.search_language}&format={output_format}"
                
                # Make the search request
                response = self.help_functions.safe_request(
                    search_url,
                    timeout=self.valves.request_timeout
                )
                
                if not response["success"]:
                    # Check if this is a rate limit error
                    if "rate limit" in response["error"].lower() or response.get("status_code") in [429, 503]:
                        # Set rate limit status
                        self.searxng_rate_limited = True
                        # Exponential backoff: 5s, 10s, 20s, etc.
                        backoff_time = self.valves.retry_delay * (2 ** retries)
                        self.searxng_cooldown_until = time.time() + backoff_time
                        
                        if retries < max_retries:
                            retries += 1
                            # Wait and retry
                            time.sleep(backoff_time)
                            continue
                        else:
                            return f"⚠️ **SearXNG Rate Limited:** {response['error']}. Please try again in {backoff_time} seconds."
                    else:
                        return f"❌ **Search Error:** {response['error']}"
                
                # Process the content based on format
                if output_format == "json":
                    try:
                        # Parse JSON response
                        json_data = json.loads(response["content"])
                        results = self.help_functions.extract_json_results(
                            json_data,
                            max_results=self.valves.max_results
                        )
                        engines_used = json_data.get("engines", [])
                    except json.JSONDecodeError:
                        return "❌ **Error:** Invalid JSON response from SearXNG"
                else:  # HTML format
                    # Process the HTML content
                    results = self.help_functions.extract_html_results(
                        response["content"],
                        max_results=self.valves.max_results
                    )
                    # Get the engines that were used
                    engines_used = self.help_functions.extract_engines_used(response["content"])
                
                # Check for rate limit messages in the response
                if not results and (
                    (output_format == "html" and self.help_functions.detect_rate_limit_page(response["content"])) or
                    (output_format == "json" and json_data.get("error", "").lower().find("rate limit") != -1)
                ):
                    # Set rate limit status
                    self.searxng_rate_limited = True
                    # Exponential backoff: 5s, 10s, 20s, etc.
                    backoff_time = self.valves.retry_delay * (2 ** retries)
                    self.searxng_cooldown_until = time.time() + backoff_time
                    
                    if retries < max_retries:
                        retries += 1
                        # Wait and retry
                        time.sleep(backoff_time)
                        continue
                    else:
                        return f"⚠️ **SearXNG Rate Limited:** Too many requests. Please try again in {backoff_time} seconds."
                
                if not results:
                    return f"🔍 **No results found for:** {sanitized_query}\n\nTry rephrasing your search query or using different keywords."
                
                # Format the final response
                formatted_results = "\n\n".join([
                    f"**[{result['title']}]({result['url']})**\n{result['content']}"
                    for result in results
                ])
                
                # Format engines used info
                engines_info = f"Engines used: {', '.join(engines_used)}" if engines_used else ""
                
                result = f"""🔍 **Search Results for:** {sanitized_query}

{formatted_results}

---
*Search completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*{engines_info}*
*Rate limit: {self.help_functions.get_rate_limit_status(user_id, self.valves.rate_limit_requests)}*"""
                
                return result
                
            except Exception as e:
                if retries < max_retries:
                    retries += 1
                    # Wait and retry with exponential backoff
                    backoff_time = self.valves.retry_delay * (2 ** retries)
                    time.sleep(backoff_time)
                    continue
                else:
                    return f"❌ **Unexpected Error:** Search failed due to: {str(e)}"
        
        # This should never be reached, but just in case
        return "❌ **Search Error:** Maximum retries exceeded."

    def web_search(self, query: str, __user__: Optional[dict] = None) -> str:
        """Alternative function name for compatibility."""
        return self.search_web(query, __user__)


class SecureHelpFunctions:
    """Helper class with security functions for the web search tool."""
    
    def __init__(self):
        # Rate limiting storage (in-memory for simplicity)
        self.request_history = {}
        self.rate_limit_window = 60  # seconds
        
        # Request headers for legitimate browsing
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OpenWebUI-SecureSearch/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def check_rate_limit(self, user_id: str, max_requests: int) -> bool:
        """Check if user is within rate limits."""
        now = time.time()
        cutoff = now - self.rate_limit_window
        
        # Clean old entries
        self.request_history = {
            uid: timestamps for uid, timestamps in self.request_history.items()
            if any(t > cutoff for t in timestamps)
        }
        
        # Check current user
        if user_id not in self.request_history:
            self.request_history[user_id] = []
        
        # Remove old timestamps for this user
        self.request_history[user_id] = [
            t for t in self.request_history[user_id] if t > cutoff
        ]
        
        # Check if over limit
        if len(self.request_history[user_id]) >= max_requests:
            return False
        
        # Add current request
        self.request_history[user_id].append(now)
        return True

    def get_rate_limit_status(self, user_id: str, max_requests: int) -> str:
        """Get current rate limit status for user."""
        current_requests = len(self.request_history.get(user_id, []))
        return f"{current_requests}/{max_requests} requests used"

    def validate_search_query(self, query: str) -> Dict[str, Any]:
        """Validate and sanitize search query with improved handling for search operators."""
        if not query or not isinstance(query, str):
            return {"valid": False, "error": "Query must be a non-empty string"}
        
        # Length validation
        if len(query) > 500:
            return {"valid": False, "error": "Query too long (max 500 characters)"}
        
        if len(query.strip()) < 1:
            return {"valid": False, "error": "Query too short (min 1 character)"}
        
        # IMPROVED: Allow common search operators and special characters
        # This regex allows:
        # - Alphanumeric characters
        # - Common punctuation
        # - Quotes for exact matches
        # - Colons for operators like site:
        # - Special search operators like + - | " : / . @ # $ % ^ & * ( ) [ ] { }
        if not re.match(r'^[a-zA-Z0-9\s\-_.,!?()[\]{}:;@#$%^&*+=/\'"]+$', query):
            return {"valid": False, "error": "Query contains invalid characters"}
        
        # Basic XSS/injection prevention - remove script tags and other potentially harmful HTML
        sanitized_query = re.sub(r'<[^>]*>', '', query).strip()
        
        return {"valid": True, "sanitized_query": sanitized_query}

    def safe_request(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Make a safe HTTP request with security controls."""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True,
                verify=False  # For internal services, often needed
            )
            
            # Check for rate limiting response codes
            if response.status_code in [429, 503]:
                return {
                    "success": False, 
                    "error": "Rate limit exceeded on SearXNG instance",
                    "status_code": response.status_code
                }
            
            response.raise_for_status()
            
            return {
                "success": True, 
                "content": response.content.decode('utf-8', errors='ignore'),
                "status_code": response.status_code
            }
            
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout - SearXNG instance may be slow or unreachable"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection error - Cannot connect to SearXNG instance"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}

    def detect_rate_limit_page(self, html_content: str) -> bool:
        """Detect if the page is a rate limit notification."""
        if not html_content:
            return False
        
        # Common rate limit indicators in SearXNG
        rate_limit_indicators = [
            "rate limit",
            "too many requests",
            "429",
            "try again later",
            "blocked",
            "captcha",
            "automated requests",
            "throttled",
            "search limit"
        ]
        
        html_lower = html_content.lower()
        
        # Check for rate limit indicators
        for indicator in rate_limit_indicators:
            if indicator in html_lower:
                return True
        
        # Check for common rate limit response patterns
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Look for error messages
        error_elements = soup.select(".error-msg") or soup.select(".alert-danger") or soup.select(".message-error")
        if error_elements:
            error_text = " ".join([el.get_text().lower() for el in error_elements])
            for indicator in rate_limit_indicators:
                if indicator in error_text:
                    return True
        
        return False

    def extract_engines_used(self, html_content: str) -> List[str]:
        """Extract which engines were used from the SearXNG results page."""
        engines = []
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Look for engine information in the results
            engine_elements = soup.select(".engines") or soup.select(".engine-info")
            
            if engine_elements:
                for element in engine_elements:
                    engine_text = element.get_text(strip=True)
                    engines.extend([e.strip() for e in engine_text.split(',')])
            
            # Remove duplicates and empty strings
            engines = list(set([e for e in engines if e]))
            
            return engines
        except Exception:
            return []

    def extract_html_results(self, html_content: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Extract search results from SearXNG HTML response."""
        results = []
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Find result elements - adjust selectors based on your SearXNG theme
            result_elements = soup.select(".result")
            if not result_elements:
                # Try alternative selectors for different SearXNG themes
                result_elements = soup.select(".result-default")
            if not result_elements:
                result_elements = soup.select(".result-item")
            
            # Process each result
            for i, result in enumerate(result_elements):
                if i >= max_results:
                    break
                
                # Extract title
                title_elem = result.select_one(".result-title") or result.select_one("h3")
                title = title_elem.get_text(strip=True) if title_elem else "No title"
                
                # Extract URL
                url_elem = result.select_one(".result-url") or title_elem.find("a") if title_elem else None
                url = url_elem.get("href") if url_elem and url_elem.get("href") else "#"
                
                # Extract content
                content_elem = result.select_one(".result-content") or result.select_one(".content")
                content = content_elem.get_text(strip=True) if content_elem else "No description available"
                
                # Clean up content
                content = self.format_text(content)
                
                # Add to results
                results.append({
                    "title": title,
                    "url": url,
                    "content": content
                })
            
            # If no results found with standard selectors, try a more generic approach
            if not results:
                # Look for any links with surrounding text
                links = soup.find_all("a")
                for i, link in enumerate(links):
                    if i >= max_results:
                        break
                    
                    # Skip if it's a navigation link or doesn't have href
                    if not link.get("href") or link.get("href").startswith("#"):
                        continue
                    
                    title = link.get_text(strip=True) or "Link"
                    url = link.get("href")
                    
                    # Get surrounding paragraph or div text
                    parent = link.find_parent(["p", "div"])
                    content = parent.get_text(strip=True) if parent else ""
                    content = content.replace(title, "")  # Remove title from content
                    
                    # Clean up content
                    content = self.format_text(content)
                    
                    results.append({
                        "title": title,
                        "url": url,
                        "content": content[:150] + "..." if len(content) > 150 else content
                    })
            
            return results
            
        except Exception as e:
            print(f"Error extracting HTML results: {str(e)}")
            return []

    def extract_json_results(self, json_data: Dict[str, Any], max_results: int = 5) -> List[Dict[str, str]]:
        """Extract search results from SearXNG JSON response."""
        results = []
        try:
            # Check if there's an error in the JSON response
            if "error" in json_data:
                print(f"Error in JSON response: {json_data['error']}")
                return []
            
            # Get results from the JSON data
            json_results = json_data.get("results", [])
            
            # Process each result
            for i, result in enumerate(json_results):
                if i >= max_results:
                    break
                
                title = result.get("title", "No title")
                url = result.get("url", "#")
                content = result.get("content", "")
                
                # If no content, try to use snippet or description
                if not content:
                    content = result.get("snippet", result.get("description", "No description available"))
                
                # Clean up content
                content = self.format_text(content)
                
                # Add to results
                results.append({
                    "title": title,
                    "url": url,
                    "content": content
                })
            
            return results
            
        except Exception as e:
            print(f"Error extracting JSON results: {str(e)}")
            return []

    def format_text(self, text: str) -> str:
        """Format and sanitize text content."""
        if not text:
            return ""
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
