# VC Scout Agent 🎯

A fun weekend project that uses AI to scout founders like a VC analyst would.

## What it does

Give it a founder's name and company, and it will:
- Check their LinkedIn for background
- Read their tweets to see how they think
- Find news articles about them
- Give you a simple score (0-10) with reasons

## Quick Start (5 minutes)

1. **Get API keys** (free):
   - OpenRouter: [openrouter.ai/keys](https://openrouter.ai/keys)
   - Exa: [exa.ai](https://exa.ai)

2. **Setup**:
   ```bash
   cp .env.example .env
   # Add your keys to .env
   ```

3. **Try it**:
   ```bash
   uv run python quick_start.py
   ```

4. **Scout someone**:
   ```bash
   uv run python -m vc_scout_agent.main "Sam Altman, OpenAI"
   ```

## How it works

It's like having 4 AI interns:
- **Researcher** - digs into LinkedIn
- **Social Media Analyst** - reads tweets
- **Market Analyst** - finds news
- **Scorer** - gives you the final take

## Example Output

```
Sam Altman - OpenAI
Score: 8.5/10

Strengths:
- Founded successful companies before
- Strong Twitter presence (1M+ followers)
- Lots of recent press coverage

Concerns:
- High profile might mean expensive

Recommendation: Strong Pursue
```

## Fun things to try

- Scout your favorite startup founders
- Compare scores between founders
- See what the AI thinks of famous CEOs
- Test with fake names to see what happens

## Tech stuff (if you care)

Built with CrewAI + Exa search + GPT-5 Nano. Runs locally, costs about $0.02 per evaluation.

## License

MIT - do whatever you want with it!

P.s. this was vibecoded with WarpCLI and Cursor. If you're looking for something specific, please contact me (link in bio).
