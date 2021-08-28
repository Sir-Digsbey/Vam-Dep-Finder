# Vam-Dep-Finder
Finds missing dependencies for VAM

# How to run
First install Python 3.8 or higher (google it if you need to).
Then download file, place anywhere you'd like, and run with `python depfinder.py --var-path <PATH>` (replace <PATH> with the path to your VAR directory).

Resuts will be saved to a file called `missing.json`.

The output will be in a JSON format, where keys are what packages need those missing dependencies, and the value is a list of all the missing packages that that package has.

For example:

```
    "vecterror.PerPip_looks.2.var": [
        "vecterror.PePivsMan",
        "Jackaroo.MocapExpressionsMale",
        "Jackaroo.JarExpressions",
        "vecterror.BODY_SHAPE1"
    ]
```

Means that `vecterror.PerPip_looks.2.var` (which I do have) is missing the packages `vecterror.PePivsMan`, `Jackaroo.MocapExpressionsMale`, `Jackaroo.JarExpressions`, etc...

Alternatively, add `--list` to get the results as a simple list of mising packages instead of a JSON - in which case the results will be saved in `missing.txt`

In case there's an error in any of the files, it will be printed at the end of the output (but not saved to the file).
