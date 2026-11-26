# extract_pdf_pages

Extract all references pages in the [OSTEP](http://pages.cs.wisc.edu/~remzi/OSTEP/) PDF files.

Use Python 3.11.5 or a later Python 3.11 release. The `soupsieve` 4 package needs this version to include its security fixes.

Install the packages from the lockfile:

```sh
pipenv install --deploy --ignore-pipfile --dev
```

This command rejects a Python version outside the required range. Use Pipenv 2026.12.1 or later for Python version ranges.

`pipenv sync` can skip Soup Sieve on older Python versions and report success. The install command uses `--deploy` to reject those versions.

Run the script:

```sh
pipenv run python main.py
```

The script writes the reference pages to `references.pdf`. The `PyPDF2` package stays on version 1.x because the script uses the API of that version.
