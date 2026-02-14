"""Career Tools - DSA roadmaps, resume tips, and portfolio ideas."""
import logging

logger = logging.getLogger(__name__)

# --- DSA topics pool organized by difficulty ---
DSA_TOPICS = [
    {"topic": "Arrays & Strings", "difficulty": "Easy", "problems": 15},
    {"topic": "Hashing & Two Pointers", "difficulty": "Easy", "problems": 10},
    {"topic": "Linked Lists", "difficulty": "Easy-Medium", "problems": 10},
    {"topic": "Stacks & Queues", "difficulty": "Medium", "problems": 10},
    {"topic": "Recursion & Backtracking", "difficulty": "Medium", "problems": 12},
    {"topic": "Binary Trees & BST", "difficulty": "Medium", "problems": 15},
    {"topic": "Graphs (BFS/DFS)", "difficulty": "Medium-Hard", "problems": 15},
    {"topic": "Dynamic Programming (1D)", "difficulty": "Medium-Hard", "problems": 15},
    {"topic": "Dynamic Programming (2D)", "difficulty": "Hard", "problems": 10},
    {"topic": "Greedy Algorithms", "difficulty": "Medium", "problems": 10},
    {"topic": "Heaps & Priority Queues", "difficulty": "Medium", "problems": 8},
    {"topic": "Tries & Segment Trees", "difficulty": "Hard", "problems": 8},
    {"topic": "Sliding Window & Intervals", "difficulty": "Medium", "problems": 10},
    {"topic": "Bit Manipulation", "difficulty": "Medium", "problems": 6},
    {"topic": "Mixed Practice & Mock Interviews", "difficulty": "Mixed", "problems": 20},
]


def get_dsa_roadmap(weeks: int = 4) -> str:
    """Generate a structured DSA study roadmap based on available weeks.

    Args:
        weeks: Number of weeks for the study plan (1-16). Default is 4.

    Returns:
        A formatted weekly DSA study plan as a string.
    """
    if not isinstance(weeks, (int, float)):
        return "Error: 'weeks' must be a number between 1 and 16."

    weeks = max(1, min(int(weeks), 16))
    topics = DSA_TOPICS[:]
    total_topics = len(topics)

    # Distribute topics across weeks
    topics_per_week = max(1, total_topics // weeks)
    plan_lines = []

    for week_num in range(1, weeks + 1):
        start = (week_num - 1) * topics_per_week
        end = start + topics_per_week if week_num < weeks else total_topics
        week_topics = topics[start:end]

        if not week_topics:
            break

        topic_names = ", ".join(t["topic"] for t in week_topics)
        total_problems = sum(t["problems"] for t in week_topics)
        plan_lines.append(
            f"Week {week_num}: {topic_names} (~{total_problems} problems)"
        )

    tip = (
        "Tip: Focus on understanding patterns, not memorizing solutions. "
        "Practice on LeetCode, Codeforces, or GeeksforGeeks."
    )
    plan_lines.append(f"\n{tip}")

    logger.info("Generated %d-week DSA roadmap", weeks)
    return "\n".join(plan_lines)


# --- Resume tips organized by category ---
RESUME_TIPS = {
    "format": [
        "Keep your resume to 1 page (2 max for 10+ years experience)",
        "Use a clean, ATS-friendly template with consistent formatting",
        "Use reverse chronological order for experience",
        "Save as PDF to preserve formatting across devices",
    ],
    "content": [
        "Quantify achievements with numbers (e.g., 'Reduced load time by 40%')",
        "Use strong action verbs: Built, Designed, Optimized, Led, Shipped",
        "Mirror keywords from the job description in your resume",
        "Include a concise professional summary (2-3 lines) at the top",
        "List relevant technical skills grouped by category",
    ],
    "mistakes_to_avoid": [
        "Don't include a photo, age, or marital status",
        "Remove outdated skills (e.g., jQuery if applying for React roles)",
        "Avoid generic statements like 'team player' without evidence",
        "Don't list every technology - focus on what's relevant to the role",
    ],
}


def get_resume_tips() -> str:
    """Get comprehensive, categorized resume tips for tech professionals.

    Returns:
        Formatted resume tips organized by category.
    """
    lines = []
    for category, tips in RESUME_TIPS.items():
        header = category.replace("_", " ").title()
        lines.append(f"\n**{header}:**")
        for i, tip in enumerate(tips, 1):
            lines.append(f"  {i}. {tip}")

    logger.info("Returned resume tips")
    return "\n".join(lines)


# --- Portfolio ideas by tech stack ---
PORTFOLIO_IDEAS = {
    "python": [
        "Full-stack web app with FastAPI + React (e.g., expense tracker)",
        "Web scraper with data visualization dashboard using Streamlit",
        "CLI tool for automating daily tasks (file organizer, email sender)",
        "REST API with authentication, rate limiting, and database (PostgreSQL)",
        "Machine learning project: sentiment analysis or price predictor",
    ],
    "javascript": [
        "Real-time chat app with Socket.io and React",
        "E-commerce storefront with Next.js and Stripe integration",
        "Browser extension for productivity (tab manager, bookmark organizer)",
        "Full-stack MERN app with auth (blog platform, task manager)",
        "Interactive data dashboard with D3.js or Chart.js",
    ],
    "java": [
        "Spring Boot microservices project with Docker",
        "Android app with Room database and Retrofit",
        "Banking system simulation with design patterns",
        "RESTful API with Spring Security and JWT authentication",
        "Distributed system with message queues (RabbitMQ/Kafka)",
    ],
    "default": [
        "Personal portfolio website with project showcase",
        "REST API with CRUD operations and database",
        "CLI automation tool for a repetitive task",
        "Real-time application (chat, notifications, live dashboard)",
        "Open-source contribution to a popular project on GitHub",
    ],
}


def get_portfolio_ideas(tech: str = "Python") -> str:
    """Get portfolio project ideas tailored to a specific technology stack.

    Args:
        tech: The technology or programming language (e.g., "Python", "JavaScript").

    Returns:
        A formatted list of portfolio project ideas.
    """
    if not tech or not tech.strip():
        tech = "Python"

    tech = tech.strip()
    key = tech.lower()
    ideas = PORTFOLIO_IDEAS.get(key, PORTFOLIO_IDEAS["default"])

    lines = [f"Portfolio project ideas for {tech}:\n"]
    for i, idea in enumerate(ideas, 1):
        lines.append(f"  {i}. {idea}")

    lines.append(
        f"\nTip: Pick ONE project, build it end-to-end, deploy it, "
        f"and write about what you learned. Quality > quantity."
    )

    logger.info("Generated portfolio ideas for '%s'", tech)
    return "\n".join(lines)
