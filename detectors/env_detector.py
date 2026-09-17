import os
import re


# Matches:
# process.env.JWT_SECRET
# process.env.DATABASE_URL
# process.env.AWS_ACCESS_KEY

ENV_PATTERN = re.compile(
    r'process\.env\.([A-Z0-9_]+)'
)


def discover_env_vars(repo_path):

    env_vars = set()

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                file_path = os.path.join(root, file)

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    matches = ENV_PATTERN.findall(content)

                    for match in matches:
                        env_vars.add(match)

                except Exception as e:
                    print(
                        f"[ENV DETECTOR ERROR] "
                        f"{file_path}: {e}"
                    )

    return sorted(list(env_vars))