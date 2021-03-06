# aptitude-analysis
Carolyn D. Gorman | NYU Robert F. Wagner Graduate School of Public Service | July 2021

## Project Summary 
Question: What is the relationship between early adulthood measures of aptitude and attitudes and later life labor market outcomes (namely wages)?

Using data from the National Longitudinal Survey of Youth 1979 (NLSY79), I prepare a preliminary examination of how indicators of aptitude and attitudes during respondents' early adulthood are related to later life labor market outcomes, here, focused on hourly wages.

## Data Summary 
The NLSY79 is a nationally representative sample of 12,686 young men and women born during the years 1957 through 1964 and living in the United States when the survey began. The survey respondents were ages 14 to 22 when first interviewed in 1979. Interviews were conducted annually from 1979 to 1994 and on a biennial basis thereafter. This research draws on data through 2013. 

## Folders 
- code: Code documentation 
- data: Contains raw NLSY79 files (uploaded on github temporarily). 
- out: Shareable output 
- draft: Draft of presentation and written piece  

## How to Reproduce This Analysis
- Get the data and files by cloning the git repository
- Set up a local virtual environment 
    - This code runs on Python 3
    - Necessary packages are listed in the file "requirements.txt"  
- Code files can be run in the following order to replicate: 
    - (1) setup_dct.py (*sets up a dictionary for the dataset via variable names*)
    - (2) setup_additional_vars.py (*processes some additional variables for further analysis*) 
    - (3) setup_classobj.py (*sets up organization of dataset as a class object*)
    - (4) setup_fin_dataset.py (*builds out the dataset which can be used across plots/analysis*)
 - Other code files, which can be run in any order:
    - plots_dataset_overview.py (*includes plots for some overview of the NLSY79*)
    - plots_exploratory.py (*includes plots for aptitude / attitude scores by socioeconomic and demographic characteristics*)
    - plots_apt_att_measures.py (*includes plots for basic relationship between aptitude/attitude & hourly wages*)
    - plots_apt_att_gender.py (*includes plots for basic relationship between aptitude/attitude and later life hourly wage*)
    - exploratory_analysis.py (*includes code to create Table 1 in the blog post*)


### Attributions 
Much of the code for structuring the dataset was modeled after https://github.com/HumanCapitalAnalysis/nlsy-data. These contributors maintain a cleaned version of the National Longitudinal Survey of Youth 1979 (NLSY79), and I would like to credit them here: Luis Wardenbach, Philipp Eisenhauer, Sebastian Becker, and @bekauf.

Thank you to the NYU Wagner MSPP class of 2021, Maxwell Austensen, Thom Blaylock, Kathy O'Regan, Sherry Glied, and Buyi Wang for their broad support and guidance.

License for the code can be found in the LICENCE file.
