# oss-stats
<img width="600" height="800" alt="image" src="https://github.com/user-attachments/assets/ac8d6854-2f55-4e47-93dd-ee5fa8c53eaa" />


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

Note: To build a distributable version of this app, use `uv build`.

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
---

## How to Contribute

We welcome contributions! To contribute to `oss-stats`, please follow these steps:

1. **Fork the repository:**
   - Click the **Fork** button at the top right of the [acmcsufoss/oss-stats](https://github.com/acmcsufoss/oss-stats) repository to create a copy in your account.

2. **Clone your fork:**
   ```bash
   # Replace <YOUR_USERNAME> with your GitHub username
   git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/oss-stats.git
   cd oss-stats
3. **Add the upstream remote:**
   ```bash
   git remote add upstream [https://github.com/acmcsufoss/oss-stats.git](https://github.com/acmcsufoss/oss-stats.git)
4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: description of the change"
   git push origin feature/your-task-name
5. **Open a Pull Request:**
   - Go to the original oss-stats repo on GitHub.
   - You will see a prompt to "Compare & pull request".
   - Describe your changes and submit for review.

---

Developed with 💚 by [acmcsufoss](https://github.com/acmcsufoss)
