# aptitude-analysis
Author: Carolyn D. Gorman  | NYU Robert F. Wagner Graduate School of Public Service  |  June / July 2021

## Project Summary 
Question: What is the relationship between early life aptitude and later life labor market outcomes?

Using data from the National Longitudinal Survey of Youth 1979 (NLSY79), I examine how indicators of aptitude, self-esteem, and sense of control during respondents' early adulthood are related to later life labor market outcomes such as income and wages, occupation, and having employer-provided health insurance coverage.

## Data Summary 
The NLSY79 is a nationally representative sample of 12,686 young men and women born during the years 1957 through 1964 and living in the United States when the survey began. The survey respondents were ages 14 to 22 when first interviewed in 1979. Interviews were conducted annually from 1979 to 1994 and on a biennial basis thereafter. This research draws on data through 2013. More information about the NLSY79 and variables included in this analysis can be found in the data documentation folder.

## Folders 
- code: Code documentation 
- data: Contains raw NLSY79 files (uploaded on github temporarily). 
- doc: Data documentation 
- out: Shareable output 
- draft: Draft of written piece  

## How to Reproduce This Analysis
- Get the data and files by cloning the git repository
- Set up a local virtual environment 
    - This code runs on Python 3
    - Necessary packages are listed in the file "requirements.txt"  
- Code files can be run in the following order to replicate: 
    - (1) dct_mapping (*sets up organization of dataset*)
    - (2) special_treatments (*sets up organization of dataset*) 
    - (3) clsSource (*sets up organization of dataset*)
    - (4) setup_plots (*includes functions used across most plots*)
    - (5) plots_dataset_overview (*includes plots for summary statistics*)
    - (6) plots_aptitude_measures (*includes basic plots for aptitude measures*)

### Attributions 
I draw base code from https://github.com/HumanCapitalAnalysis/nlsy-data. These contributors maintain a cleaned version of the National Longitudinal Survey of Youth 1979 (NLSY79). Much of the code--particularly for structuring the dataset--should be credited to the above linked contributors: Luis Wardenbach, Philipp Eisenhauer, Sebastian Becker, and @bekauf.
https://github.com/HumanCapitalAnalysis/nlsy-data

License for the code can be found in the LICENCE file.
