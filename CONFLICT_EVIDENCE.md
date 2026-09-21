# Conflict Evidence - Task 2

Every block below is **real captured terminal output** from this repository, not
a reconstruction. It is committed as a file so the conflict, the markers and the
manual resolution are inspectable from a flat file snapshot of `main`, without
needing access to the commit graph, the branches or any pull request.

Quick reference:

| Thing | Value |
| --- | --- |
| Common base commit | `00d26c81d23ce4a4279ec6d2d1065127e037b411` (`00d26c8`) |
| Branch 1 | `feature-banner-blue` -> commit `f0ff2f9` |
| Branch 2 | `feature-banner-green` -> commit `404a7c8` |
| Merge 1 (clean, `--no-ff`) | `accd3ab6df8fece3be40381341086d198dfd4716` |
| Merge 2 (conflicted, resolved by hand) | `e64f511a52ba06ac0bc8291a6d873fe60e89b262` |
| Conflict target file | `release_banner.txt` (single meaningful line) + mirrored `RELEASE_BANNER` line in `dashboard.py` |

---

## 1. Both branches were created from the SAME base commit

`git merge-base` returns the common ancestor of the two branches. It is exactly
the commit that introduced `release_banner.txt`:

```text
$ git merge-base feature-banner-blue feature-banner-green
00d26c81d23ce4a4279ec6d2d1065127e037b411
```

And that commit is `00d26c8` in the log:

```text
$ git log --oneline --graph --all --decorate
* 404a7c8 (feature-banner-green) Reword release banner for the Green Edition
| * f0ff2f9 (feature-banner-blue) Reword release banner for the Blue Edition
|/
* 00d26c8 (HEAD -> main) Add release_banner.txt as the shared release banner text
* 5dc7ae6 Add calculator entry point and dashboard presentation layer
* 727fd21 Add addition, subtraction, multiplication and division modules
* b2867fc Add login, profile and numeric input collection modules
* e539452 Add project scaffolding with gitignore, env template and configuration
```

The `|/` in that graph is the fork point: both branch tips descend from
`00d26c8` and neither descends from the other.

---

## 2. The SAME LINE of the SAME FILE was changed differently in each branch

Captured **before** the merges were performed. Note that both diffs carry the
identical hunk header `@@ -5,4 +5,4 @@` and both remove the identical `-` line,
which is what makes a conflict unavoidable.

### Branch 1 - `feature-banner-blue`

```text
$ git diff main feature-banner-blue -- release_banner.txt
diff --git a/release_banner.txt b/release_banner.txt
index 4ae6157..2722f8a 100644
--- a/release_banner.txt
+++ b/release_banner.txt
@@ -5,4 +5,4 @@
 # two branches edit it differently so Git must raise a real merge conflict.
 # The same string is mirrored in dashboard.py as RELEASE_BANNER.
 #
-Calculator Suite v1.0 - release banner pending final wording
+Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use
```

### Branch 2 - `feature-banner-green`

```text
$ git diff main feature-banner-green -- release_banner.txt
diff --git a/release_banner.txt b/release_banner.txt
index 4ae6157..2a45aca 100644
--- a/release_banner.txt
+++ b/release_banner.txt
@@ -5,4 +5,4 @@
 # two branches edit it differently so Git must raise a real merge conflict.
 # The same string is mirrored in dashboard.py as RELEASE_BANNER.
 #
-Calculator Suite v1.0 - release banner pending final wording
+Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust
```

Same file, same line number, same starting content, two different results.

---

## 3. First merge - clean, no conflict

```text
$ git switch main
Already on 'main'

$ git merge --no-ff feature-banner-blue -m "Merge feature-banner-blue into main"
Merge made by the 'ort' strategy.
 dashboard.py       | 2 +-
 release_banner.txt | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

`--no-ff` forces a real merge commit (`accd3ab`) instead of fast-forwarding, so
the branch topology stays visible in the graph forever.

---

## 4. Second merge - the REAL conflict

This is the failed merge, verbatim, including the non-zero exit code:

```text
$ git merge feature-banner-green
Auto-merging dashboard.py
CONFLICT (content): Merge conflict in dashboard.py
Auto-merging release_banner.txt
CONFLICT (content): Merge conflict in release_banner.txt
Automatic merge failed; fix conflicts and then commit the result.
(exit code: 1)
```

---

## 5. `git status` during the conflict

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

```text
$ git diff --name-only --diff-filter=U
dashboard.py
release_banner.txt
```

`--diff-filter=U` lists only unmerged (conflicted) paths - independent proof
that Git itself, not the author, flagged these two files.

---

## 6. The conflicted files exactly as Git wrote them

### `release_banner.txt`

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

### `dashboard.py`

```text
$ cat dashboard.py
"""Final integration point - displays the results produced by calculator.py."""

