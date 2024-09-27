# Climate Change Uncertainty Spillover in the Macroeconomy
This repository contains codes and jupyter notebooks which compute and demonstrate results of "Climate Change Uncertainty Spillover in the Macroeconomy" by [Micheal Barnett][id1], [William Brock][id2] and [Lars Peter Hansen][id3]. Latest version could be found [here][id4].

For further detail of computation, see also: [online documentation](https://climateuncertaintyspillover.readthedocs.io/en/latest/)

[id1]: tocomplete
[id2]: https://economics.missouri.edu/people/brock
[id3]: https://larspeterhansen.org/
[id4]: https://larspeterhansen.org/research/papers/

## Table of contents
- [Prerequisite](#prerequisite)
- [Acessing our project](#acessing)
- [Quick user's guide](#quick-guide)

## <a name="prerequisite"></a>Prerequisite
`Python == 3.8.x`, package manager such as `pip`,  and `jupyter notebook` to checkout the notebooks.

To go to the documentation of this project, please go to: (link avaliable when published).

This project has been tested in an environment with
> `Python == 3.8.7` and  `jupyter notebook == 5.7.10`

## <a name="acessing"></a>Acessing our project
To access our notebook binder, click below:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lphansen/ClimateUncertaintySpillover.git/macroAnnual_v2?filepath=sec0_prep.ipynb)

To store the notebook as well as codes in your local machine. You can do this by following steps below:

1.  Open a Windows command prompt, Mac terminal or Linux terminal and change into the folder you would like to store the files.
 	-  You can do this using the command `cd` in the command prompt (on Windows) or terminal (on Mac and Linux).
        - For example, running `cd 'C:\Users\username\python'` (don’t forget '' around the path name to use an absolute path) would lead me to my designated folder.

    ```bash
    $ cd [folder path name]
    ```

2.  Clone the github repository for the paper
    - If you don’t have github installed, try installing it from this page: https://git-scm.com/download.
    - You can do this by running below in the command prompt:

    ```bash
    $ git clone https://github.com/lphansen/WrestlingClimatie.git
    ```

3.  Change directories into the ‘Wrestling’ folder and install the required packages for the current user or your initiated virtual environment:

    ```bash
    $ cd WrestlingClimate
    $ pip install -r requirements.txt
    ```
4. Access the notebooks, run the following under the folder `WrestlingClimate/`:

    ```bash
    $ jupyter notebook
    ```
    and you will see the notebooks listed below.

    Then click <button type = "button" name="runall">Run all</button> from <button type="runtime" name="runtime">runtime</button> to see our results.

## <a name="quick-guide"></a>Quick user's guide

description of notebooks' contents

The notebooks are separated according to section in the paper.
- Section 1: [Introduction](sec1_Introduction.ipynb)
- Section 2: [Climate Dynamics](sec2_UncertainClimateDynamics.ipynb)
- Section 3: [Uncertain Damage](sec3_UncertainDamage.ipynb)
- Section 4: [Illustrative Economy I: Uncertain Damages](sec4_IllustrativeEconI.ipynb)
- Section 5: [Illustrative Economy II: Uncertainty Decomposition](sec5_IllustrativeEconII.ipynb)
- Section 6: [Illustrative Economy III: Carbon abatement technology](sec6_IllustrativeEconIII.ipynb)
- Section 7: [Conclusion](sec7_Conclusion.ipynb)

As well as [appendices](appendices.ipynb):
- A. Complete model
- B. Computation methods
