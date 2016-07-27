# Hand history converter

### Purpose

* To create a hand history converter to convert from the Hyperborean AI hand histories to Pokerstars hand histories.

### Setup

Follow these instructions to get the code and start debugging it.

1. Make sure you have a suitable installation of **git** for your operating system. There's great **git** instructions here: `https://git-scm.com/`
2. Make sure you have **python** installed on your system.  I used Python 2.7.10
3. Optionally, install **PyCharm** for a great Python integrated development environment: `https://www.jetbrains.com/pycharm/`
4. Clone the repository with the command `git clone git@github.com:chrisalvino/handhistoryconverter.git`
5. You can run the program by executing `converter.py 3pl.HITSZ_CS_14.Hyperborean_iro.SmooCT.0.0.log AiParserOutput.txt 8 16`. 

The first argument is the input file name, the second argument is the output file name, the third is the size of the small bet and the fourth is the size of the big bet.

### Branching code

Follow these instructions to start modifying the code.

1. Create a branch with the command `git branch myBranchFeatureName`.  The branch name should be descriptive of the changes you are making but short.  I'll use the name `myBranchFeatureName` for example here.
2. Switch your local repository to the branch you just made with `git checkout myBranchFeatureName`
3. Make your changes to the code 
4. Use `git add` for every file you change, for example if you changes `converter.py` then do `git add converter.py`
5. Commit your changes to your local repository with a comment: `git commit -m "Cleaned up some functions"`
6. Push changes on that branch back to github with `git push origin myBranchFeatureName` 
7. Go to the project page, `https://github.com/chrisalvino/handhistoryconverter` and make a pull request for the pushed branch.
    1. Click on `Pull Requests` and then `New Pull Request`
    2. Select the branch you want to merge into as `base: master` and the branch you want merge from as `compare: myBranchFeatureName`
    3. Click `Create Pull Request`






