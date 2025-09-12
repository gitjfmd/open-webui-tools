
## 🔨 Code Contribution

### Setting Up Your Development Environment

1.  **Fork the Repository**
    Click the 'Fork' button at the top right of the [main repository page](https://github.com/gitjfmd/open-webui-tools) to create your copy on GitHub.

2.  **Clone Your Fork**
    ```bash
    git clone https://github.com/YOUR_USERNAME/open-webui-tools.git
    cd open-webui-tools
    ```

3.  **Set Upstream Remote**
    Add the original repository as a remote to sync with the latest changes.
    ```bash
    git remote add upstream https://github.com/gitjfmd/open-webui-tools.git
    ```

### The Contribution Workflow

1.  **Sync Your Fork:** Always start from an up-to-date `main` branch.
    ```bash
    git checkout main
    git fetch upstream
    git merge upstream/main
    ```

2.  **Create a Branch:** Create a descriptive branch for your work.
    ```bash
    # For a new tool:
    git checkout -b feat/add-google-drive-sync
    # For a bug fix:
    git checkout -b fix/crash-in-pdf-tool
    # For documentation:
    git checkout -b docs/update-install-guide
    ```

3.  **Make Your Changes:** This is where you build your tool or fix the bug!
    *   **For a new tool:** Create a new folder for it in the appropriate category (e.g., `/tools/api-integrations/your-tool-name/`).
    *   **Include a README:** Every tool must have its own `README.md` with installation, configuration, and usage instructions.
    *   **Test thoroughly:** Ensure your tool works with the latest version of Open WebUI.

4.  **Stage and Commit Your Changes:**
    ```bash
    git add .
    git commit -m "feat: add Google Drive sync tool with OAuth2 support"
    ```
    **Commit Message Guidelines:**
    *   Use the imperative mood ("Add" not "Adds" or "Added").
    *   Start with a type: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
    *   Keep the first line under 50 characters.

5.  **Push to Your Fork:**
    ```bash
    git push origin your-branch-name
    ```

6.  **Submit a Pull Request (PR):**
    *   Go to your fork on GitHub. You will see a prompt to open a PR for your new branch.
    *   **Write a clear title and description.** Explain what you did and why.
    *   **Link related issues.** If your PR fixes an issue, write `Fixes #123`.
    *   **Use the PR template** (if provided) to ensure you include all necessary information.

### Code and PR Review

*   Once submitted, project maintainers and community members will review your PR.
*   We may suggest changes or ask questions. Please don't be discouraged—this is a normal part of the process!
*   Once approved, a maintainer will merge your PR. Congratulations!

## 🙋 Need Help?

If you have any questions or need help at any point, please don't hesitate to:
*   Ask a question in our [GitHub Discussions](https://github.com/gitjfmd/open-webui-tools/discussions).
*   Comment on the relevant issue or pull request.

Thank you for contributing and helping to build the future of Open WebUI! 🚀
