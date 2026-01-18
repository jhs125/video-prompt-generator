import json
from textwrap import dedent


def build_prompt_from_video(v):
    """
    Turn one row of your viral video data into a detailed
    text prompt for recreating a similar-style video.
    """
    title = v.get("Video Title", "").strip()
    url = v.get("Video URL", "").strip()
    niche = v.get("Niche", "").strip()
    keyword = v.get("Keyword", "").strip()
    idea_angle = v.get("Idea Angle", "").strip()
    duration_sec = v.get("Duration (sec)", 15)
    tags = v.get("Tags", "")
    description = v.get("Description", "").strip()
    views = v.get("Views", 0)
    engagement_rate = v.get("Engagement Rate (%)", 0)

    # Basic guess for hook style based on title / keyword
    hook_theme = ""
    if "mindset" in title.lower() or "mindset" in keyword.lower():
        hook_theme = "rich vs poor mindset and money psychology"
    elif "habits" in title.lower():
        hook_theme = "1% millionaire habits and daily routines"
    elif "stock" in title.lower() or "trading" in title.lower():
        hook_theme = "trading discipline, patience and long-term wealth"
    elif "ramsey" in title.lower() or "buffet" in title.lower():
        hook_theme = "celebrity money lessons in a 1-line hook"
    elif "business idea" in title.lower():
        hook_theme = "simple visual business idea that looks premium"
    else:
        hook_theme = "short, punchy money-success motivation"

    base_prompt = f"""
    You are scripting a YouTube Short in the niche:
    "{niche}" (keyword focus: "{keyword}").

    Your job:
    Recreate the *format, pacing and emotional tone* of this viral video:
    - Title: {title}
    - URL (for reference only, do NOT copy): {url}
    - Duration: ~{duration_sec} seconds
    - Views: {views:,} | Engagement: {engagement_rate}%
    - Tags (original): {tags if tags else "[none provided]"}
    - Idea Angle: {idea_angle}

    GOAL:
    - Keep the *structure* and *energy* similar.
    - CHANGE the story, examples, and wording completely.
    - Do NOT copy or closely paraphrase the original.
    - Focus on: {hook_theme}.

    SCRIPT REQUIREMENTS:
    1. Format:
       - Write as a script with *very short lines* suitable for subtitles.
       - Use 1–2 short sentences per beat (max ~8–10 words per line).
       - Total length should fit a {duration_sec}-second Short (approx. 40–60 words for 6–10s; 80–120 for 30–50s).

    2. Structure:
       A) HOOK (0–2s):
          - Start with a scroll-stopping line directly about wealth/money:
            Example styles (adapt, don't copy):
            - "This is why most people never get rich."
            - "Poor mindset vs rich mindset in 5 seconds."
            - "Only 1% of people do this with their money."
       B) VALUE (middle):
          - 2–4 quick, punchy points or contrasts.
          - Use simple language, direct "you" framing.
          - Focus on behavior, habits, or mindset—NOT generic quotes.
       C) CTA (last 1–2s):
          - Soft call to action:
            - "Follow for daily money stories."
            - "Save this before you forget."
            - "Watch again if it hit you."

    3. Style:
       - Conversational, clear, no complex jargon.
       - Make it feel like a quick reality check.
       - Stay under 5th–8th grade reading level where possible.
       - Do not mention YouTube, 'this video', or timestamps.

    4. Visual Hints (in brackets):
       - Add simple visual suggestions like:
         [Text on screen: Poor vs Rich Mindset]
         [B-roll: counting cash, city skyline, notebook]
         Keep them minimal (1 every 2–3 lines max).

    5. Compliance:
       - No medical, legal, or financial guarantees.
       - No get-rich-quick claims.
       - No direct copying from the original description:
         {description[:250] + ("..." if len(description) > 250 else "")}

    OUTPUT:
    - Return ONLY the final short-form script with inline visual hints.
    - Do NOT include analysis or explanation.
    """

    return dedent(base_prompt).strip()