# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Processing the Data 
# %% [markdown]
# ### In this notebook, the data from the NLSY79 are cleaned and processed for further analysis.
# %% [markdown]
# I draw code for this notebook from https://github.com/HumanCapitalAnalysis/nlsy-data. These contributors maintain a cleaned version of the National Longitudinal Survey of Youth 1979 (NLSY79). A majority of the code below should be credited to the above linked contributors: Luis Wardenbach, Philipp Eisenhauer, Sebastian Becker, and @bekauf. 

# %%
import os
import pandas as pd
import numpy as np
import shlex
from pathlib import Path


# %%
os.chdir(r'c:/Users/bec10/OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis')
proj_dir = Path(os.path.abspath(""))
print(proj_dir)


# %%
def get_mappings():
    """Process a mapping of two separate cases: (1) variables that vary by year, and 
    (2) variables where there are multiple realizations each year. Start with 1978 
    as information about 1978 employment histories is collected with the initial 
    interview. Note that from 1996 on, the NLSY is generated every other year. 
    """
    # Set up grid for survey years. 
    years = range(1978, 2013)

    # Set up a dictionary for variables 
    dct_full = dict()

    dct_full.update(process_time_constant(years))
    dct_full.update(process_multiple_each_year())
    dct_full.update(process_single_each_year())
    dct_full.update(process_highest_degree_received())
    

    # Finishing
    return years, dct_full

# %%
def get_name(substrings):
    """Search through the variable descriptions in NLSY file by substrings. 
    """
    # Allow passing in a string or list of strings from the variable descriptions.
    if type(substrings) == str:
        substrings = [substrings]

    with open(proj_dir / 'data/input/all-variables.sdf', 'r') as infile:
        for line in infile.readlines():
            is_relevant = [substring in line for substring in substrings]
            is_relevant = np.all(is_relevant)
            if not is_relevant:
                continue
            # This special treatment is only required for the string that identifies RACE.
            line = line.replace("'", '')
            list_ = shlex.split(line)
            name = list_[0].replace('.', '')

            return name

    raise AssertionError('Substrings not found ...')


# %%
def get_year_name(substrings):
    """Search through the variable descriptions in NLSY file by substrings. 
    """
    # Allow passing in a string or list of strings from the variable descriptions.
    if type(substrings) == str:
        substrings = [substrings]

    container = dict()
    with open(proj_dir / 'data/input/all-variables.sdf', 'r') as infile:
        for line in infile.readlines():
            is_relevant = [substring in line for substring in substrings]
            is_relevant = np.all(is_relevant)
            if is_relevant:
                list_ = shlex.split(line)
                name = list_[0].replace('.', '')
                year = int(list_[1])
                container[year] = name

    return container


