"""Main CrewAI workflow for founder scouting."""

from typing import Dict, Any
from crewai import Crew, Task, Process
from pydantic import BaseModel

from ..agents import ScoutAgents


class FounderProfile(BaseModel):
    """Structured output for founder evaluation."""
    founder_name: str
    company_name: str | None = None
    background_summary: str
    social_media_analysis: str
    market_presence_analysis: str
    overall_score: float  # 0-10 scale
    strengths: list[str]
    concerns: list[str]
    recommendation: str
    detailed_rationale: str


class FounderScoutCrew:
    """Multi-agent crew for comprehensive founder evaluation."""
    
    def __init__(self):
        """Initialize the scout crew with all specialized agents."""
        self.agents = ScoutAgents()
    
    def create_research_task(self, founder_info: str) -> Task:
        """Create task for researching founder background."""
        return Task(
            description=(
                f"Research the following founder: {founder_info}\n\n"
                "Your task is to:\n"
                "1. Find and analyze their LinkedIn profile for education, work history, and achievements\n"
                "2. Search for news articles and press mentions about them\n"
                "3. Look for any previous ventures, exits, or notable accomplishments\n"
                "4. Assess their professional credentials and track record\n"
                "5. Identify any red flags or concerns in their background\n\n"
                "Provide a comprehensive summary of your findings with specific examples and sources."
            ),
            expected_output=(
                "A detailed research report covering the founder's background, education, "
                "work experience, previous ventures, achievements, and any concerns. "
                "Include specific URLs and quotes from sources."
            ),
            agent=self.agents.research_agent(),
        )
    
    def create_social_media_task(self, founder_info: str) -> Task:
        """Create task for analyzing social media presence."""
        return Task(
            description=(
                f"Analyze the social media presence of: {founder_info}\n\n"
                "Your task is to:\n"
                "1. Search for their Twitter/X profile and analyze recent activity\n"
                "2. Assess their thought leadership and technical expertise based on tweets\n"
                "3. Evaluate their engagement level and influence in their community\n"
                "4. Check their LinkedIn for professional updates and network\n"
                "5. Identify their communication style and ability to build an audience\n"
                "6. Look for any controversial statements or red flags\n\n"
                "Provide insights on their social proof and online influence."
            ),
            expected_output=(
                "A comprehensive analysis of the founder's social media presence, "
                "including their thought leadership, engagement metrics, influence level, "
                "and any notable patterns or concerns. Include specific examples of their posts."
            ),
            agent=self.agents.social_media_analyst(),
        )
    
    def create_market_analysis_task(self, founder_info: str) -> Task:
        """Create task for analyzing market presence and media coverage."""
        return Task(
            description=(
                f"Analyze the market presence and media coverage of: {founder_info}\n\n"
                "Your task is to:\n"
                "1. Search for recent news articles and press coverage\n"
                "2. Identify any funding announcements or major milestones\n"
                "3. Assess their visibility and recognition in their industry\n"
                "4. Look for speaking engagements, podcast appearances, or interviews\n"
                "5. Evaluate their company's market traction (if applicable)\n"
                "6. Identify momentum indicators and growth signals\n\n"
                "Provide insights on their market position and media presence."
            ),
            expected_output=(
                "A detailed analysis of the founder's market presence, media coverage, "
                "industry recognition, and momentum indicators. Include specific articles, "
                "funding amounts, and measurable traction metrics."
            ),
            agent=self.agents.market_analyst(),
        )
    
    def create_scoring_task(self) -> Task:
        """Create task for synthesizing findings and scoring the founder."""
        return Task(
            description=(
                "Based on all the research gathered by the team, evaluate this founder "
                "for potential investment.\n\n"
                "Your task is to:\n"
                "1. Synthesize findings from background research, social media analysis, and market analysis\n"
                "2. Score the founder on a 0-10 scale based on:\n"
                "   - Background & Experience (0-2 points)\n"
                "   - Social Proof & Influence (0-2 points)\n"
                "   - Market Traction & Media Presence (0-2 points)\n"
                "   - Technical/Domain Expertise (0-2 points)\n"
                "   - Execution & Leadership Signals (0-2 points)\n"
                "3. List key strengths (top 3-5 positive indicators)\n"
                "4. List concerns or red flags (if any)\n"
                "5. Provide a clear recommendation: 'Strong Pursue', 'Pursue', 'Monitor', or 'Pass'\n"
                "6. Write detailed rationale explaining the score and recommendation\n\n"
                "Be objective, data-driven, and specific in your evaluation."
            ),
            expected_output=(
                "A structured founder evaluation report containing:\n"
                "- Overall score (0-10) with breakdown by category\n"
                "- Top 3-5 key strengths with specific examples\n"
                "- Any concerns or red flags\n"
                "- Clear recommendation (Strong Pursue/Pursue/Monitor/Pass)\n"
                "- Detailed rationale (3-4 paragraphs) explaining the assessment\n"
                "- Next steps or due diligence recommendations"
            ),
            agent=self.agents.scoring_agent(),
        )
    
    def scout_founder(self, founder_info: str) -> str:
        """
        Execute the complete founder scouting workflow.
        
        Args:
            founder_info: Information about the founder (name, company, etc.)
            
        Returns:
            Comprehensive evaluation report
        """
        # Create all tasks
        research_task = self.create_research_task(founder_info)
        social_media_task = self.create_social_media_task(founder_info)
        market_task = self.create_market_analysis_task(founder_info)
        scoring_task = self.create_scoring_task()
        
        # Set up task dependencies
        scoring_task.context = [research_task, social_media_task, market_task]
        
        # Create the crew
        crew = Crew(
            agents=[
                self.agents.research_agent(),
                self.agents.social_media_analyst(),
                self.agents.market_analyst(),
                self.agents.scoring_agent(),
            ],
            tasks=[
                research_task,
                social_media_task,
                market_task,
                scoring_task,
            ],
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
        )
        
        # Execute the workflow
        result = crew.kickoff()
        
        return result
    
    def scout_multiple_founders(self, founders_list: list[str]) -> Dict[str, Any]:
        """
        Scout multiple founders and return comparative analysis.
        
        Args:
            founders_list: List of founder information strings
            
        Returns:
            Dictionary with individual reports and comparative analysis
        """
        results = {}
        
        for founder_info in founders_list:
            print(f"\n{'='*80}")
            print(f"Scouting: {founder_info}")
            print(f"{'='*80}\n")
            
            result = self.scout_founder(founder_info)
            results[founder_info] = result
        
        return results