from calculator import total, subtraction, multiplication, div

# --- Release banner --------------------------------------------------------
# The line below mirrors the single meaningful line of release_banner.txt.
# It is the deliberate merge-conflict target for Task 2.
<<<<<<< HEAD
RELEASE_BANNER = "Calculator Suite v1.0 - Blue Edition: fast, focused arithmetic for everyday use"
=======
RELEASE_BANNER = "Calculator Suite v1.0 - Green Edition: reliable, fully tested arithmetic you can trust"
>>>>>>> feature-banner-green

print("*************** DASHBOARD ***************")
print(RELEASE_BANNER)
print("Result of addition is       : ", total)
print("Result of subtraction is    : ", subtraction)
print("Result of multiplication is : ", multiplication)
print("Result of division is       : ", div)
print("*****************************************")
```

Reading the markers:

- `<<<<<<< HEAD` opens the conflict; everything under it is **our** side, the
  content already on `main` (which at this point is the Blue Edition wording
  merged in step 3).
- `=======` is the divider between the two competing versions.
- `>>>>>>> feature-banner-green` closes the conflict; everything between the
  divider and this line is **their** side, the incoming branch.

Git writes these markers into the working-tree file and leaves the path
unmerged in the index. Nothing can be committed until a human removes the
markers and stages the file.

---

## 7. The manually resolved file

The resolution was hand-written, not `--ours`, `--theirs` or a mergetool. Both
wordings were folded into one sentence:

```text
$ cat release_banner.txt
# Release banner for the calculator project.
#
# This file deliberately holds exactly ONE meaningful line: the banner text on
# the last line below. That single line is the conflict target for Task 2 -
# two branches edit it differently so Git must raise a real merge conflict.
# The same string is mirrored in dashboard.py as RELEASE_BANNER.
#
Calculator Suite v1.0 - Blue/Green Edition: fast, focused and fully tested arithmetic you can trust every day
```

```text
$ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   dashboard.py
	modified:   release_banner.txt
```

Note "All conflicts fixed but you are still merging" - Git confirms the
resolution was staged while the merge was still in progress, which is what makes
the next commit a true conflict-resolution merge commit.

---

## 8. The resolution commit

```text
$ git show e64f511a52ba06ac0bc8291a6d873fe60e89b262 --stat
commit e64f511a52ba06ac0bc8291a6d873fe60e89b262
Merge: accd3ab 404a7c8
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:35 2026 +0530

    Resolve merge conflict in release_banner.txt by combining both branch wordings

    feature-banner-blue and feature-banner-green both rewrote the single banner
    line of release_banner.txt (and its mirror in dashboard.py), so Git reported a
    real content conflict on that line. The conflict was resolved by hand rather
    than by taking one side: the final wording keeps 'fast, focused' from the Blue
    Edition and 'fully tested ... you can trust' from the Green Edition.

 dashboard.py       | 6 ++++--
 release_banner.txt | 2 +-
 2 files changed, 5 insertions(+), 3 deletions(-)
```

The `Merge: accd3ab 404a7c8` header is the proof that this is a genuine merge
commit with two parents: the previous state of `main` and the tip of
`feature-banner-green`. A hand-edited ordinary commit could not have it.

Confirmed independently:

```text
$ git rev-list --parents -n 1 HEAD
e64f511a52ba06ac0bc8291a6d873fe60e89b262 accd3ab6df8fece3be40381341086d198dfd4716 404a7c819a1fc320bb7f458a977657a222cee94c
```

```text
$ git log --merges --oneline
e64f511 Resolve merge conflict in release_banner.txt by combining both branch wordings
accd3ab Merge feature-banner-blue into main
```

Two merge commits: the clean one and the conflicted one.

---

## 9. Full history graph

```text
$ git log --graph --oneline --all --decorate
*   e64f511 (HEAD -> main) Resolve merge conflict in release_banner.txt by combining both branch wordings
|\
| * 404a7c8 (feature-banner-green) Reword release banner for the Green Edition
* |   accd3ab Merge feature-banner-blue into main
|\ \
| |/
|/|
| * f0ff2f9 (feature-banner-blue) Reword release banner for the Blue Edition
|/
* 00d26c8 Add release_banner.txt as the shared release banner text
* 5dc7ae6 Add calculator entry point and dashboard presentation layer
* 727fd21 Add addition, subtraction, multiplication and division modules
* b2867fc Add login, profile and numeric input collection modules
* e539452 Add project scaffolding with gitignore, env template and configuration
```

Both branch tips are kept alive and pushed, so this exact graph reproduces on a
fresh clone with `git log --graph --oneline --all --decorate`.
