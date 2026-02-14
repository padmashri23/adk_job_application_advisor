"""Interview Preparation Tool - Technical and behavioral interview guidance."""
import logging

logger = logging.getLogger(__name__)

TECHNICAL_QUESTIONS = {
    "python": [
        "Explain the difference between a list and a tuple.",
        "What are Python decorators and when would you use them?",
        "How does Python's GIL affect multithreading?",
        "Explain generators and when to use them over lists.",
        "What is the difference between deepcopy and shallow copy?",
        "How do you handle memory leaks in Python?",
        "Explain Python's MRO (Method Resolution Order).",
        "What are context managers and how do you create one?",
    ],
    "javascript": [
        "Explain closures with an example.",
        "What is the event loop and how does it work?",
        "Difference between var, let, and const.",
        "How does prototypal inheritance work?",
        "Explain promises, async/await, and error handling.",
        "What is the difference between == and ===?",
        "How does the 'this' keyword work in different contexts?",
        "Explain Web Workers and when to use them.",
    ],
    "java": [
        "Explain the difference between abstract class and interface.",
        "How does garbage collection work in Java?",
        "What is the difference between HashMap and ConcurrentHashMap?",
        "Explain SOLID principles with examples.",
        "How does Java handle memory management (heap vs stack)?",
        "What are streams and functional interfaces in Java 8+?",
        "Explain the volatile keyword and its use cases.",
        "What is the difference between checked and unchecked exceptions?",
    ],
    "system_design": [
        "Design a URL shortener like bit.ly.",
        "Design a rate limiter for an API.",
        "How would you design a chat application like WhatsApp?",
        "Design a notification system for a large-scale app.",
        "How would you design a job queue system?",
        "Design a caching strategy for a high-traffic website.",
    ],
    "default": [
        "Explain RESTful API design principles.",
        "What is the difference between SQL and NoSQL databases?",
        "How does HTTPS work? Explain the TLS handshake.",
        "What are microservices and when should you use them?",
        "Explain CI/CD pipelines and their benefits.",
        "How would you optimize a slow database query?",
    ],
}

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you disagreed with a teammate. How did you handle it?",
    "Describe a project where you had to learn a new technology quickly.",
    "Tell me about a time you missed a deadline. What did you learn?",
    "How do you prioritize tasks when everything seems urgent?",
    "Describe a bug that took you a long time to find. How did you debug it?",
    "Tell me about a time you received critical feedback. How did you respond?",
    "Describe a situation where you had to explain a technical concept to a non-technical person.",
    "Tell me about your most challenging project and what made it difficult.",
]

STAR_METHOD = (
    "Use the STAR method for behavioral answers:\n"
    "  S - Situation: Set the scene and context\n"
    "  T - Task: Describe what you needed to accomplish\n"
    "  A - Action: Explain the specific steps YOU took\n"
    "  R - Result: Share the outcome with measurable impact"
)


def get_interview_questions(role: str = "software engineer", tech: str = "python") -> str:
    """Get curated interview questions for a specific role and tech stack.

    Args:
        role: The job role (e.g., "software engineer", "frontend developer").
        tech: The primary technology or language (e.g., "python", "javascript").

    Returns:
        A formatted list of technical and behavioral interview questions with tips.
    """
    if not role or not role.strip():
        role = "software engineer"
    if not tech or not tech.strip():
        tech = "python"

    tech = tech.strip().lower()
    role = role.strip()

    tech_qs = TECHNICAL_QUESTIONS.get(tech, TECHNICAL_QUESTIONS["default"])
    lines = [f"Interview prep for {role} ({tech.title()}):\n"]

    lines.append("**Technical Questions:**")
    for i, q in enumerate(tech_qs, 1):
        lines.append(f"  {i}. {q}")

    # Add system design for senior roles
    if any(word in role.lower() for word in ["senior", "lead", "staff", "architect"]):
        lines.append("\n**System Design Questions:**")
        for i, q in enumerate(TECHNICAL_QUESTIONS["system_design"], 1):
            lines.append(f"  {i}. {q}")

    lines.append("\n**Behavioral Questions:**")
    for i, q in enumerate(BEHAVIORAL_QUESTIONS[:5], 1):
        lines.append(f"  {i}. {q}")

    lines.append(f"\n**Answering Framework:**\n{STAR_METHOD}")

    lines.append(
        "\n**General Tips:**\n"
        "  - Research the company's tech stack and recent projects\n"
        "  - Prepare 2-3 questions to ask YOUR interviewer\n"
        "  - Practice coding on a whiteboard or shared editor\n"
        "  - Think out loud during technical questions"
    )

    logger.info("Generated interview prep for '%s' (%s)", role, tech)
    return "\n".join(lines)
