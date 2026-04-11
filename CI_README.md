Continuous Integration / Delivery Setup

- This repository includes a basic GitHub Actions workflow at .github/workflows/ci.yml.
- The workflow automatically detects common project types (Node / Python) and runs tests accordingly when pushing to main or on PRs targeting main.
- You can extend the workflow to cover more languages and test commands as the project grows.
