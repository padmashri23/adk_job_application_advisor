"""Skill Gap Analysis Tool - Compare skills against job requirements."""
import logging

logger = logging.getLogger(__name__)

# Common skill requirements by role
ROLE_REQUIREMENTS = {
    "frontend developer": {
        "must_have": ["HTML", "CSS", "JavaScript", "React or Vue or Angular", "Git"],
        "good_to_have": ["TypeScript", "Testing (Jest/Cypress)", "Webpack/Vite", "REST APIs", "Responsive Design"],
        "bonus": ["Next.js/Nuxt.js", "GraphQL", "CI/CD", "Performance Optimization", "Accessibility (a11y)"],
    },
    "backend developer": {
        "must_have": ["Python or Java or Node.js", "SQL", "REST APIs", "Git", "Database Design"],
        "good_to_have": ["Docker", "Cloud (AWS/GCP/Azure)", "Redis/Caching", "Testing", "Message Queues"],
        "bonus": ["Kubernetes", "Microservices", "GraphQL", "CI/CD", "System Design"],
    },
    "full stack developer": {
        "must_have": ["HTML/CSS/JavaScript", "Backend Language (Python/Java/Node.js)", "SQL", "REST APIs", "Git"],
        "good_to_have": ["React or Vue", "Docker", "Cloud Basics", "Testing", "Authentication/Security"],
        "bonus": ["TypeScript", "CI/CD", "Kubernetes", "System Design", "DevOps"],
    },
    "data scientist": {
        "must_have": ["Python", "SQL", "Statistics", "Pandas/NumPy", "Machine Learning Basics"],
        "good_to_have": ["Scikit-learn", "Data Visualization", "Deep Learning", "Feature Engineering", "Git"],
        "bonus": ["MLOps", "Spark/Big Data", "Cloud ML Services", "A/B Testing", "NLP/CV"],
    },
    "devops engineer": {
        "must_have": ["Linux", "Docker", "CI/CD", "Cloud (AWS/GCP/Azure)", "Scripting (Bash/Python)"],
        "good_to_have": ["Kubernetes", "Terraform/IaC", "Monitoring (Prometheus/Grafana)", "Networking", "Git"],
        "bonus": ["Service Mesh", "Security (DevSecOps)", "Cost Optimization", "Multi-cloud", "GitOps"],
    },
    "mobile developer": {
        "must_have": ["Kotlin/Swift or React Native/Flutter", "REST APIs", "Git", "UI/UX Basics", "State Management"],
        "good_to_have": ["Testing", "CI/CD", "Push Notifications", "Offline Storage", "App Store Deployment"],
        "bonus": ["Performance Profiling", "Native Modules", "GraphQL", "Accessibility", "Analytics"],
    },
    "default": {
        "must_have": ["Programming Language", "Data Structures & Algorithms", "Git", "Problem Solving", "Communication"],
        "good_to_have": ["SQL", "REST APIs", "Testing", "Cloud Basics", "Docker"],
        "bonus": ["System Design", "CI/CD", "Open Source Contributions", "Technical Writing", "Leadership"],
    },
}


def analyze_skill_gap(current_skills: str, target_role: str = "full stack developer") -> str:
    """Analyze the gap between current skills and target role requirements.

    Args:
        current_skills: Comma-separated list of skills the user currently has
            (e.g., "Python, HTML, CSS, Git, SQL").
        target_role: The role the user is targeting
            (e.g., "frontend developer", "backend developer").

    Returns:
        A formatted skill gap analysis with recommendations.
    """
    if not current_skills or not current_skills.strip():
        return "Error: Please provide your current skills as a comma-separated list (e.g., 'Python, SQL, Git')."

    if not target_role or not target_role.strip():
        target_role = "full stack developer"

    target_role = target_role.strip().lower()
    user_skills = {s.strip().lower() for s in current_skills.split(",") if s.strip()}

    if not user_skills:
        return "Error: No valid skills found. Please provide skills separated by commas."

    # Find the closest matching role
    requirements = ROLE_REQUIREMENTS.get(target_role, ROLE_REQUIREMENTS["default"])

    lines = [f"Skill Gap Analysis for: {target_role.title()}\n"]
    lines.append(f"Your skills: {', '.join(sorted(user_skills))}\n")

    total_matched = 0
    total_required = 0

    for category, label in [
        ("must_have", "Must Have (Critical)"),
        ("good_to_have", "Good to Have (Competitive Edge)"),
        ("bonus", "Bonus (Stand Out)"),
    ]:
        skills = requirements[category]
        total_required += len(skills)
        lines.append(f"**{label}:**")

        for skill in skills:
            # Check if user has any variant of the skill
            skill_variants = [s.strip().lower() for s in skill.split(" or ")]
            has_skill = any(
                variant in user_skills or any(variant in us for us in user_skills)
                for variant in skill_variants
            )
            icon = "[HAVE]" if has_skill else "[NEED]"
            if has_skill:
                total_matched += 1
            lines.append(f"  {icon} {skill}")

        lines.append("")

    # Readiness score
    score = round((total_matched / total_required) * 100) if total_required else 0
    if score >= 80:
        verdict = "You're strongly qualified! Focus on bonus skills to stand out."
    elif score >= 60:
        verdict = "Good foundation! Fill the 'Must Have' gaps first, then 'Good to Have'."
    elif score >= 40:
        verdict = "Decent start. Prioritize the 'Must Have' skills - these are non-negotiable."
    else:
        verdict = "Early stage - focus 100% on 'Must Have' skills before anything else."

    lines.append(f"**Readiness Score: {score}%**")
    lines.append(verdict)

    lines.append(
        "\n**Action Plan:**\n"
        "  1. Fill all [NEED] items in 'Must Have' first\n"
        "  2. Build a project that demonstrates 3+ skills together\n"
        "  3. Move to 'Good to Have' skills to beat other candidates\n"
        "  4. Contribute to open source to show real-world experience"
    )

    logger.info("Skill gap analysis for '%s' - score: %d%%", target_role, score)
    return "\n".join(lines)
