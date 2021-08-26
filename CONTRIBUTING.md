# Contributing to Kosmorro

If you are reading this, then you are probably looking for a way to contribute to Kosmorro (you're in the good place!). Thank you!
There are multiple ways to contribute that can match with your possibilities.

## Opening issues

### Reporting bugs

If you found a bug, please check it is not already reported in the _Issues_ tab.
If it is not, [create a bug report](https://github.com/Kosmorro/lib/issues/new/choose) and fill in the template that offers to you. Feel free to give as much information as possible, as it will make the bug easier to fix.

### Suggest a new feature

Have an idea of feature you think would be nice on Kosmorro? Time to suggest it!
First, please check someone didn't suggest your next revolution in the _Issues_ tab. If it's not, [create a feature request](https://github.com/Deuchnord/kosmorro/issues/new/choose) and fill in the templace that offers to you.

## Writing code [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Kosmorro/lib)

First of all, if you are fixing an opened issue, check that nobody is already working on it — if someone seems to be but their Pull Request seems stuck, please ask them first if you can continue the development. If you retake the code they produced, **don't change the author of the commits**.

Before writing the code, first create a fork of the repository and clone it. You may also want to add the original repository (`Deuchnord/kosmorro`), so you can update your fork with the last upstream commits.

Then create a new branch and start coding. Finally, commit and push, then open a PR on this project. If your project is not complete, feel free to open it as Draft (if you forgot to activate the Draft status, just edit the first comment to say it), then mark it as ready for review when you're done.

### Choosing the right target branch

Whatever you are doing, always base your working branch on `master`.
When you create your PR, please consider selecting the right target branch:

- If you are fixing a bug or optimizing something, then target the `master` branch.
- If you are doing anything else, then target the `feature` branch.

This allows to make easier to publish patch releases, which have a higher priority than the minor releases.

### Matching the coding standards

Kosmorro's source code follows the major coding standards of Python (PEPs). Before marking your Pull Request as ready for review, don't forget to check that the code respects the coding standards with PyLint (it is run on the CI, but feel free to run it on your local machine too). Your PR must have a global note of 10/10 to be elligible to merge.
To ensure your code is matching the coding standards, you can use [`black`](https://github.com/psf/black) to fix the potential issues.

### Testing the code

[Unit tests](https://en.wikipedia.org/wiki/Unit_testing) check that every little piece of code (any _unit_) does exactly what it is supposed to do. They have several advantages, like proving that new things in the codebase works exactly as they should, and making sure that future changes done later won't break them.

There are two kinds of tests on this project:

- **legacy unit tests**, written with the `unittest` module
- **Documentation tests** (Doctest), written directly in the docs of the library.

The legacy tests are present for historic reason. If you want to add new tests, prefer the Doctest.

To run the tests, invoke the following commands, depending on what you want to test:

| Type | Command
| --- | ---
| Legacy tests | `make test`
| Doctest | `python3 tests.py`

Note: there are currently some memory leaks in the unit tests, making the result quite difficult to read. I am working to fix this.
If you have troubles reading them, feel free to ask.

### Commiting

The commit messages of this project follow the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/): basically, when you commit your changes, please prefix them with the following:

- **`fix: `** if your changes fix a bug;
- **`feat: `** if your changes add a new feature.

The message of your commit must start with a lowercase.
Finally, if your change introduce a BC-break, add a footer beginning with `BREAKING CHANGE:` and explaining precisely the BC-break.

Once your PR is ready to review, please squash your commits so it contains only one commit.

> To ensure your commits follow this convention, you can use [glint](https://github.com/brigand/glint).

The commit messages are then used to generate the changelog using [`conventional-changelog`](https://github.com/conventional-changelog/conventional-changelog):

```bash
conventional-changelog -p angular -i CHANGELOG.md -s
```

## Licensing and Copyright Attribution

When you open a Pull Request to the project, you agree to license your code under the [GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
