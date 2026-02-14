"""Wellness & Mental Health Tool - Mood tracking, journaling, stress management."""
import json
import logging
import os
import random
from datetime import datetime

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
MOOD_FILE = os.path.join(DATA_DIR, "mood_log.json")
JOURNAL_FILE = os.path.join(DATA_DIR, "journal.json")

VALID_MOODS = ["great", "good", "okay", "low", "stressed", "anxious", "sad", "angry", "tired"]

MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "It's going to be hard, but hard does not mean impossible.",
    "Don't wait for opportunity. Create it.",
    "Sometimes we're tested not to show our weaknesses, but to discover our strengths.",
    "The key to success is to focus on goals, not obstacles.",
    "Dream bigger. Do bigger.",
    "You don't have to be perfect to be amazing.",
    "Discipline is choosing between what you want now and what you want most.",
    "Small progress is still progress.",
]

AFFIRMATIONS = [
    "I am capable of achieving my goals.",
    "I deserve success and happiness.",
    "I am growing stronger every single day.",
    "My potential is limitless.",
    "I choose to focus on what I can control.",
    "I am worthy of good things happening to me.",
    "Challenges help me grow and become better.",
    "I trust the process and my journey.",
    "I am enough, just as I am right now.",
    "Today I choose joy and gratitude.",
]

BREATHING_EXERCISES = {
    "4-7-8 Relaxing Breath": (
        "1. Breathe IN through your nose for 4 seconds\n"
        "2. HOLD your breath for 7 seconds\n"
        "3. Breathe OUT through your mouth for 8 seconds\n"
        "4. Repeat 3-4 times\n\n"
        "This activates your parasympathetic nervous system and calms anxiety."
    ),
    "Box Breathing (Navy SEAL technique)": (
        "1. Breathe IN for 4 seconds\n"
        "2. HOLD for 4 seconds\n"
        "3. Breathe OUT for 4 seconds\n"
        "4. HOLD for 4 seconds\n"
        "5. Repeat 4-5 times\n\n"
        "Used by special forces to stay calm under pressure."
    ),
    "5-5-5 Grounding": (
        "1. Breathe deeply and name 5 things you can SEE\n"
        "2. Name 4 things you can TOUCH\n"
        "3. Name 3 things you can HEAR\n"
        "4. Name 2 things you can SMELL\n"
        "5. Name 1 thing you can TASTE\n\n"
        "This grounds you in the present moment and reduces anxiety."
    ),
}

STRESS_TIPS = {
    "stressed": [
        "Take a 10-minute walk outside - movement reduces cortisol",
        "Write down 3 things you're grateful for right now",
        "Break your biggest task into tiny steps and do just the first one",
        "Listen to your favorite song and take deep breaths",
        "Talk to someone you trust about what's on your mind",
    ],
    "anxious": [
        "Try the 4-7-8 breathing technique (ask me for instructions)",
        "Write down your worries - getting them out of your head helps",
        "Focus only on the next 30 minutes, not the whole day",
        "Limit caffeine and social media for the rest of today",
        "Remember: anxiety lies. You've handled hard things before.",
    ],
    "sad": [
        "It's okay to feel sad. Don't fight it - acknowledge it",
        "Reach out to one person who makes you feel safe",
        "Do one small thing that usually brings you joy",
        "Go outside and get sunlight for at least 15 minutes",
        "Remember: bad days don't mean a bad life. This will pass.",
    ],
    "angry": [
        "Step away from the situation for at least 10 minutes",
        "Write down exactly what made you angry without filtering",
        "Do intense physical exercise to channel the energy",
        "Ask yourself: will this matter in 5 years?",
        "Practice the box breathing technique to cool down",
    ],
    "tired": [
        "Take a 20-minute power nap if possible (set an alarm!)",
        "Drink water - dehydration causes fatigue more than you'd think",
        "Step outside for fresh air and sunlight",
        "Prioritize only 1-2 essential tasks today - it's okay to rest",
        "Go to bed 1 hour earlier tonight. Sleep debt is real.",
    ],
}

