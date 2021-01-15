# Latex_formula_editor

A LaTeX formula reference and editing tool

## What's this

* An off-line reference of math-related LaTex symbols and operators, giving you quick a
reminder to the obscure or unfamiliar Latex codes when composing without quick access to inernet.

* Converts LaTex formula to png image file with control of image resolution.

## Screenshots

![Screenshot 1](https://github.com/Xunius/Latex_formula_editor/blob/master/Screenshot_1.png)
![Screenshot 2](https://github.com/Xunius/Latex_formula_editor/blob/master/Screenshot_2.png)


## Platform/OS

Developed and tested in Linux. Might work in Mac.

## Dependencies

* Python 2 or 3
* PyQt5 (python module)
* latex (`texlive-core` and `texlive-latexextra` packages)
* convert (part of the ImageMagick suite)

## Usage

1. Download the zip file and unzip it to local disk.
2. Change into its directory.
3. Make tex2im executable: `chmod +x ./tex2im/tex2im`.
4. Run `python latex_formula_editor.py`

## Trouble-shooting

### "Failed to render image. Please re-check your formula" error

**Issue**
After typing in the formula and hitting "Render", an error message of
*"Failed to render image. Please re-check your formula"* appears below.

**Solution**

Please make sure `texlive-core` and `texlive-latexextra` are installed and working.
Then make sure the `tex2im/tex2im` file has execution permission.
If the error still persists, check out the problem below.

### convert: attempt to perform an operation not allowed by the security policy `gs'

**Issue**

After typing in the formula and hitting "Render", an error message of
*"Failed to render image. Please re-check your formula"* appears below.
`texlive-core` and `texlive-latexextra` are both installed and working, and
`tex2im` has execution permission.

**Solution**

Open up a terminal and `cd` into the `tex2im` folder, run the following test command:

```
tex2im "\sum_{i=0}^5 x_i^2"
```

If this error message is printed out:

```
convert: attempt to perform an operation not allowed by the security policy `gs' @ error/delegate.c/ExternalDelegateCommand/378.
```

Then this is a problem related to `ImageMagic`. See [this stackoverflow post](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion) for more information.

Personally I use an arch-based Linux OS, and this fix worked for me:

Edit the `/etc/Imagemagic-7/policy.xml` file, and comment out this line:

```
<policy domain="delegate" rights="none" pattern="gs" />
```


## Related projects

This project incorporates with minor changes of [tex2im](http://www.nought.de/tex2im.php), which provides the LaTeX image rendering functionality. The files of *tex2im* can be found in the subfolder with same name.


