import os


AUTH_KEYWORDS = [
    "authMiddleware",
    "jwt",
    "passport",
    "authenticate",
    "verifyToken"
]


def discover_auth(repo_path):

    findings = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                path = os.path.join(root, file)

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as source_file:
                        content = source_file.read()

                    for keyword in AUTH_KEYWORDS:
                        if keyword in content:
                            findings.append({
                                "indicator": keyword,
                                "file": path
                            })

                except Exception:
                    pass

    return findings