"""Agent definitions for the VC Scout multi-agent system."""

from crewai import Agent, LLM

from ..config import settings
from ..tools import (
    ExaTwitterSearchTool,
    ExaLinkedInSearchTool,
    ExaGeneralWebSearchTool,
    ExaFounderNewsSearchTool,
)


def get_llm():
    """Get the configured LLM instance via OpenRouter."""
    return LLM(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
    )


class ScoutAgents:
    """Collection of specialized agents for founder scouting."""
    
    @staticmethod
    def research_agent() -> Agent:
        """Agent specialized in deep research on founders and their background."""
        return Agent(
            role="Founder Research Specialist",
            goal=(
                "Conduct comprehensive research on founders to uncover their background, "
                "experience, achievements, and public presence across multiple sources."
            ),
            backstory=(
                "You are an expert researcher with years of experience in due diligence "
                "for venture capital firms. You have a keen eye for identifying promising "
                "founders by analyzing their career trajectory, education, previous ventures, "
                "and public reputation. You know how to dig deep into LinkedIn profiles, "
                "news articles, and web sources to build a complete picture of a founder's "
                "capabilities and track record."
            ),
            tools=[
                ExaLinkedInSearchTool(),
                ExaGeneralWebSearchTool(),
                ExaFounderNewsSearchTool(),
            ],
            llm=get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @staticmethod
    def social_media_analyst() -> Agent:
        """Agent specialized in analyzing social media presence and engagement."""
        return Agent(
            role="Social Media Intelligence Analyst",
            goal=(
                "Analyze founder's social media presence, thought leadership, "
                "community engagement, and influence on platforms like Twitter/X and LinkedIn."
            ),
            backstory=(
                "You are a social media intelligence expert who specializes in evaluating "
                "online presence and influence of startup founders. You understand that a "
                "founder's social media activity reveals their thought leadership, ability "
                "to build community, technical expertise, and market positioning. You excel "
                "at identifying authentic engagement, measuring influence, and spotting red flags "
                "or green flags in how founders present themselves and interact online. "
                "You pay special attention to Twitter/X for tech founders and LinkedIn for "
                "professional networking and credibility."
            ),
            tools=[
                ExaTwitterSearchTool(),
                ExaLinkedInSearchTool(),
            ],
            llm=get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @staticmethod
    def market_analyst() -> Agent:
        """Agent specialized in analyzing market presence and media coverage."""
        return Agent(
            role="Market & Media Analyst",
            goal=(
                "Assess founder's market presence, media coverage, industry recognition, "
                "and overall visibility in their sector."
            ),
            backstory=(
                "You are a market intelligence analyst with deep experience in the startup "
                "ecosystem. You track industry trends, media coverage, and market positioning "
                "of founders and their companies. You know how to interpret press coverage, "
                "funding announcements, and industry recognition to gauge a founder's market "
                "traction and reputation. You understand that media presence often correlates "
                "with fundraising success and can identify founders who are gaining momentum."
            ),
            tools=[
                ExaFounderNewsSearchTool(),
                ExaGeneralWebSearchTool(),
            ],
            llm=get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @staticmethod
    def scoring_agent() -> Agent:
        """Agent that synthesizes all research and provides investment recommendations."""
        return Agent(
            role="Founder Evaluation & Scoring Specialist",
            goal=(
                "Synthesize all research findings to evaluate founders and provide "
                "actionable investment recommendations with detailed scoring and rationale."
            ),
            backstory=(
                "You are a senior venture capital analyst with a proven track record of "
                "identifying successful founders before they become household names. You have "
                "developed a sophisticated framework for evaluating founder quality based on "
                "multiple dimensions: background & experience, social proof & influence, "
                "market traction & media presence, technical expertise, and execution capability. "
                "You excel at synthesizing diverse data points into clear, actionable "
                "recommendations. You provide structured scores with detailed justifications, "
                "highlighting both strengths and potential concerns. Your recommendations have "
                "helped your firm secure investments in multiple unicorn companies."
            ),
            tools=[],  # This agent synthesizes, doesn't search
            llm=get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @staticmethod
    def orchestrator_agent() -> Agent:
        """Main orchestrator agent that coordinates the entire scouting process."""
        return Agent(
            role="VC Scouting Orchestrator",
            goal=(
                "Coordinate a comprehensive founder evaluation by delegating research tasks "
                "to specialized agents and synthesizing their findings into actionable intelligence."
            ),
            backstory=(
                "You are the head of founder scouting at a top-tier venture capital firm. "
                "You have built a team of specialized analysts and know exactly how to "
                "orchestrate their work to efficiently evaluate potential founder investments. "
                "You understand that finding great founders requires looking at multiple angles: "
                "their professional background, social media influence, market presence, and "
                "overall execution capability. You coordinate the research process, ensure "
                "thorough coverage of all relevant aspects, and deliver comprehensive reports "
                "that help your partners make investment decisions."
            ),
            tools=[
                ExaTwitterSearchTool(),
                ExaLinkedInSearchTool(),
                ExaGeneralWebSearchTool(),
                ExaFounderNewsSearchTool(),
            ],
            llm=get_llm(),
            verbose=True,
            allow_delegation=True,
        )
