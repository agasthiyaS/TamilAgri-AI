# Contributing to TamilAgri AI 🌾

Welcome to **TamilAgri AI**! This project is designed to be collaboratively developed by beginner CSE students. Follow this guide to work together cleanly and avoid stepping on each other's changes.

---

## 👥 Team Collaboration Workflow (GitHub)

### 1. Daily Golden Rule
> **Always pull before you start working!**
> ```bash
> git checkout main
> git pull origin main
> ```

---

### 2. Feature Branching Workflow
Never push directly to the `main` branch. Create a feature branch for your work:

```bash
# Format: feature/<your-name>-<short-description>
git checkout -b feature/selva-weather-tuning
```

#### Recommended Branch Names:
* `feature/weather-openmeteo-improvements`
* `feature/tnau-paddy-rules-verification`
* `feature/sms-gateway-fast2sms`
* `feature/ui-mobile-responsive-enhancements`
* `bugfix/duplicate-alert-timestamp`

---

### 3. Clear Commit Messages
Write short, meaningful commit messages using standard prefixes:

* `feat:` Added a new feature (e.g., `feat: add Tamil Nadu district rainfall threshold`)
* `fix:` Fixed a bug (e.g., `fix: mobile number validation regex`)
* `docs:` Updated documentation (e.g., `docs: add TNAU agromet references`)
* `test:` Added or updated tests (e.g., `test: add unit test for flowering heat stress`)
* `style:` UI / CSS styling changes (e.g., `style: enhance glassmorphism contrast on mobile`)

Example:
```bash
git add .
git commit -m "feat: add tillering stage flood drainage recommendation in Tamil"
```

---

### 4. Pushing and Opening a Pull Request (PR)
When your feature or bug fix is ready:

```bash
git push -u origin feature/selva-weather-tuning
```

1. Go to your GitHub repository in your browser.
2. Click **Compare & pull request**.
3. Write a brief description of:
   * What files you changed.
   * What you tested locally.
4. Request your teammate to review and click **Merge**.

---

### 5. Keeping Secrets Safe
⚠️ **CRITICAL:** Never commit `.env` or any real API keys!
* Only commit `.env.example` with blank placeholders.
* `.env`, `tamilagri.db`, `venv/`, and `node_modules/` are already listed in `.gitignore`.
* Double check with `git status` before running `git add`.

---

## 🧪 Testing Before Pushing
Always verify that tests pass before pushing:

```bash
# In the project root:
.\venv\Scripts\pytest -v

# In the frontend directory:
cd frontend
npm run build
```
