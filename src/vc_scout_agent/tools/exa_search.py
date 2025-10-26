"""Exa search tools for gathering founder intelligence."""

from datetime import datetime, timedelta
from typing import Any

from exa_py import Exa
from crewai.tools import BaseTool
from pydantic import Field

from ..config import settings


class ExaTwitterSearchTool(BaseTool):
    """Search Twitter/X for founder activity and engagement."""
    
    name: str = "exa_twitter_search"
    description: str = (
        "Search Twitter/X for information about founders, their tweets, engagement, "
        "and public presence. Use this to assess founder's thought leadership, "
        "community engagement, and social proof."
    )
    exa_client: Exa = Field(default_factory=lambda: Exa(api_key=settings.exa_api_key))
    
    def _run(self, query: str, num_results: int = 10) -> str:
        """Execute Twitter search via Exa.
        
        Args:
            query: Search query about the founder
            num_results: Number of results to return
            
        Returns:
            Formatted search results with Twitter content
        """
        try:
            # Use Exa's neural search with Twitter domain filter
            start_date = datetime.now() - timedelta(days=settings.search_days_back)
            
            results = self.exa_client.search_and_contents(
                query=f"{query} site:twitter.com OR site:x.com",
                type="neural",
                num_results=min(num_results, settings.max_search_results),
                start_published_date=start_date.strftime("%Y-%m-%d"),
                text=True,
                highlights=True
            )
            
            if not results.results:
                return f"No Twitter results found for: {query}"
            
            formatted_results = []
            for idx, result in enumerate(results.results, 1):
                formatted_results.append(
                    f"\n--- Result {idx} ---\n"
                    f"URL: {result.url}\n"
                    f"Title: {result.title}\n"
                    f"Published: {result.published_date}\n"
                    f"Content: {result.text[:500] if result.text else 'N/A'}...\n"
                    f"Highlights: {result.highlights if hasattr(result, 'highlights') else 'N/A'}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error searching Twitter: {str(e)}"


class ExaLinkedInSearchTool(BaseTool):
    """Search LinkedIn for founder profiles and professional background."""
    
    name: str = "exa_linkedin_search"
    description: str = (
        "Search LinkedIn for founder profiles, work history, education, "
        "and professional achievements. Use this to assess founder credentials, "
        "network, and career trajectory."
    )
    exa_client: Exa = Field(default_factory=lambda: Exa(api_key=settings.exa_api_key))
    
    def _run(self, query: str, num_results: int = 10) -> str:
        """Execute LinkedIn search via Exa.
        
        Args:
            query: Search query about the founder
            num_results: Number of results to return
            
        Returns:
            Formatted search results with LinkedIn content
        """
        try:
            results = self.exa_client.search_and_contents(
                query=f"{query} site:linkedin.com/in",
                type="neural",
                num_results=min(num_results, settings.max_search_results),
                text=True,
                highlights=True
            )
            
            if not results.results:
                return f"No LinkedIn results found for: {query}"
            
            formatted_results = []
            for idx, result in enumerate(results.results, 1):
                formatted_results.append(
                    f"\n--- Result {idx} ---\n"
                    f"URL: {result.url}\n"
                    f"Title: {result.title}\n"
                    f"Content: {result.text[:500] if result.text else 'N/A'}...\n"
                    f"Highlights: {result.highlights if hasattr(result, 'highlights') else 'N/A'}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error searching LinkedIn: {str(e)}"


class ExaGeneralWebSearchTool(BaseTool):
    """Search the web for founder mentions, articles, and press coverage."""
    
    name: str = "exa_web_search"
    description: str = (
        "Search the general web for founder information including news articles, "
        "blog posts, interviews, press releases, and any other public content. "
        "Use this for comprehensive background research."
    )
    exa_client: Exa = Field(default_factory=lambda: Exa(api_key=settings.exa_api_key))
    
    def _run(self, query: str, num_results: int = 15) -> str:
        """Execute general web search via Exa.
        
        Args:
            query: Search query about the founder
            num_results: Number of results to return
            
        Returns:
            Formatted search results from across the web
        """
        try:
            start_date = datetime.now() - timedelta(days=settings.search_days_back)
            
            results = self.exa_client.search_and_contents(
                query=query,
                type="neural",
                num_results=min(num_results, settings.max_search_results * 2),
                start_published_date=start_date.strftime("%Y-%m-%d"),
                text=True,
                highlights=True
            )
            
            if not results.results:
                return f"No web results found for: {query}"
            
            formatted_results = []
            for idx, result in enumerate(results.results, 1):
                formatted_results.append(
                    f"\n--- Result {idx} ---\n"
                    f"URL: {result.url}\n"
                    f"Title: {result.title}\n"
                    f"Published: {result.published_date}\n"
                    f"Content: {result.text[:500] if result.text else 'N/A'}...\n"
                    f"Highlights: {result.highlights if hasattr(result, 'highlights') else 'N/A'}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error in web search: {str(e)}"


class ExaFounderNewsSearchTool(BaseTool):
    """Search for recent news and media coverage about founders."""
    
    name: str = "exa_founder_news_search"
    description: str = (
        "Search for recent news articles, press releases, and media coverage "
        "about founders and their companies. Use this to find latest developments, "
        "funding announcements, and media attention."
    )
    exa_client: Exa = Field(default_factory=lambda: Exa(api_key=settings.exa_api_key))
    
    def _run(self, query: str, num_results: int = 10) -> str:
        """Execute news search via Exa.
        
        Args:
            query: Search query about the founder or company
            num_results: Number of results to return
            
        Returns:
            Formatted news results
        """
        try:
            # Focus on news sites and recent publications
            start_date = datetime.now() - timedelta(days=settings.search_days_back)
            
            news_sites = [
                "techcrunch.com", "theinformation.com", "bloomberg.com",
                "reuters.com", "wsj.com", "forbes.com", "fortune.com"
            ]
            
            site_filter = " OR ".join([f"site:{site}" for site in news_sites])
            
            results = self.exa_client.search_and_contents(
                query=f"{query} ({site_filter})",
                type="neural",
                num_results=min(num_results, settings.max_search_results),
                start_published_date=start_date.strftime("%Y-%m-%d"),
                text=True,
                highlights=True
            )
            
            if not results.results:
                return f"No news results found for: {query}"
            
            formatted_results = []
            for idx, result in enumerate(results.results, 1):
                formatted_results.append(
                    f"\n--- Result {idx} ---\n"
                    f"Source: {result.url}\n"
                    f"Title: {result.title}\n"
                    f"Published: {result.published_date}\n"
                    f"Content: {result.text[:500] if result.text else 'N/A'}...\n"
                    f"Highlights: {result.highlights if hasattr(result, 'highlights') else 'N/A'}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error searching news: {str(e)}"
