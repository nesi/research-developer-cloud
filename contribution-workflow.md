## 1. Fork in the cloud

1. Visit https://github.com/nesi/research-developer-cloud
2. Click `Fork` button (top right) to establish a cloud-based fork.

## 2. Clone fork to local storage

Create your clone:

```sh
git clone https://github.com/<user>/research-developer-cloud.git DIRECTORY_NAME
# or: git clone git@github.com:<user>/research-developer-cloud.git DIRECTORY_NAME

cd DIRECTORY_NAME
git remote add upstream https://github.com/nesi/research-developer-cloud.git
# or: git remote add upstream git@github.com:nesi/research-developer-cloud.git

# Never push to upstream master
git remote set-url --push upstream no_push

# Confirm that your remotes make sense:
git remote -v
```

## 3. Create a Working Branch

Get your local master up to date. Note that depending on which repository you are working from,
the default branch may be called "main" instead of "master".

```sh
cd DIRECTORY_NAME
git fetch upstream
git checkout main
git rebase upstream/main
```

Create your new branch.

```sh
git checkout -b 2023-09-20_myfeature
```

You may now edit files on the `2023-09-20_myfeature` branch.

### Running the Research Developer Cloud docs

For getting up and running please read [Setting up a local development environment](local-development-environment.md)

## 4. Keep your branch in sync

You will need to periodically fetch changes from the `upstream`
repository to keep your working branch in sync. Note that depending on which repository you are working from,
the default branch may be called 'main' instead of 'master'.

Make sure your local repository is on your working branch and run the
following commands to keep it in sync:

```sh
git fetch upstream
git rebase upstream/main
```

Please don't use `git pull` instead of the above `fetch` and
`rebase`. Since `git pull` executes a merge, it creates merge commits. These make the commit history messy
and violate the principle that commits ought to be individually understandable
and useful (see below). 

You might also consider changing your `.git/config` file via
`git config branch.autoSetupRebase always` to change the behavior of `git pull`, or another non-merge option such as `git pull --rebase`.

## 5. Commit Your Changes

You will probably want to regularly commit your changes. It is likely that you will go back and edit,
build, and test multiple times. After a few cycles of this, you might
[amend your previous commit](https://www.w3schools.com/git/git_amend.asp).

```sh
git commit
```

## 6. Push to GitHub

When your changes are ready for review, push your working branch to
your fork on GitHub.

```sh
git push -f <your_remote_name> 2023-09-20_myfeature
```

## 7. Create a Pull Request

1. Visit your fork at `https://github.com/<user>/research-developer-cloud`
2. Click the **Compare & Pull Request** button next to your `2023-09-20_myfeature` branch.
3. Check you are setting your PR from your forked repo to the main repo


### Get a code review

Once your pull request has been opened it will be assigned to one or more
reviewers.  Those reviewers will do a thorough code review, looking for
correctness, bugs, opportunities for improvement, documentation and comments,
and style.

Commit changes made in response to review comments to the same branch on your
fork.

Very small PRs are easy to review.  Very large PRs are very difficult to review.