JOURNAL_PROMPTS = [
    "What's one thing you accomplished today that you're proud of?",
    "What's something you're looking forward to this week?",
    "Write about a challenge you faced recently and what you learned.",
    "What are 3 things you're grateful for right now?",
    "If you could tell your future self one thing, what would it be?",
    "What's one habit you want to build and why?",
    "Describe your ideal day. What does it look like?",
    "What's something weighing on your mind? Write it all out.",
    "Who made a positive impact on your life recently?",
    "What would you do if you knew you couldn't fail?",
]


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> list:
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_json(filepath: str, data: list) -> None:
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def log_mood(mood: str, notes: str = "") -> str:
    """Log your current mood for tracking over time.

    Args:
        mood: How you're feeling. One of: great, good, okay, low,
            stressed, anxious, sad, angry, tired.
        notes: Optional notes about why you feel this way.

    Returns:
        Confirmation with personalized advice based on mood.
    """
    if not mood or not mood.strip():
        return f"Please tell me how you're feeling. Options: {', '.join(VALID_MOODS)}"

    mood = mood.strip().lower()
    if mood not in VALID_MOODS:
        return f"I don't recognize '{mood}'. Try one of: {', '.join(VALID_MOODS)}"

    entries = _load_json(MOOD_FILE)
    entry = {
        "mood": mood,
        "notes": notes.strip() if notes else "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    entries.append(entry)
    _save_json(MOOD_FILE, entries)

    # Build response
    lines = [f"Mood logged: {mood} ({entry['timestamp']})"]

    if mood in STRESS_TIPS:
        tips = STRESS_TIPS[mood]
        lines.append(f"\nI hear you. Here are some things that might help:\n")
        for i, tip in enumerate(random.sample(tips, min(3, len(tips))), 1):
            lines.append(f"  {i}. {tip}")

    if mood in ("great", "good"):
        lines.append(f"\nThat's wonderful! Keep riding this energy.")
        lines.append(f"Affirmation: {random.choice(AFFIRMATIONS)}")
    elif mood == "okay":
        lines.append(f"\nOkay is fine. Not every day needs to be amazing.")
        lines.append(f"Here's a thought: {random.choice(MOTIVATIONAL_QUOTES)}")

    # Show streak info
    today = datetime.now().strftime("%Y-%m-%d")
    dates_logged = sorted(set(e["date"] for e in entries))
    lines.append(f"\nMood tracking streak: {len(dates_logged)} days logged total")

    logger.info("Logged mood: %s", mood)
    return "\n".join(lines)


def get_mood_history(days: int = 7) -> str:
    """View your mood history over recent days.

    Args:
        days: Number of days to look back (default: 7).

    Returns:
        Formatted mood history with patterns and insights.
    """
    entries = _load_json(MOOD_FILE)
    if not entries:
        return "No mood entries yet. Use log_mood() to start tracking how you feel!"

    days = max(1, min(int(days), 90))

    # Filter to recent days
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e["date"] >= cutoff]

    if not recent:
        return f"No mood entries in the last {days} days."

    lines = [f"Mood History (last {days} days):\n"]

    # Group by date
    by_date = {}
    for e in recent:
        by_date.setdefault(e["date"], []).append(e)

    for date in sorted(by_date.keys(), reverse=True):
        day_entries = by_date[date]
        moods = ", ".join(e["mood"] for e in day_entries)
        notes = [e["notes"] for e in day_entries if e.get("notes")]
        note_str = f" - {'; '.join(notes)}" if notes else ""
        lines.append(f"  {date}: {moods}{note_str}")

    # Mood distribution
    mood_counts = {}
    for e in recent:
        mood_counts[e["mood"]] = mood_counts.get(e["mood"], 0) + 1

    lines.append(f"\nMood breakdown:")
    for mood, count in sorted(mood_counts.items(), key=lambda x: -x[1]):
        bar = "#" * count
        lines.append(f"  {mood:10s} {bar} ({count})")

    # Insight
    most_common = max(mood_counts, key=mood_counts.get)
    positive = sum(mood_counts.get(m, 0) for m in ("great", "good"))
    negative = sum(mood_counts.get(m, 0) for m in ("sad", "angry", "stressed", "anxious"))
    total = len(recent)

    if positive > negative:
        lines.append(f"\nOverall: You've been mostly positive! Keep it up.")
    elif negative > positive:
        lines.append(f"\nOverall: It's been a tough stretch. Be kind to yourself.")
    else:
        lines.append(f"\nOverall: Mixed feelings are normal. You're doing fine.")

    return "\n".join(lines)


def get_motivation() -> str:
    """Get a motivational quote and positive affirmation to boost your energy.

    Returns:
        A random motivational quote with an affirmation.
    """
    quote = random.choice(MOTIVATIONAL_QUOTES)
    affirmation = random.choice(AFFIRMATIONS)

    return (
        f"**Today's Motivation:**\n"
        f'"{quote}"\n\n'
        f"**Affirmation for you:**\n"
        f"{affirmation}\n\n"
        f"Say the affirmation out loud. It rewires your brain over time."
    )


