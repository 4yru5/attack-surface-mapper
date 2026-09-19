import json
import os


def detect_framework(repo_path):
    package_json = os.path.join(repo_path, "package.json")

    framework = "Unknown"
    language = "JavaScript"

    if not os.path.exists(package_json):
        return {
            "framework": framework,
            "language": language
        }

    with open(package_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = {}

    dependencies.update(data.get("dependencies", {}))
    dependencies.update(data.get("devDependencies", {}))

    if "express" in dependencies:
        framework = "Express"

    elif "@nestjs/core" in dependencies:
        framework = "NestJS"

    elif "fastify" in dependencies:
        framework = "Fastify"

    if "typescript" in dependencies:
        language = "TypeScript"

    return {
        "framework": framework,
        "language": language
    }