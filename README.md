# oss_stats

`oss_stats` is a Python CLI tool that fetches statistics from the [acmcsufoss](https://github.com/acmcsufoss) GitHub organization and the [acmcsuf.com](https://github.com/EthanThatOneKid/acmcsuf.com) repository, including issues, pull requests, commits, and total number of contributors. It provides an interactive command-line interface with colored outputs to make exploring GitHub data simple and engaging.

## Prerequisites

To access GitHub statistics, you’ll need a **GitHub personal access token**.

### **How to Get a GitHub Token**
1. Go to [GitHub Settings](https://github.com/settings/tokens).
2. Click **"Generate new token"**.
3. Under **"Select scopes"**, enable the following:
    - `repo` (to access private and public repositories, if needed)
    - `read:org` (if you want to access organization-level data)
4. Click **"Generate token"** and **copy** the token (you won’t be able to see it again).

> ⚠️ **Important:** Keep this token secret! Treat it like a password.

---

## Setting up the Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/acmcsufoss/oss_stats.git
   cd oss_stats
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate   # On Windows
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your GitHub token:**
   - Create a `.env` file in the project root with the following content:
   ```bash
   GITHUB_TOKEN="your_github_token_here"
   ```
---

## Installation

To install `oss_stats` locally:

```bash
pip install .
```

Alternatively, if you’re actively developing:

```bash
pip install -e .
```

> **Note:** The `-e` flag installs the project in **editable mode** so that any changes you make reflect immediately without reinstallation.

## Usage

Once installed, you can run the CLI tool from the terminal:

```bash
oss_stats
```

---

Developed with 💚 by [acmcsufoss](https://github.com/acmcsufoss)
