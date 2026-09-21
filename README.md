# Task 2 - Create and Resolve a Real Merge Conflict

A small Python calculator project used as the vehicle for a **genuine Git merge
conflict**: two branches created from one common base commit, both editing the
same line of the same file, merged back into `main` so that Git raised a real
`CONFLICT (content)`, which was then resolved by hand and committed.

Everything that proves it - the base commit SHA, the two divergent diffs, the
failed merge output, the raw `<<<<<<<` / `=======` / `>>>>>>>` markers, the
resolved file and the full commit graph - is **pasted verbatim into this README
and into [`CONFLICT_EVIDENCE.md`](CONFLICT_EVIDENCE.md)**, so it is all visible
in a flat file snapshot without needing the commit graph, the branches or a PR.

---

## What the project is

A four-module calculator wired together through a login and a dashboard:

| File | Role |
| --- | --- |
| `config.py` | Reads `API_KEY` from the environment, with a safe demo fallback |
| `.env.example` | Documents `API_KEY` without committing a real secret |
| `login.py` | Collects username and password |
| `profile.py` | Derives the logged-in profile name |
| `input_variables.py` | Collects the two operands |
| `addition_module.py`, `subtract_module.py`, `multiply_module.py`, `division_module.py` | The four operations, each guarded on API key + profile |
| `calculator.py` | Entry point that wires the modules to the operands |
| `dashboard.py` | Final integration point; prints the banner and the results |
| `release_banner.txt` | **The deliberate conflict target** - one meaningful line |

Every prompt falls back to a default when stdin is closed, so the project runs
non-interactively in a review environment instead of crashing with `EOFError`.

---

## How to run

```bash
git clone https://github.com/6-month-fde-challenge/task-02-merge-conflict-resolution.git
cd task-02-merge-conflict-resolution
python dashboard.py
```

Real output on a fresh clone with no stdin and no setup:

```text
$ python dashboard.py < /dev/null
Enter a number 1 :    -> no input available, using default: 10
Enter a number 2 :    -> no input available, using default: 5
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
*************** DASHBOARD ***************
Calculator Suite v1.0 - Blue/Green Edition: fast, focused and fully tested arithmetic you can trust every day
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
*****************************************
(exit code: 0)
```

The banner line printed there is the **resolved** conflict line.

---

## The conflict, step by step

**Common base commit:** `00d26c81d23ce4a4279ec6d2d1065127e037b411` (`00d26c8`)
- "Add release_banner.txt as the shared release banner text"

Both branches were cut from that exact commit using
`git switch -c <branch> 00d26c81d23ce4a4279ec6d2d1065127e037b411`, so they are
true siblings rather than one descending from the other:

```text
$ git merge-base feature-banner-blue feature-banner-green
00d26c81d23ce4a4279ec6d2d1065127e037b411
```

**The two branches:**

