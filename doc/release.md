# Release steps

- update version information in repository by editing the following files:
```
    openms/core.py
    setup.py
```
- push changes to github
- Create a release at github, tagging the version in the normal way.
- `git pull` in local repository, to update tags
- Upload release to `pypi.org`:
```
    rm -rf dist 
    rm -rf *.egg-info 
    python setup.py sdist 
    twine upload dist/*
```

