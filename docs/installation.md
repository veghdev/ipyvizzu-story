# Installation

`ipyvizzu-story` requires the [ipyvizzu](https://pypi.org/project/ipyvizzu)
package.

!!! info
    `ipyvizzu-story` requires and downloads the
    [Vizzu](https://github.com/vizzuhq/vizzu-lib) `JavaScript`/`C++`
    [library](https://www.jsdelivr.com/package/npm/vizzu) and the
    [Vizzu-Story](https://github.com/vizzuhq/vizzu-ext-js-story) `JavaScript`
    [package](https://www.jsdelivr.com/package/npm/vizzu-story) from
    `jsDelivr CDN`.

## pypi

Run the following command to install `ipyvizzu-story` from
[pypi](https://pypi.org/project/ipyvizzu-story/)

```sh
pip install ipyvizzu-story
```

and this is how to upgrade it.

```sh
pip install -U ipyvizzu-story
```

You can use `ipyvizzu-story` in `Jupyter/IPython`, `Streamlit` or
`Python` (see [Environments chapter](environments/index.md) for more details).

### Jupyter/IPython

You can install `ipyvizzu-story` in your notebook without using the command line
by entering the following code into a cell.

```
!pip install ipyvizzu-story
```

If you want to install `Jupyter/IPython` as a dependency, install
`ipyvizzu-story` with the following command.

```sh
pip install ipyvizzu-story[jupyter]
```

### Streamlit

If you want to install `Streamlit` as a dependency, install `ipyvizzu-story`
with the following command.

```sh
pip install ipyvizzu-story[streamlit]
```