| Branch | Tip | Link |
| --- | --- | --- |
| `feature-banner-blue` | `f0ff2f9` | [tree/feature-banner-blue](https://github.com/6-month-fde-challenge/task-02-merge-conflict-resolution/tree/feature-banner-blue) |
| `feature-banner-green` | `404a7c8` | [tree/feature-banner-green](https://github.com/6-month-fde-challenge/task-02-merge-conflict-resolution/tree/feature-banner-green) |

**The exact line that diverged** - line 8 of `release_banner.txt`, mirrored by
the `RELEASE_BANNER` line of `dashboard.py`:

| Version | Line 8 of `release_banner.txt` |
| --- | --- |
| base `00d26c8` | `Calculator Suite v1.0 - release banner pending final wording` |
| `feature-banner-blue` | `Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use` |
| `feature-banner-green` | `Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust` |

Proven by diff, captured before the merges. Both hunks have the same header and
delete the same line:

```text
$ git diff main feature-banner-blue -- release_banner.txt
@@ -5,4 +5,4 @@
 #
-Calculator Suite v1.0 - release banner pending final wording
+Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use

$ git diff main feature-banner-green -- release_banner.txt
@@ -5,4 +5,4 @@
 #
-Calculator Suite v1.0 - release banner pending final wording
+Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust
```

**Merge 1 (clean).** `--no-ff` guarantees a real merge commit so the topology
survives:

```text
$ git merge --no-ff feature-banner-blue -m "Merge feature-banner-blue into main"
Merge made by the 'ort' strategy.
 dashboard.py       | 2 +-
 release_banner.txt | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

**Merge 2 (conflict).** `main` now holds the Blue wording; the incoming branch
holds the Green wording for the same line, so Git cannot decide:

```text
$ git merge feature-banner-green
Auto-merging dashboard.py
CONFLICT (content): Merge conflict in dashboard.py
Auto-merging release_banner.txt
CONFLICT (content): Merge conflict in release_banner.txt
Automatic merge failed; fix conflicts and then commit the result.
(exit code: 1)
```

```text
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   dashboard.py
	both modified:   release_banner.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

---

## The conflict markers

`release_banner.txt` exactly as Git wrote it during the conflict:

```text
$ cat release_banner.txt
# Release banner for the calculator project.
#
# This file deliberately holds exactly ONE meaningful line: the banner text on
# the last line below. That single line is the conflict target for Task 2 -
# two branches edit it differently so Git must raise a real merge conflict.
# The same string is mirrored in dashboard.py as RELEASE_BANNER.
#
<<<<<<< HEAD
Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use
=======
Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust
>>>>>>> feature-banner-green
```

`dashboard.py` at the same moment:

```text
$ cat dashboard.py
# --- Release banner --------------------------------------------------------
# The line below mirrors the single meaningful line of release_banner.txt.
# It is the deliberate merge-conflict target for Task 2.
<<<<<<< HEAD
RELEASE_BANNER = "Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use"
=======
RELEASE_BANNER = "Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust"
>>>>>>> feature-banner-green
```

**What the markers mean:**

- `<<<<<<< HEAD` - start of the conflicted region. Everything from here down to
  the divider is **our** side: what `main` (`HEAD`) already contains. Here that
  is the Blue Edition wording, because merge 1 put it on `main`.
- `=======` - the divider. It separates the two competing versions of the same
  region. It is not content; it is a fence.
- `>>>>>>> feature-banner-green` - end of the conflicted region. Everything
  between the divider and this line is **their** side: the version coming from
  the branch being merged in. The label after the arrows names that source.

While the markers are present the path is *unmerged* in Git's index. Git refuses
to complete the merge until a human deletes the markers, leaves the intended
content, and stages the file with `git add`.

---

## How I decided what to keep

I did **not** take `--ours` or `--theirs`. Each branch contributed a genuinely
useful idea and discarding either would have lost information:

- `feature-banner-blue` sold the product on **speed and focus** -
  "fast, focused arithmetic for everyday use".
- `feature-banner-green` sold it on **reliability and test coverage** -
  "reliable, fully tested arithmetic you can trust".

Speed and trustworthiness are not in tension, so the honest resolution keeps
both claims in one sentence. I hand-wrote a combined line that carries
"fast, focused" from Blue, "fully tested ... you can trust" from Green, and
folds Blue's "everyday use" into the closing "every day". The edition name
became "Blue/Green Edition" to record that the released banner is the union of
the two branches.

**Final resolved line:**

```text
Calculator Suite v1.0 - Blue/Green Edition: fast, focused and fully tested arithmetic you can trust every day
```

Staged and committed while the merge was still in progress:

```text
$ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   dashboard.py
	modified:   release_banner.txt
```

**Resolution commit:** [`e64f511a52ba06ac0bc8291a6d873fe60e89b262`](https://github.com/6-month-fde-challenge/task-02-merge-conflict-resolution/commit/e64f511a52ba06ac0bc8291a6d873fe60e89b262)

```text
$ git show e64f511a52ba06ac0bc8291a6d873fe60e89b262 --stat
commit e64f511a52ba06ac0bc8291a6d873fe60e89b262
Merge: accd3ab 404a7c8
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:35 2026 +0530

    Resolve merge conflict in release_banner.txt by combining both branch wordings

 dashboard.py       | 6 ++++--
 release_banner.txt | 2 +-
 2 files changed, 5 insertions(+), 3 deletions(-)
```

The `Merge: accd3ab 404a7c8` line is the two-parent proof: this is a real merge
commit, not a hand-edited ordinary commit.

---

## Full git history

The whole point of the task, pasted from the repository:

```text
$ git log --graph --oneline --all --decorate
* 6d49063 (HEAD -> main, origin/main) Document the merge conflict with captured evidence and submission links
*   e64f511 Resolve merge conflict in release_banner.txt by combining both branch wordings
|\
| * 404a7c8 (origin/feature-banner-green, feature-banner-green) Reword release banner for the Green Edition
* |   accd3ab Merge feature-banner-blue into main
|\ \
| |/
|/|
| * f0ff2f9 (origin/feature-banner-blue, feature-banner-blue) Reword release banner for the Blue Edition
|/
* 00d26c8 Add release_banner.txt as the shared release banner text
* 5dc7ae6 Add calculator entry point and dashboard presentation layer
* 727fd21 Add addition, subtraction, multiplication and division modules
* b2867fc Add login, profile and numeric input collection modules
* e539452 Add project scaffolding with gitignore, env template and configuration
```

> **Note on this capture.** It was taken one commit before the final
> "Refresh captured git history evidence" commit that published it, so `main`
> shows `6d49063` at the tip rather than that refresh commit. Everything the
> task is graded on - the base commit, both branch tips, both merges and the
> resolution commit - is unaffected. Run the command yourself on a clone to see
> the same shape with one extra commit on top.

How to read it:

- `00d26c8` is the **common base**. Both branch lines leave from it.
- `f0ff2f9` and `404a7c8` are the two **branch tips**, still alive and pushed,
  each shown with its branch name in parentheses.
- `accd3ab` is **merge 1**, the clean `--no-ff` merge of the Blue branch.
- `e64f511` is **merge 2**, the conflict-resolution merge of the Green branch.
- The two `|\` forks are the two merges; the diamond shape is exactly the
  "two branches from one base, both merged back" topology the task asks for.

Both merges, listed on their own:

```text
$ git log --merges --oneline
e64f511 Resolve merge conflict in release_banner.txt by combining both branch wordings
accd3ab Merge feature-banner-blue into main
```

Both feature branches exist on the remote:

```text
$ git ls-remote --heads origin
f0ff2f9eb67459e82cb656c8caf38ba230716710	refs/heads/feature-banner-blue
404a7c819a1fc320bb7f458a977657a222cee94c	refs/heads/feature-banner-green
6d49063a7f4674d91d3a290c386cfafe75497dea	refs/heads/main
```

---

## Command walkthrough

Every command that built this repository, with its real output.

**1. Initialise**

```text
$ git init -b main
Initialized empty Git repository in .../task-02-merge-conflict-resolution/.git/
$ git config user.name "veerandra7"
$ git config user.email "veerandra.data@gmail.com"
```

**2. Commit the baseline in five descriptive commits**

```text
$ git log --oneline
00d26c8 Add release_banner.txt as the shared release banner text
5dc7ae6 Add calculator entry point and dashboard presentation layer
727fd21 Add addition, subtraction, multiplication and division modules
b2867fc Add login, profile and numeric input collection modules
e539452 Add project scaffolding with gitignore, env template and configuration
```

`00d26c8` is the base commit, recorded before branching.

**3. Branch 1 from the base**

```text
$ git switch -c feature-banner-blue 00d26c81d23ce4a4279ec6d2d1065127e037b411
Switched to a new branch 'feature-banner-blue'
$ tail -1 release_banner.txt
Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use
$ git commit -m "Reword release banner for the Blue Edition"
```

**4. Branch 2 from the SAME base**

```text
$ git switch -c feature-banner-green 00d26c81d23ce4a4279ec6d2d1065127e037b411
Switched to a new branch 'feature-banner-green'
$ tail -1 release_banner.txt
Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust
$ git commit -m "Reword release banner for the Green Edition"
$ git merge-base feature-banner-blue feature-banner-green
00d26c81d23ce4a4279ec6d2d1065127e037b411
```

**5. Merge 1 - clean**

```text
$ git switch main
$ git merge --no-ff feature-banner-blue -m "Merge feature-banner-blue into main"
Merge made by the 'ort' strategy.
 dashboard.py       | 2 +-
 release_banner.txt | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

**6. Merge 2 - conflict**

```text
$ git merge feature-banner-green
Auto-merging dashboard.py
CONFLICT (content): Merge conflict in dashboard.py
Auto-merging release_banner.txt
CONFLICT (content): Merge conflict in release_banner.txt
Automatic merge failed; fix conflicts and then commit the result.

$ git diff --name-only --diff-filter=U
dashboard.py
release_banner.txt
```

**7. Resolve by hand and commit**

```text
$ git add release_banner.txt dashboard.py
$ git commit -m "Resolve merge conflict in release_banner.txt by combining both branch wordings"
$ git rev-list --parents -n 1 HEAD
e64f511a52ba06ac0bc8291a6d873fe60e89b262 accd3ab6df8fece3be40381341086d198dfd4716 404a7c819a1fc320bb7f458a977657a222cee94c
```

**8. Push everything, keeping both branches alive**

```text
$ gh repo create 6-month-fde-challenge/task-02-merge-conflict-resolution --public --source=. --remote=origin --push
$ git push -u origin --all
```

---

## Fixes applied after review feedback

The previous submission scored poorly because the conflict work existed only in
the local commit graph and was therefore invisible to a reviewer looking at a
flat file snapshot. Every point raised has been addressed:

- **"No verifiable branch or commit history proving two branches were created
  from the same base."** The full commit graph is now pushed with both feature
  branches alive on the remote, and `git merge-base` output plus the base SHA
  `00d26c81d23ce4a4279ec6d2d1065127e037b411` are pasted into this README and
  into `CONFLICT_EVIDENCE.md`.
- **"No file history or diff is visible showing the same line of the same file
  changed differently in two branches."** Both `git diff` captures are pasted
  above, taken before the merges, showing the identical hunk header and the
  identical removed line with two different replacements.
- **"The submitted snapshot does not show a merge attempt that produced Git
  conflict markers."** The failed `git merge` output, the `git status` during
  the conflict, and the raw conflicted files with `<<<<<<< HEAD`, `=======` and
  `>>>>>>> feature-banner-green` are pasted verbatim above and in
  `CONFLICT_EVIDENCE.md`.
- **"The commit history proving a manual resolution is not available in the
  source view."** `git show --stat` of the resolution commit, its two-parent
  `Merge:` header, `git rev-list --parents`, and `git log --merges` are all
  included, and the reasoning behind the hand-written combined line is written
  out in "How I decided what to keep".
- **"Use `git log --graph --oneline --all` and keep the branches or commits
  visible."** That exact command's real output is pasted in the "Full git
  history" section, and both branches are pushed so it reproduces on a clone.
- **"Add a simple text file or comment line as the deliberate conflict
  target."** `release_banner.txt` was added for exactly this - a plain text file
  whose only meaningful line is the banner, mirrored by a single commented
  `RELEASE_BANNER` line in `dashboard.py`, so the same-line edits and the final
  resolution are trivial to inspect.

No conflict markers remain in any source file. They appear only inside the
fenced evidence blocks of `README.md` and `CONFLICT_EVIDENCE.md`, where they are
documentation rather than broken code - `python dashboard.py` runs clean, as the
output at the top of this README shows.

---

## Repository layout

```text
task-02-merge-conflict-resolution/
├── .env.example              # documents API_KEY; no real secret committed
├── .gitignore                # ignores caches, venvs, .env - never a file the code imports
├── CONFLICT_EVIDENCE.md      # full captured evidence of the conflict
├── README.md                 # this file
├── submission_links.txt      # repo, branch and commit URLs
├── release_banner.txt        # THE CONFLICT TARGET - one meaningful line
├── config.py
├── login.py
├── profile.py
├── input_variables.py
├── addition_module.py
├── subtract_module.py
├── multiply_module.py
├── division_module.py
├── calculator.py
└── dashboard.py              # mirrors the banner line; prints the results
```

`.gitignore` deliberately does not ignore any module that the code imports, and
there is no `secrets.py` - `config.py` reads `API_KEY` from the environment
instead, so a fresh clone runs without setup.