# %%
def process_time_constant(years):
    """Process time-constant variables.
    """    
    dct_constant = dict()

    dct_constant['RACE'] = dict()
    substrings = 'RACIAL/ETHNIC COHORT FROM SCREENER'
    for year in years:
        dct_constant['RACE'][year] = get_name(substrings)

    dct_constant['IDENTIFIER'] = dict()
    substrings = 'CASEID'
    for year in years:
        dct_constant['IDENTIFIER'][year] = get_name(substrings)

    dct_constant['SAMPLE_ID'] = dict()
    substrings = 'SAMPLE_ID'
    for year in years:
        dct_constant['SAMPLE_ID'][year] = get_name(substrings)

    dct_constant['GENDER'] = dict()
    substrings = 'SEX OF R'
    for year in years:
        dct_constant['GENDER'][year] = get_name(substrings)

    dct_constant['HIGHEST_GRADE_COMPLETED_FATHER'] = dict()
    substrings = 'HGC-FATHER'
    for year in years:
        dct_constant['HIGHEST_GRADE_COMPLETED_FATHER'][year] = get_name(substrings)

    dct_constant['HIGHEST_GRADE_COMPLETED_MOTHER'] = dict()
    substrings = 'HGC-MOTHER'
    for year in years:
        dct_constant['HIGHEST_GRADE_COMPLETED_MOTHER'][year] = get_name(substrings)
        
    '''EMOTIONAL / APTITUDE / INTELLIGENCE SCORES 
    '''    
    # ROTTER'S LOCUS OF CONTROL SCALE 
    dct_constant['ROTTER_SCORE'] = dict()
    substrings = 'ROTTER SCALE SCORE'
    for year in years:
        dct_constant['ROTTER_SCORE'][year] = get_name(substrings)

    for i in range(1, 5):
        label = 'ROTTER_' + str(i)
        substrings = 'ROTTER-' + str(i) + 'A'
        dct_constant[label] = dict()
        for year in years:
            dct_constant[label][year] = get_name(substrings)
            
    # ROSENBERG SELF-ESTEEM SCORE 
    dct_constant['ROSENBERG_SCORE'] = dict()
    substrings = 'SELF-ESTEEM SCORE'
    for year in years:
        dct_constant['ROSENBERG_SCORE'][year] = get_name(substrings)

    for i in range(1, 11):
        label = 'ROSENBERG_' + str(i)
        substrings = 'R030' + str(i + 34) + '.00'
        dct_constant[label] = dict()
        for year in years:
            dct_constant[label][year] = get_name(substrings)

    # ARMED SERVICES VOCATIONAL APTITUDE BATTERY (ASVAB)
    # The ASVAB is a well-known aptitude test that is used for career exploration, given
    # in high schools, community colleges, at job corps centers, and at correctional facilities.
    dct_constant['ASVAB_ARITHMETIC_REASONING'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 2-ARITHMETIC REASONING'
    for year in years:
        dct_constant['ASVAB_ARITHMETIC_REASONING'][year] = get_name(substrings)

    dct_constant['ASVAB_WORD_KNOWLEDGE'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 3-WORD KNOWLEDGE'
    for year in years:
        dct_constant['ASVAB_WORD_KNOWLEDGE'][year] = get_name(substrings)

    dct_constant['ASVAB_PARAGRAPH_COMPREHENSION'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 4-PARAGRAPH COMP'
    for year in years:
        dct_constant['ASVAB_PARAGRAPH_COMPREHENSION'][year] = get_name(substrings)

    dct_constant['ASVAB_NUMERICAL_OPERATIONS'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 5-NUMERICAL OPERATIONS'
    for year in years:
        dct_constant['ASVAB_NUMERICAL_OPERATIONS'][year] = get_name(substrings)

    dct_constant['ASVAB_ALTERED_TESTING'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - NORMAL/ALTERED TESTING'
    for year in years:
        dct_constant['ASVAB_ALTERED_TESTING'][year] = get_name(substrings)

    dct_constant['AFQT_1'] = dict()
    substrings = 'PROFILES, ARMED FORCES QUALIFICATION TEST (AFQT) PERCENTILE SCORE - 1980'
    for year in years:
        dct_constant['AFQT_1'][year] = get_name(substrings)

    return dct_constant


# %%
def process_multiple_each_year():
    """Process variables with multiple each year--
    specifically, employment status for multiple weeks.
    """
    dct_multiple = dict()

    # The mapping between the continuous weeks counter and the calendar year is provided on the
    # NLSY website.
    mapping_continuous_week = pd.read_pickle(proj_dir / 'data/input/continuous_week_crosswalk_2012.pkl')
    years = mapping_continuous_week['Week Start: \nYear'].unique()

    # Prepare container
    year_weeks = dict()
    for year in years:
        year_weeks[year] = []

    for index, row in mapping_continuous_week.iterrows():
        year = row['Week Start: \nYear']
        year_weeks[year] += [row['Continuous \nWeek Number']]

    # Process employment information for some selected weeks.
    weeks = [1, 7, 13, 14, 20, 26, 40, 46, 52]

    for type_ in ['STATUS', 'HOURS']:
        for week in weeks:
            label, idx = 'EMP_' + type_ + '_WK_' + str(week), week - 1
            dct_multiple[label] = dict()
            for year in years:
                substring = 'WEEK ' + str(year_weeks[year][idx])
                if type_ == 'STATUS':
                    substrings = ['LABOR FORCE STATUS', substring]
                elif type_ == 'HOURS':
                    substrings = ['HOURS AT ALL JOBS', substring]
                else:
                    raise AssertionError
                dct_multiple[label][year] = get_name(substrings)

    return dct_multiple


# %%
def process_single_each_year():
    """Process variables that vary by year (i.e. one variable measured each year).
    """
    # Initialize containers
    dct = dict()

    
    ''' EDUCATION
    '''
    substrings = 'HIGHEST GRADE ATTENDED'
    dct['HIGHEST_GRADE_ATTENDED'] = get_year_name(substrings)

    substrings = 'HIGHEST GRADE COMPLETED AS'
    dct['HIGHEST_GRADE_COMPLETED'] = get_year_name(substrings)
    

    ''' MONTH/YEAR OF BIRTH
    '''
    substrings = 'DATE OF BIRTH - YEAR'
    dct['YEAR_OF_BIRTH'] = get_year_name(substrings)

    substrings = 'DATE OF BIRTH - MONTH'
    dct['MONTH_OF_BIRTH'] = get_year_name(substrings)
    

    ''' OCCUPATION INFORMATION 
    '''
    # CPSOCC70
    substrings = 'OCCUPATION AT CURRENT JOB/MOST RECENT JOB (70 CENSUS 3 DIGIT)'
    dct['CPSOCC70'] = get_year_name(substrings)

    # OCCALL70
    for i in range(1, 6):
        substrings = ['OCCUPATION (CENSUS 3 DIGIT, 70 CODES)', 'JOB #0' + str(i)]
        dct['OCCALL70_JOB_' + str(i)] = get_year_name(substrings)

    # In the year 1993, the substring is changed for some reason and cannot be easily
    # distinguished from the CPSOCC70 variable.
    for i in range(2, 6):
        substrings = 'OCCUPATION (CENSUS 3 DIGIT) JOB #0' + str(i)
        dct['OCCALL70_JOB_' + str(i)].update(get_year_name(substrings))

    # In the year 1982, the substring for the fourth job contains a 0 instead of an O.
    substrings = ['OCCUPATION (CENSUS 3 DIGIT, 70 C0DES)', 'JOB #04']
    dct['OCCALL70_JOB_4'].update(get_year_name(substrings))

    #LINKING OCALLEMP70 and CPSOCC7
    for i in range(1, 6):
        substrings = ['IS JOB #0' + str(i) + ' SAME AS CURRENT JOB?']
        dct['CPS_JOB_INDICATOR_JOB_' + str(i)] = get_year_name(substrings)
        

    '''INCOME AND WAGES 
    '''
    # HOURLY RATE OF PAY JOB ##
    for i in range(1, 6):
        substrings = ['HOURLY RATE OF PAY JOB #0' + str(i)]
        dct['WAGE_HOURLY_JOB_' + str(i)] = get_year_name(substrings)

    # TOTAL INCOME FROM MILITARY SERVICE
    substrings = 'TOTAL INCOME FROM MILITARY SERVICE'
    dct['INCOME_MILITARY'] = get_year_name(substrings)
    
    # TOTAL INCOME FROM WAGES AND SALARY 
    substrings = 'TOTAL INCOME FROM WAGES AND SALARY'
    dct['INCOME_WAGES_SALARY'] = get_year_name(substrings)
    
    # POVERTY STATUS 
    substrings = 'FAMILY POVERTY STATUS IN PRIOR YEAR'
    dct['POVSTATUS'] = get_year_name(substrings)
    
    
    '''HEALTH VARIABLES 
    '''
    substrings = 'DOES HEALTH LIMIT KIND OF WORK R CAN DO?'
    dct['AMT_WORK_LMT'] = get_year_name(substrings)
    
    substrings = 'DOES HEALTH LIMIT KIND OF WORK R CAN DO?'
    dct['TYPE_WORK_LMT'] = get_year_name(substrings)

    substrings = 'R COVERED BY ANY HEALTH/HOSPITAL PLAN'
    dct['HEALTH_INS'] = get_year_name(substrings)
    
        
    ''' OTHER VARIABLES
    '''
    # MARITAL STATUS 
    substrings = 'MARITIAL STATUS'
    dct['MAR_STATUS'] = get_year_name(substrings)
    
    # REGION OF RESIDENCE
    substrings = 'REGION OF CURRENT RESIDENCE'
    dct['REGION'] = get_year_name(substrings) 
    
    # REASON FOR NONINTERVIEW
    substrings = ['REASON FOR NONINTERVIEW']
    dct['REASON_NONINTERVIEW'] = get_year_name(substrings)
    
    # MILITARY ENROLLMENT STATUS AS OF MAY 1 SURVEY YEAR (REVISED)
    substrings = 'ENROLLMENT STATUS AS OF MAY 1 SURVEY YEAR (REVISED)'
    dct['ENROLLMENT_STATUS'] = get_year_name(substrings)

    return dct

# %%
def process_highest_degree_received():
    '''This function processes information on the highest degree ever received. There are
    two different variables in some years with the same information.
    '''
    # This method reads in the variable names for the highest grade received.
    def read_highest_degree_received():
        
        rslt = dict()
        with open(proj_dir / 'data/input/all-variables.sdf', 'r') as infile:
            for line in infile.readlines():
                is_relevant = 'HIGHEST DEGREE EVER RECEIVED' in line

                if not is_relevant:
                    continue

                list_ = shlex.split(line)
                variable, year = list_[0].replace('.', ''), int(list_[1])
                if year not in rslt.keys():
                    rslt[year] = []

                rslt[year] += [variable]

        return rslt

    rslt = read_highest_degree_received()

    dct = dict()
    for year in rslt.keys():
        for val in rslt[year]:
            label = 'HIGHEST_DEGREE_RECEIVED_1'
            if label in dct.keys():
                if year in dct[label].keys():
                    label = 'HIGHEST_DEGREE_RECEIVED_2'
            if label not in dct.keys():
                dct[label] = dict()
            dct[label][year] = val

    return dct
