# extract_pdf_pages

Extract all references pages in the [OSTEP](http://pages.cs.wisc.edu/~remzi/OSTEP/) PDF files.

Use Python 3.11.5 or a later Python 3.11 release. The `soupsieve` 4 package needs this version to include its security fixes.

Install the packages from the lockfile:

```sh
pipenv sync --dev
```

Run the script:

```sh
pipenv run python main.py
```

The script writes the reference pages to `references.pdf`. The `PyPDF2` package stays on version 1.x because the script uses the API of that version.
