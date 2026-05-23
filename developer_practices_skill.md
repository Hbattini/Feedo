

# Developer Best Practices

These are hard rules. Apply these rules whenever helping with any coding task, code review, writing scripts, setting up projects, or giving engineering advice. These are non-negotiable baseline practices — enforce them even if not explicitly asked.

---

## Security

**Never commit secrets**

- No API keys, tokens, passwords, private keys, or credentials in any file that touches version control  
- `.env` files are never committed — always in `.gitignore`  
- If a secret is accidentally committed, treat it as compromised immediately — rotate it, don't just delete it from history  
- Use environment variables: `os.environ.get("API_KEY")` / `process.env.API_KEY`  
- Secret management: `.env.example` with placeholder values is committed; `.env` with real values is not

\# .gitignore — always include these

.env

.env.local

.env.\*.local

\*.pem

\*.key

secrets/

**Validate and sanitize inputs**

- Never trust user input — validate on the backend regardless of frontend validation  
- Use parameterized queries, never string interpolation in SQL  
- Never pass raw user input to `eval()`, `exec()`, `subprocess`, or shell commands

**Principle of least privilege**

- API keys and service accounts should only have permissions they actually need  
- Database users should not have superuser privileges in production

---

## Git Hygiene

**Commit messages**

- Format: `type: short description` — e.g. `feat: add cat profile creation`, `fix: correct JWT expiry check`  
- Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`  
- Present tense, imperative: "add" not "added" or "adds"  
- No commit messages like "fix", "wip", "asdf", "test", "update"

**Branch naming**

- `feat/cat-profile-creation`  
- `fix/jwt-token-refresh`  
- `chore/update-dependencies`

**What not to commit**

- `.env` files and secrets (see above)  
- `node_modules/`, `__pycache__/`, `.pyc` files, `venv/`, `.venv/`  
- Build artifacts: `dist/`, `build/`, `.next/`  
- IDE config: `.idea/`, `.vscode/` (unless it's shared workspace settings the team agrees on)  
- OS files: `.DS_Store`, `Thumbs.db`  
- Log files: `*.log`

**`.gitignore` is not optional** — set it up before the first commit, not after.

---

## Code Quality

**No dead code**

- Don't leave commented-out code in PRs — delete it. Git history exists for a reason.  
- No unused imports, unused variables, unused functions

**No magic numbers or strings**

- Bad: `if age_months > 120:`  
- Good: `SENIOR_CAT_THRESHOLD_MONTHS = 120`

**Functions do one thing**

- If a function name has "and" in it, it probably does two things  
- If a function is longer than \~40 lines, consider breaking it up

**Fail loudly, not silently**

- Don't catch exceptions and do nothing  
- Bad: `except Exception: pass`  
- Good: log the error, re-raise, or handle it explicitly

**Return early**

- Reduce nesting by returning or raising early instead of wrapping everything in if/else

\# Bad

def process(data):

    if data:

        if data.is\_valid():

            return data.result()

\# Good

def process(data):

    if not data:

        return None

    if not data.is\_valid():

        raise ValueError("invalid data")

    return data.result()

---

## Environment and Configuration

**Separate config from code**

- Config that changes between environments (dev/staging/prod) goes in environment variables, not in code  
- No hardcoded URLs, ports, database names, or usernames in source code  
- Provide `.env.example` with all required variable names and placeholder values

**Environment parity**

- Dev, staging, and production should run the same Docker image  
- "Works on my machine" is not acceptable — Docker solves this

**Never use production data locally**

- Dev databases use seed data, not copies of production  
- If you need prod data for debugging, anonymize it first

---

## Dependencies

**Pin versions**

- `requirements.txt` or `package.json` should pin exact versions in production  
- Use `pip freeze > requirements.txt` / `npm ci` not `npm install` in CI

**Review before installing**

- Check weekly downloads and last updated date before adding a new dependency  
- Don't add a package for something you can write in 10 lines

**Keep dependencies up to date**

- Security vulnerabilities in dependencies are your problem  
- Run `pip audit` / `npm audit` regularly

---

## API Design (GraphQL / REST)

**Never expose internal IDs directly if they reveal business information**

- Sequential integer IDs expose record counts — use UUIDs for public-facing resources

**Always paginate list endpoints**

- Never return unbounded lists — always have a limit

**Error responses should be informative but not leak internals**

- Bad: returning a full stack trace to the client  
- Good: a structured error with a code and human-readable message

**Idempotency**

- Mutations that create resources should be safe to retry  
- Use idempotency keys for operations that must not run twice (e.g. billing)

---

## Database

**Migrations are forward-only**

- Never modify an existing migration that has been run in any environment  
- Always write a new migration

**Never drop a column in one step**

- Step 1: stop writing to the column, deploy  
- Step 2: stop reading from the column, deploy  
- Step 3: drop the column, deploy  
- Skipping steps causes downtime

**Index foreign keys**

- Every FK column should have an index unless you have a specific reason not to

**Don't run migrations automatically on deploy in production**

- Run them manually or with explicit approval — an accidental migration in prod is painful

**Raw SQL over ORM for complex queries**

- If a query involves 3+ joins, scoring, or aggregation — write it in SQL  
- ORM-generated SQL for complex queries is often inefficient and hard to debug

---

## Testing

**Test behavior, not implementation**

- Tests should break when behavior changes, not when you rename a variable

**The testing pyramid**

- Most tests: unit tests (fast, isolated)  
- Some tests: integration tests (slower, test components together)  
- Few tests: end-to-end tests (slowest, test full user flows)

**Tests are not optional for critical paths**

- Auth logic must have tests  
- Recommendation engine logic must have tests  
- Payment/billing logic must have tests

**CI runs tests on every PR**

- No merging without green tests

---

## Docker

**One process per container**

- Don't run your database and your app in the same container

**Don't run as root**

- Add a non-root user in your Dockerfile

RUN adduser \--disabled-password \--gecos '' appuser

USER appuser

**Use `.dockerignore`**

- Exclude `node_modules/`, `.env`, `.git/`, build artifacts from the image

**Multi-stage builds for production**

- Build stage compiles/installs dependencies  
- Production stage copies only what's needed — smaller, more secure image

---

## Logging and Observability

**Log at appropriate levels**

- `DEBUG` — development only, verbose  
- `INFO` — normal operations worth recording (user registered, recommendation generated)  
- `WARNING` — something unexpected but handled (cache miss, retry)  
- `ERROR` — something failed and needs attention

**Never log sensitive data**

- No passwords, tokens, PII (email, name, address) in logs

**Structured logging over print statements**

- Use a logging library, not `print()`  
- Log as JSON in production — easier to query

---

## Code Review

**Every PR gets reviewed before merge**

- No self-merging without a second set of eyes, except for trivial chores

**PR size**

- Keep PRs small and focused — one concern per PR  
- A PR that changes 1000 lines rarely gets a thorough review

**Review checklist (mental)**

- Does this introduce a security vulnerability?  
- Does this have tests?  
- Does this work if the inputs are empty, null, or unexpected?  
- Is there a simpler way to do this?  
- Does this break anything existing?

---

## General

**Read the error message before asking for help**

- The error message usually tells you what's wrong

**Don't optimize prematurely**

- Make it work, make it right, make it fast — in that order

**The simplest solution that works is usually the best solution**

- Complexity is a liability, not an asset

**Document why, not what**

- Code shows what it does — comments explain why a non-obvious decision was made

**Bus factor**

- No single person should be the only one who understands a critical system  
- Write documentation as if you'll be hit by a bus tomorrow