def get_breathing_exercise(exercise_type: str = "calm") -> str:
    """Get a guided breathing exercise for stress relief.

    Args:
        exercise_type: Type of exercise - "calm" for relaxation,
            "focus" for concentration, "ground" for anxiety relief.

    Returns:
        Step-by-step breathing exercise instructions.
    """
    exercise_type = exercise_type.strip().lower() if exercise_type else "calm"

    if exercise_type in ("calm", "relax", "sleep"):
        name = "4-7-8 Relaxing Breath"
    elif exercise_type in ("focus", "concentrate", "energy"):
        name = "Box Breathing (Navy SEAL technique)"
    elif exercise_type in ("ground", "anxiety", "panic"):
        name = "5-5-5 Grounding"
    else:
        name = random.choice(list(BREATHING_EXERCISES.keys()))

    instructions = BREATHING_EXERCISES[name]
    return f"**{name}**\n\n{instructions}\nTake your time. There's no rush."


def journal_entry(entry: str = "", get_prompt: bool = False) -> str:
    """Write a journal entry or get a journaling prompt.

    Args:
        entry: Your journal entry text. Leave empty to get a writing prompt.
        get_prompt: Set to True to get a journaling prompt instead of writing.

    Returns:
        Confirmation of saved entry or a journaling prompt.
    """
    if get_prompt or not entry or not entry.strip():
        prompt = random.choice(JOURNAL_PROMPTS)
        return (
            f"**Journal Prompt:**\n"
            f"{prompt}\n\n"
            f"Take 5-10 minutes to write your thoughts. "
            f"Call journal_entry() with your text when ready."
        )

    entries = _load_json(JOURNAL_FILE)
    journal = {
        "entry": entry.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "word_count": len(entry.strip().split()),
    }
    entries.append(journal)
    _save_json(JOURNAL_FILE, entries)

    total = len(entries)
    total_words = sum(e.get("word_count", 0) for e in entries)

    return (
        f"Journal entry saved! ({journal['timestamp']})\n"
        f"Words: {journal['word_count']}\n"
        f"Total entries: {total} | Total words written: {total_words}\n\n"
        f"Writing is therapy. Great job taking time for yourself."
    )


def weekly_checkin() -> str:
    """Get a comprehensive weekly mental health check-in summary.

    Returns:
        Weekly wellness summary with mood trends, journal activity,
        and personalized recommendations.
    """
    from datetime import timedelta

    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Mood data
    moods = _load_json(MOOD_FILE)
    recent_moods = [m for m in moods if m["date"] >= cutoff]

    # Journal data
    journals = _load_json(JOURNAL_FILE)
    recent_journals = [j for j in journals if j["date"] >= cutoff]

    lines = ["**Weekly Wellness Check-In**\n"]
    lines.append(f"Period: {cutoff} to {datetime.now().strftime('%Y-%m-%d')}\n")

    # Mood summary
    if recent_moods:
        mood_counts = {}
        for m in recent_moods:
            mood_counts[m["mood"]] = mood_counts.get(m["mood"], 0) + 1

        dominant = max(mood_counts, key=mood_counts.get)
        lines.append(f"**Mood Summary:** {len(recent_moods)} entries logged")
        for mood, count in sorted(mood_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  - {mood}: {count} times")
        lines.append(f"  Dominant mood: {dominant}")

        positive = sum(mood_counts.get(m, 0) for m in ("great", "good"))
        negative = sum(mood_counts.get(m, 0) for m in ("sad", "angry", "stressed", "anxious"))

        if positive > negative:
            lines.append("  Trend: Positive week overall!")
        elif negative > positive:
            lines.append("  Trend: Rough week. Consider talking to someone you trust.")
        else:
            lines.append("  Trend: Balanced week.")
    else:
        lines.append("**Mood:** No mood entries this week. Try logging daily!")

    lines.append("")

    # Journal summary
    if recent_journals:
        total_words = sum(j.get("word_count", 0) for j in recent_journals)
        lines.append(f"**Journal:** {len(recent_journals)} entries, {total_words} words written")
    else:
        lines.append("**Journal:** No entries this week. Even 5 minutes helps!")

    lines.append("")

    # Recommendations
    lines.append("**This Week's Recommendations:**")
    lines.append(f"  1. {random.choice(MOTIVATIONAL_QUOTES)}")
    lines.append(f"  2. Try a breathing exercise when you feel overwhelmed")
    lines.append(f"  3. Write in your journal at least 3 times this week")
    lines.append(f"  4. Get outside for at least 20 minutes of sunlight daily")
    lines.append(f"  5. Celebrate one win from this week, no matter how small")

    return "\n".join(lines)
