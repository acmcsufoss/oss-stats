# oss-stats

`oss-stats` is a Python CLI tool that fetches statistics from the [acmcsufoss](https://github.com/acmcsufoss) GitHub organization and the [acmcsuf.com](https://github.com/EthanThatOneKid/acmcsuf.com) repository, including issues, pull requests, commits, and total number of contributors. It provides an interactive command-line interface with colored outputs to make exploring GitHub data simple and engaging.

## Prerequisites

- To access GitHub statistics, you’ll need a **GitHub personal access token**.
- This project uses the `uv` package manager and build frontend. See https://docs.astral.sh/uv/.


### **How to Get a GitHub Token**

1. Go to [GitHub Settings](https://github.com/settings/tokens).
2. Click **"Generate new token (classic)"**.
3. Under **"Select scopes"**, enable the following:
    - `repo` (to access private and public repositories, if needed)
    - `read:org` (if you want to access organization-level data)
4. Click **"Generate token"** and **copy** the token (you won’t be able to see it again).

> ⚠️ **Important:** Keep this token secret! Treat it like a password.

---

## Setting up the Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/acmcsufoss/oss-stats.git
   cd oss-stats
   ```

2. **Install dependencies using uv:**

   ```bash
   uv sync
   ```

3. **Set up your GitHub token:**

   - Create a `.env` file in the project root with the following content:

   ```bash
   GITHUB_TOKEN="your_github_token_here"
   ```

4. **Run:**
   ```bash
   uv run oss-stats
   ```

Note: To build a distributable version of this app, use `uv build`.

Developed with 💚 by [acmcsufoss](https://github.com/acmcsufoss)
