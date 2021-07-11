
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
import pickle
import pandas as pd
import numpy as np
import shlex
from numpy.testing import assert_equal
from pathlib import Path


# %%
proj_dir = Path(os.path.abspath(''))
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
    dct_full.update(process_school_enrollment_monthly())

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
        substrings = 'HOURLY RATE OF PAY JOB #0' + str(i)
        dct['WAGE_HOURLY_JOB_' + str(i)] = get_year_name(substrings)

    # TOTAL INCOME FROM MILITARY SERVICE
    substrings = 'TOTAL INCOME FROM MILITARY SERVICE'
    dct['INCOME_MILITARY'] = get_year_name(substrings)
    
    # TOTAL INCOME FROM WAGES AND SALARY 
    substrings = 'TOTAL INCOME FROM WAGES AND SALARY'
    dct['INCOME_WAGES_SALARY'] = get_year_name(substrings)
    
    #POVERTY STATUS 
    substrings = 'FAMILY POVERTY STATUS IN PREVIOUS CALENDAR YEAR'
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
# This function processes information on the highest degree ever received. There are
# two different variables in some years with the same information.
def process_highest_degree_received():

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


# %%
# This function processes the monthly school enrollment data. This is surprisingly
# difficult as, for example, information about March 1990 is asked in the 1990 and 1991 surveys.
def process_school_enrollment_monthly():

    # Search for the information in the short description file.  
    def read_school_enrollment_monthly():

        rslt = dict()
        with open(proj_dir / 'data/input/all-variables.sdf', 'r') as infile:
            for line in infile.readlines():
                is_relevant = 'MONTHS ENROLLED IN SCHOOL SINCE LAST INT' in line
                is_relevant = np.all(is_relevant)

                if not is_relevant:
                    continue

                list_ = shlex.split(line)

                # Collect information
                variable, month = list_[0].replace('.', ''), list_[10]

                if 'R09052.00' in line:
                    month, year = list_[12], int(list_[13])
               
                # There are some typos in the variable descriptions
                elif 'INT-' in line:
                    month, year = list_[9], int(list_[10])
                else:
                    year = int(list_[11])

                # The labeling convention for year is all over the place. For example 2012
                # shows up as 12 as well.
                if 0 <= year < 25:
                    year += 2000
                elif 70 < year < 100:
                    year += 1900
                else:
                    pass

                # The labeling convention for the month is also inconsistent.
                if 'JAN' in month:
                    month = 'JANUARY'
                elif 'FEB' in month:
                    month = 'FEBRUARY'
                elif 'MAR' in month:
                    month = 'MARCH'
                elif 'APR' in month:
                    month = 'APRIL'
                elif 'MAY' in month:
                    month = 'MAY'
                elif 'JUN' in month:
                    month = 'JUNE'
                elif 'JUL' in month:
                    month = 'JULY'
                elif 'AUG' in month:
                    month = 'AUGUST'
                elif 'SEP' in month:
                    month = 'SEPTEMBER'
                elif 'OCT' in month:
                    month = 'OCTOBER'
                elif 'NOV' in month:
                    month = 'NOVEMBER'
                elif 'DEC' in month:
                    month = 'DECEMBER'
                else:
                    raise AssertionError

                if year not in rslt.keys():
                    rslt[year] = dict()
                if month not in rslt[year].keys():
                    rslt[year][month] = []

                rslt[year][month] += [variable]

        return rslt

    rslt = read_school_enrollment_monthly()
    dct = dict()
    for year in rslt.keys():
        for month in rslt[year].keys():
            for val in rslt[year][month]:
                label = 'ENROLLED_SCHOOL_' + month + '_1'

                if label in dct.keys():
                    if year in dct[label].keys():
                        label = 'ENROLLED_SCHOOL_' + month + '_2'

                if label not in dct.keys():
                    dct[label] = dict()

                dct[label][year] = val

    return dct

# %% [markdown]
# The following section contains some functionality for special treatment that is required for a
# selected few variables. 

# %%
def aggregate_highest_degree_received(df):
    """ This function merges the information about the highest degree ever received,
     sometimes collected under two variable names but never with conflicting information.
     At least one of the two variables is always a missing value.
    """    
    label = 'HIGHEST_DEGREE_RECEIVED'

    # This assignment rule simply takes the first assignment and then tries to replace it with
    # the second if the first is a missing value.
    df[label] = df['HIGHEST_DEGREE_RECEIVED_1']

    cond = df[label].isnull()
    df.loc[cond, label] = df['HIGHEST_DEGREE_RECEIVED_2']

    return df


# %%
def cleaning_highest_grade_attended(df):
    """ The variable for highest grade attended contains a value 95 
    which corresponds to UNGRADED.
    """
    cond = df['HIGHEST_GRADE_ATTENDED'] == 95
    df.loc[cond, 'HIGHEST_GRADE_ATTENDED'] = np.nan

    return df


# %%
def aggregate_school_enrollment_monthly(df):
    """ This function merges information about monthly school enrollment, sometimes
     collected twice due the differing time an individual is interviewed that year.
    """
    months = []
    months += ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST']
    months += ['SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

    for month in months:
        label = 'ENROLLED_SCHOOL_' + month
        df[label] = np.nan

        df[label] = df['ENROLLED_SCHOOL_' + month + '_1']

        cond = df[label].isnull()
        df.loc[cond, label] = df['ENROLLED_SCHOOL_' + month + '_2']

        # It also appears that sometimes the indicator that an individual was attending school that
        # month takes values different from one. However, SELECTED is always positive and NOT
        # SELECTED is always zero.
        cond = df[label] == 0
        df.loc[cond, label] = 0

        cond = df[label] > 0
        df.loc[cond, label] = 1

    return df


# %%
def create_is_interviewed(df):
    """This function creates an indicator that evaluates to TRUE if an individual
    was interviewed that year based on the information about the reasons for non-interviews. 
    """
    df['IS_INTERVIEWED'] = df['REASON_NONINTERVIEW'].fillna(0) == 0

    for year in [1995, 1997, 1999, 2001, 2003, 2005, 2007, 2009, 2011]:
        df.loc[(slice(None), year), 'IS_INTERVIEWED'] = False

    return df


# %%
def standarize_employer_information(df):
    """This function merges the employer-specific information on an individual's occupation
    using the 70 CPS codes into a new variable. See additional information at:
    https://www.nlsinfo.org/content/cohorts/nlsy79/topical-guide/employment/jobs-employers
    """
    # Create a set of new variables to signal to users that a modification took place.
    for i in range(1, 6):
        df['OCCALL70_MOD_JOB_' + str(i)] = df['OCCALL70_JOB_' + str(i)]

    # The information on #1 is missing in 1979 and 1993, as it is identical with CPSOCC70.
    for year in [1979, 1993]:
        cond = df['SURVEY_YEAR'] == year
        df.loc[cond, 'OCCALL70_MOD_JOB_1'] = df.loc[cond, 'CPSOCC70']

    # For the years 1980 - 1992 there is an indicator variable that maps the CPSOCC70 information
    # to the OCCALL70 variable.

    # NOTE: There are two open questions that are ignored here: (1) There exist two variables in
    # 1990 that read ``INT CHECK - IS JOB #01 SAME AS CURRENT JOB?'' (R3340000, R3342400). The
    # realizations of both variables are not identical. (2) There exist a few individuals where
    # the CPSOCC indicator takes value one for more than one of the 5 OCCALL70 variables. 
    for i in range(1, 6):
        cond = (df['CPS_JOB_INDICATOR_JOB_' + str(i)] == 1)
        df.loc[cond, 'OCCALL70_MOD_JOB_' + str(i)] = df.loc[cond, 'CPSOCC70']

    return df


# %%
def calculate_afqt_scores(df):
    """This function calculates the Aptitude, Achievement, and Intelligence (AFQT) scores, 
    with the Numerical Operations score adjusted along the lines described in NLS Attachment 106. 
    For more details, see information at: 
    https://www.nlsinfo.org/content/cohorts/nlsy79/topical-guide/education/aptitude-achievement-intelligence-scores
    """
    df['NUMERICAL_ADJ'] = df['ASVAB_NUMERICAL_OPERATIONS']

    adjust_no = {0: 0, 1: 0, 2: 1, 3: 2, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 14, 13: 15, 14: 16,
        15: 17, 16: 18, 17: 19, 18: 21, 19: 22, 20: 23, 21: 24, 22: 25, 23: 26, 24: 27, 25: 28,
        26: 29, 27: 30, 28: 31, 29: 33, 30: 34, 31: 35, 32: 36, 33: 37, 34: 38, 35: 39, 36: 39,
        37: 40, 38: 41, 39: 42, 40: 43, 41: 44, 42: 45, 43: 46, 44: 47, 45: 48, 46: 49, 47: 49,
        48: 50, 49: 50, 50: 50}

    df['NUMERICAL_ADJ'].replace(adjust_no, inplace=True)

    df['AFQT_RAW'] = 0.00
    df['AFQT_RAW'] += df['ASVAB_ARITHMETIC_REASONING']
    df['AFQT_RAW'] += df['ASVAB_WORD_KNOWLEDGE']
    df['AFQT_RAW'] += df['ASVAB_PARAGRAPH_COMPREHENSION']
    df['AFQT_RAW'] += 0.5 * df['NUMERICAL_ADJ']

    del df['NUMERICAL_ADJ']
    
    # There are a few variables which can be used to compute AFQT_RAW while there is no AFQT_1
    # available. The variable AFQT_1 is set to NAN by the NLSY team if the test procedure was
    # altered, i.e. variable R06148 (ASVAB_ALTERED_TESTING) takes value 67. However, those who maintain
    # the cleaned version of this dataset noticed there are other indicators of problems as well.
    #
    #   PROFILES, ASVAB VOCATIONAL TEST - NORMAL/ALTERED TESTING
    #
    #       11625   51      COMPLETED
    #          41   52      COMP-CONVERTED REFUSAL
    #         127   53      COMP-PROBLEM REPORTED
    #          85   54      COMP-SPANISH INSTR. CARDS
    #          36   67      COMP-PRODECURES ALTERED
    #
    # They followed up with the NLSY staff for guidance on how to deal with 51, 52, 53,
    # 54. The correspondence is available in ``correspondence-altered-testing.pdf'' in the sources
    # subdirectory of their github page. In short, detailed info isn't available anymore on the 
    # meaning of the different realizations. They follow the original decision of the NLSY staff
    # to only set 67 to NAN.
    cond = df['ASVAB_ALTERED_TESTING'].isin([67])
    df.loc[cond, 'AFQT_RAW'] = np.nan

    # This unit test reconstructs the AFQT_1 variable from the inputs.
    assert_equal(_test_afqt(df), True)

    return df


# %%
def aggregate_birth_information(df):
    """ This function aggregates the birth information collected in 1979 and 1981. For more
    details, see information at:
    https://www.nlsinfo.org/content/cohorts/nlsy79/topical-guide/household/age
    """
    # This method constructs the correct birth variable for each agent.
    def _construct_birth_info(agent):

        # Store the original information for now for debugging and testing purposes.
        for substring in ['YEAR_OF_BIRTH', 'MONTH_OF_BIRTH']:
            for year in [1979, 1981]:
                agent[substring + '_' + str(year)] = agent[substring][:, year].values[0]
            # Start with a clean slate that always prefers the information from 1981
            agent[substring] = np.nan
            agent[substring] = agent[substring + '_1981']
            # If no information in 1981 is available, fall back to 1979.
            if agent[substring].isnull().values.any():
                agent[substring] = agent[substring + '_1979']

        return agent

    df = df.groupby('IDENTIFIER').apply(_construct_birth_info)

    # Apply some basic tests to ensure that the computation was correct.
    for substring in ['YEAR_OF_BIRTH', 'MONTH_OF_BIRTH']:
        # There cannot be any missing values in the birth variables.
        assert not df[substring].isnull().any()
        # Whenever there is not a missing value in for 1981 then the columns should be identical.
        # For the others it should be identical to 1979.
        cond = (df[substring + '_1981'].notnull())
        assert df.loc[cond, substring].equals(df.loc[cond, substring + '_1981'])
        assert df.loc[~cond, substring].equals(df.loc[~cond, substring + '_1979'])

    # There's no need to keep track of the intermediate variables.
    for substring in ['YEAR_OF_BIRTH', 'MONTH_OF_BIRTH']:
        for year in [1979, 1981]:
            del df[substring + '_' + str(year)]

    df['YEAR_OF_BIRTH'] += 1900

    return df


# %%
def _test_afqt(df):
    """ NLSY provides percentile information for AFQT scores, reconstructed here 
    as a check based on NLSY instructions.
    """
    # Breaking the logic of the code a bit, only work with copies of the object here.
    df_internal = df.copy(deep=True)

    # Adjust for missing values, even though this is done later in the code for all variables.
    for label in ['AFQT_RAW', 'AFQT_1']:
        cond = (df_internal[label] < 0)
        df_internal.loc[cond, label] = np.nan

    # Match ``AFQT_RAW`` to percentile of distribution
    cond = df_internal['AFQT_RAW'] <= 23.5
    df_internal.loc[cond, 'AFQT_PERCENTILES'] = 1

    infos = []
    infos += [(23.50, 27.00, 2), (27.00, 29.50, 3), (29.50, 32.00, 4), (32.00, 34.00, 5)]
    infos += [(34.00, 36.50, 6), (36.50, 38.00, 7), (38.00, 40.00, 8), (40.00, 41.00, 9)]

    infos += [(41.00, 42.50, 10), (42.50, 44.00, 11), (44.00, 45.50, 12), (45.50, 47.00, 13)]
    infos += [(47.00, 48.50, 14), (48.50, 49.50, 15), (49.50, 51.00, 16), (51.00, 52.50, 17)]

    for i in range(18, 29):
        infos += [(i + 34.50, i + 35.50, i)]

    infos += [(63.50, 64.00, 29), (64.00, 65.00, 30), (65.00, 65.50, 31), (65.50, 66.50, 32)]
    infos += [(66.50, 67.00, 33), (67.00, 67.50, 34), (67.50, 68.50, 35), (68.50, 69.00, 36)]
    infos += [(69.00, 69.50, 37), (69.50, 70.50, 38), (70.50, 71.00, 39), (71.00, 71.50, 40)]
    infos += [(71.50, 72.00, 41), (72.00, 73.00, 42), (73.00, 73.50, 43), (73.50, 74.00, 44)]
    infos += [(74.00, 74.50, 45), (74.50, 75.50, 46), (75.50, 76.00, 47), (76.00, 76.50, 48)]
    infos += [(76.50, 77.50, 49)]

    for i, j in enumerate(range(50, 62), 1):
        infos += [(j + 28.00 - 0.50 * i, j + 28.00, j)]

    for i, j in enumerate(range(62, 94), 1):
        infos += [(j + 21.50 - 0.50 * i,  j + 21.50, j)]

    infos += [(99.00, 100.00, 94)]

    for i, j in enumerate(range(95, 98), 1):
        infos += [(j + 5.50 - 0.50 * i, j + 5.50, j)]

    infos += [(101.50, 102.50, 98), (102.5, 105.00, 99)]

    for info in infos:
        lower, upper, value = info
        cond = (df_internal['AFQT_RAW'] > lower) & (df_internal['AFQT_RAW'] <= upper)
        df_internal.loc[cond, 'AFQT_PERCENTILES'] = value

    return df_internal['AFQT_PERCENTILES'].equals(df_internal['AFQT_1'])

# %% [markdown]
# Finally, this model is a maintained list of all variables processed for the panel and checked via testing. 

# %%
# This maintained list contains all variables processed for the panel. 
TIME_CONSTANT = []
TIME_CONSTANT += ['IDENTIFIER', 'RACE', 'GENDER']
TIME_CONSTANT += ['ASVAB_ARITHMETIC_REASONING', 'ASVAB_WORD_KNOWLEDGE', 'ASVAB_ALTERED_TESTING']
TIME_CONSTANT += ['ASVAB_PARAGRAPH_COMPREHENSION', 'ASVAB_NUMERICAL_OPERATIONS']
TIME_CONSTANT += ['AFQT_1', 'SAMPLE_ID', 'ROTTER_SCORE', 'ROTTER_1', 'ROTTER_2']
TIME_CONSTANT += ['ROTTER_3', 'ROTTER_4', 'ROSENBERG_SCORE', 'ROSENBERG_1', 'ROSENBERG_2']
TIME_CONSTANT += ['ROSENBERG_3', 'ROSENBERG_4', 'ROSENBERG_5', 'ROSENBERG_6', 'ROSENBERG_7']
TIME_CONSTANT += ['ROSENBERG_8', 'ROSENBERG_9', 'ROSENBERG_10']
TIME_CONSTANT += ['HIGHEST_GRADE_COMPLETED_FATHER', 'HIGHEST_GRADE_COMPLETED_MOTHER']

TIME_VARYING = []
TIME_VARYING += ['ENROLLMENT_STATUS', 'YEAR_OF_BIRTH', 'CPSOCC70']
TIME_VARYING += ['MONTH_OF_BIRTH', 'HIGHEST_GRADE_COMPLETED', 'SURVEY_YEAR']
TIME_VARYING += ['INCOME_MILITARY', 'REASON_NONINTERVIEW', 'HIGHEST_GRADE_ATTENDED']
TIME_VARYING += ['HIGHEST_DEGREE_RECEIVED_1', 'HIGHEST_DEGREE_RECEIVED_2']
TIME_VARYING += ['INCOME_WAGES_SALARY', 'POVSTATUS', 'AMT_WORK_LMT']
TIME_VARYING += ['TYPE_WORK_LMT','HEALTH_INS', 'MAR_STATUS', 'REGION']


# %%
for start in ['EMP_HOURS_WK_', 'EMP_STATUS_WK_']:
    for week in ['1', '7', '13', '14', '20', '26', '40', '46', '52']:
        TIME_VARYING += [start + week]


# %%
for start in ['WAGE_HOURLY_JOB_', 'CPS_JOB_INDICATOR_JOB_', 'OCCALL70_JOB_']:
    for job in ['1', '2', '3', '4', '5']:
        TIME_VARYING += [start + job]


# %%
months = []
months += ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER']
months += ['OCTOBER', 'NOVEMBER', 'DECEMBER']
for month in months:
    for idx in ['1', '2']:
        TIME_VARYING += ['ENROLLED_SCHOOL_' + month + '_' + idx]


# %%
# These variables are created during processing. These are part of a separate list as they are
# not available when the data is transformed from wide to long format.
DERIVED_VARS = []
DERIVED_VARS += ['AFQT_RAW', 'IS_INTERVIEWED', 'HIGHEST_DEGREE_RECEIVED']


# %%
for start in ['OCCALL70_MOD_JOB_']:
    for job in ['1', '2', '3', '4', '5']:
        DERIVED_VARS += [start + job]


# %%
for month in months:
    DERIVED_VARS += ['ENROLLED_SCHOOL_' + month]


# %%
class SourceCls(object):
    """This class contains all methods that prepare the source dataset for further uses.
    """
    def __init__(self):
        # Class attributes
        self.survey_years = None
        self.source_wide = None
        self.source_long = None
        self.dct = None
    
    def read_source(self, num_agents=None):
        """Read the original file from the NLS Investigator
        """
        self.source_wide = pd.read_csv(r'C:\Users\bec10\OneDrive\Desktop\files\repos\gorman-earlyjobskills-analysis\code\data\input\all-variables.csv', nrows=num_agents)

        # Process variable dictionary
        survey_years, dct = get_mappings()

        # Attach results as class attributes
        self.survey_years = survey_years
        self.dct = dct

    # Add some basic variables that are easily constructed from the original information
    # and frequently used during finer processing of the data.
    def add_basic_variables(self):

        # Distribute class attributes
        source_long = self.source_long

        # Processing birth information is not as straightforward as one might think.
        source_long = aggregate_birth_information(source_long)

        # Compute the AFQT score as suggested in the data documentation.
        source_long = calculate_afqt_scores(source_long)

        # There are no missing values for all these variables, so integer type can be enforced.
        for varname in ['MONTH_OF_BIRTH', 'YEAR_OF_BIRTH']:
            source_long[varname] = source_long[varname].astype('int64')

        source_long = aggregate_school_enrollment_monthly(source_long)
        source_long = aggregate_highest_degree_received(source_long)
        source_long = cleaning_highest_grade_attended(source_long)
        source_long = standarize_employer_information(source_long)
        source_long = create_is_interviewed(source_long)

        self.source_long = source_long

    # Transform from wide to long format.    
    def transform_wide_to_panel(self):

        # Distribute class attributes
        survey_years = self.survey_years
        source_wide = self.source_wide
        dct = self.dct

        # Change from the original wide format to the typical panel structure
        self.source_long = wide_to_long(source_wide, survey_years, dct)
        self._set_missing_values()

    # Ensure a uniform treatment of missing values.    
    def _set_missing_values(self):
 
        # Distribute class attributes
        source_long = self.source_long

        # In the original dataset, missing values are indicated by negative values
        for varname in TIME_VARYING + TIME_CONSTANT:
            cond = source_long[varname] < 0
            if np.sum(cond) > 0:
                source_long.loc[cond, varname] = np.nan

    # Perform some basic consistency checks for the constructed panel.
    def testing(self):
      
        # Distribute class attributes
        source_long = self.source_long

        # There are several variables where there cannot be a missing value.
        varnames = []
        varnames += ['IDENTIFIER', 'RACE', 'GENDER', 'MONTH_OF_BIRTH', 'YEAR_OF_BIRTH']
        varnames += ['SURVEY_YEAR']
        for varname in varnames:
            np.testing.assert_equal(source_long[varname].notnull().all(), True)
    
        # The same is true for the all EMP_STATUS_ variables. In R26.1 there is one individual
        # which in fact does have missing values in their employment status.
        subset = source_long.drop(9269, level='Identifier')
        np.testing.assert_equal(subset.filter(regex='EMP_STATUS_*').notnull().all().all(), True)
        
        # For all EMP_HOURS_ variables, we know that non-missing values need to be positive.
        assert source_long.filter(regex='EMP_HOURS_*').apply(lambda column: (column[column.notnull()] >= 0).all()).all()
    
        # There are several variables which are not supposed to vary over time.
        varnames = []
        varnames += ['IDENTIFIER', 'RACE', 'GENDER', 'MONTH_OF_BIRTH', 'YEAR_OF_BIRTH', 'AFQT_1']
        varnames += ['AFQT_RAW', 'ASVAB_ALTERED_TESTING', 'SAMPLE_ID']
        for varname in varnames:
            np.testing.assert_equal((source_long[varname].notnull().groupby(
                level='Identifier').std() == 0).all(), True)

        # The distribution of race is known from the NLSY website.
        values = source_long['RACE'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([7510, 3174, 2002], values)
    
        # The distribution of gender is known from the NLSY website.
        values = source_long['GENDER'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([6403, 6283], values)

        # The distribution of sample identifiers is known from the NLSY website.
        values = source_long['SAMPLE_ID'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([2279, 2236, 1105, 1067, 901, 751, 742, 729, 609, 405,
                                        346, 342, 226, 218, 203, 198, 162, 89, 53, 25], values)

        # A bit about the AFQT_1 variable is known from the codebook.
        stat = source_long['AFQT_1'].groupby(level='Identifier').first().isnull().sum()
        np.testing.assert_equal(stat, 808)
        stat = (source_long['AFQT_1'].min(), source_long['AFQT_1'].max())
        np.testing.assert_equal(stat, (1, 99))
        stat = source_long['AFQT_1'].mean()
        np.testing.assert_equal(stat, 40.906044788684966)

        # ASVAB_ALTERED_TESTING
        values = source_long.groupby(level='Identifier').first()['ASVAB_ALTERED_TESTING'].value_counts().values
        np.testing.assert_equal([11625, 127, 85, 41, 36], values)

        # We know that CPSOCC70 is used to impute OCCALL70_MOD_JOB_1 in 1979 and 1993.
        for year in [1979, 1993]:
            cond = source_long['CPSOCC70'][:, year].equals(source_long['OCCALL70_MOD_JOB_1'][:, year])
            np.testing.assert_equal(cond, True)

        '''Check the distribution of selected variables at random.
        '''
        
        # HIGHEST_DEGREE_RECEIVED
        cases = []
        cases += [(1988, (6031, 922, 626, 587, 178, 160, 49, 11))]
        cases += [(1996, (60, 36, 29, 24, 10, 2, 1))]
        cases += [(2010, (4025, 976, 728, 708, 442, 394, 178, 49, 47))]

        for case in cases:
            year, rslt = case
            label = 'HIGHEST_DEGREE_RECEIVED'
            np.testing.assert_equal(source_long[label][:, year].value_counts().values, rslt)

        # HIGHEST_GRADE_ATTENDED
        cases = []
        cases += [(1984, (352, 212, 212, 201, 108, 61, 21, 15, 10, 10, 6, 4))]
        cases += [(1994, (72, 61, 59, 34, 34, 33, 31, 17, 9, 7, 6, 5, 4, 1))]
        cases += [(2002, (94, 64, 61, 51, 51, 37, 35, 22, 16, 9, 6, 4, 2, 1))]

        for case in cases:
            year, rslt = case
            label = 'HIGHEST_GRADE_ATTENDED'
            np.testing.assert_equal(source_long[label][:, year].value_counts().values, rslt)

        # SCHOOL_ENROLLMENT MONTHLY
        cases = []
        cases += [(2011, 'JANUARY', '1', (188, 156))]
        cases += [(1980, 'APRIL', '1', (5353,))]
        cases += [(1994, 'JUNE', '1', (490, 232))]

        for case in cases:
            year, month, idx, rslt = case
            label = 'ENROLLED_SCHOOL_' + month + '_' + idx
            np.testing.assert_equal(source_long[label][:, year].value_counts().values, rslt)

        # IS_INTERVIEWED
        cases = []
        cases += [(1980, (12141, 545))]
        cases += [(1994, (8891, 3795))]
        cases += [(2000, (8032, 4654))]

        for case in cases:
            year, rslt = case
            stat = source_long['IS_INTERVIEWED'].groupby('Survey Year').value_counts()[year].values
            np.testing.assert_equal(stat, rslt)

        # CPSOCC70
        cases = []
        cases += [[(1979, source_long), (173, 104, 345, 1038, 403, 0, 785, 615, 9, 181, 1295, 253)]]
        cases += [[(1988, source_long), (1356, 966, 415, 1825, 1016, 0, 1274, 617, 14, 113, 1271, 122)]]
        cases += [[(1993, source_long), (1276, 909, 313, 1393,  857, 1,  942, 557, 24, 47, 1171, 60)]]

        for case in cases:
            args, rslt = case
            np.testing.assert_almost_equal(rslt, cpsocc_counts(*args))

        # OCCALL70
        cases = []
        cases += [[(1988, 1, source_long), (24, 6, 5, 15, 8, 0, 10, 9, 0, 2, 32, 2)]]
        cases += [[(1993, 3, source_long), (43, 18, 16, 51, 35, 1, 47, 23, 1, 1, 68, 3)]]
        cases += [[(2000, 5, source_long), (8, 8, 1, 7, 15, 0, 17, 8, 0, 1, 21, 0)]]

        for case in cases:
            args, rslt = case
            np.testing.assert_almost_equal(rslt, occall_counts(*args))

        # EMP_STATUS
        cases = []
        cases += [[(2007, 26, source_long), (6240, 4614, 38, 0, 321, 1464, 9)]]
        cases += [[(1997, 46, source_long), (7206, 3668, 16, 0, 258, 1464, 73)]]
        cases += [[(1987, 20, source_long), (8068, 1486, 65, 43, 554, 2171, 299)]]

        for case in cases:
            args, rslt = case
            np.testing.assert_almost_equal(rslt, emp_status_counts(*args))

        # EMP_HOURS
        cases = []
        cases += [[(1992, 14, source_long), (5697, 87, 194, 330, 762, 4009, 876, 379, 151, 74, 78, 0, 49)]]
        cases += [[(2009, 7, source_long), (6760, 79, 144, 280, 664, 3350, 707, 375, 147, 83, 23, 33, 41)]]
        cases += [[(2010, 52, source_long), (7170, 68, 111, 278, 558, 3061, 766, 356, 144, 68, 17, 44, 45)]]

        for case in cases:
            args, rslt = case
            np.testing.assert_almost_equal(rslt, emp_hours_counts(*args))

        # WAGE_HOURLY
        cases = []
        cases += [[(1979, 5, source_long), (0, 3, 6, 45, 26, 8, 1, 3, 0, 1, 0, 1)]]
        cases += [[(1988, 4, source_long), (0, 2, 2, 6, 59, 76, 67, 53, 42, 15, 10, 52)]]
        cases += [[(1991, 2, source_long), (0, 26, 44, 41, 97, 323, 327, 262, 180, 182, 119, 647)]]

        for case in cases:
            args, rslt = case
            np.testing.assert_almost_equal(rslt, wage_hourly_counts(*args))

        # Confirm that all included variables are mentioned at the beginning of the notebook.
        varnames = TIME_CONSTANT + TIME_VARYING + DERIVED_VARS
        np.testing.assert_equal(set(source_long.columns.values), set(varnames))

        # This ensures that there are no surprising changes to the dataset
        val = 8726642399.5
        np.testing.assert_equal(source_long.sum(numeric_only=True).sum(), val)

    # Store the dataset for further proccessing
    def store(self, fname):

        # Distribute class attributes
        source_long = self.source_long

        # Write out persistent storage
        source_long.to_pickle(fname)

    # Store the dataset for further processing.
    def load(self, fname):

        # Distribute class attributes
        self.source_long = pd.read_pickle(fname)

# %% [markdown]
# The original data is set up in wide format; the following allows for working with a typical panel structure.

# %%
def wide_to_long(source_wide, additional_level, dct):

    # Set up an empty dataframe with the right index structure. This setup maintains the mapping
    # between the index in the dataframe and the NLSY identifier.
    caseid = [x + 1 for x in source_wide.index]
    multi_index = pd.MultiIndex.from_product([caseid, additional_level], names=['Identifier', 'Survey Year'])
    pd_long = pd.DataFrame(index=multi_index)

    # It is useful to have a column that corresponds to each of the two indices.
    pd_long['IDENTIFIER'] = pd_long.index.get_level_values('Identifier')
    pd_long['SURVEY_YEAR'] = pd_long.index.get_level_values('Survey Year')

    for long_name in dct.keys():
        # Initialize the column with missing values.
        pd_long[long_name] = np.nan
        for year in additional_level:
            # Some variables might not be defined for each year. If that is the case,
            # missing values simply remain.
            if year not in dct[long_name].keys():
                continue
            # Now simply assign the variable name to the corresponding year.
            pd_long.loc[(slice(None), year), long_name] = source_wide[dct[long_name][year]].values

    # Some variables have no missing values and so integer type can be imposed.
    for varname in ['IDENTIFIER', 'SURVEY_YEAR', 'RACE', 'GENDER']:
        pd_long[varname] = pd_long[varname].astype('int64')

    return pd_long


# %%
# This function returns counts for each of the bins of the variable.
def cpsocc_counts(year, source_long):

    bins = []
    bins += [(1, 195), (201, 245), (260, 285), (301, 395), (401, 575), (580, 590)]
    bins += [(601, 715), (740, 785), (801, 802), (821, 824), (901, 965), (980, 984)]

    counts = _get_counts_year(source_long['CPSOCC70'], bins, year)

    return counts


# %%
# This function returns counts for each of the bins of the variable.
def occall_counts(year, num, source_long):

    bins = []
    bins += [(1, 195), (201, 245), (260, 285), (301, 395), (401, 575), (580, 590), (601, 715)]
    bins += [(740, 785), (801, 802), (821, 824), (901, 965), (980, 984)]

    counts = _get_counts_year(source_long['OCCALL70_JOB_' + str(num)], bins, year)

    return counts


# %%
# This function returns counts for each of the bins of the variable.
def wage_hourly_counts(year, num, source_long):

    bins = []
    bins += [(0, 1), (1, 99), (100, 199), (200, 299), (300, 399), (400, 499), (500, 599)]
    bins += [(600, 699), (700, 799), (800, 899), (900, 999), (1000, np.inf)]

    counts = _get_counts_year(source_long['WAGE_HOURLY_JOB_' + str(num)], bins, year)

    return counts


# %%
# This function returns counts for each of the bins of the variable.
def emp_hours_counts(year, week, source_long):

    bins = []
    bins += [(0, 0), (1, 9), (10, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69)]
    bins += [(70, 79), (80, 89), (90, 99), (100, np.inf)]

    label = 'EMP_HOURS_WK_' + str(week)
    counts = _get_counts_year(source_long[label], bins, year)
    counts += [source_long[label].loc[:, year].isnull().sum()]

    return counts


# %%
# This function returns counts for each of the bins of the variable.
def emp_status_counts(year, week, source_long):

    bins = []
    bins += [(100, np.inf), (0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (7, 7)]

    counts = _get_counts_year(source_long['EMP_STATUS_WK_' + str(week)], bins, year)

    return counts


# %%
# This function returns counts for each of the bins of the variable.
def _get_counts_year(series, bins, year):
    
    counts = []
    for bounds in bins:
        lower, upper = bounds
        counts += [series.loc[:, year].between(lower, upper).sum()]

    return counts


# %%
source_object = SourceCls()
source_object.read_source()
source_object.transform_wide_to_panel()
source_object.add_basic_variables()
source_object.store('C:/OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis/code/data/output/full-list-variables.pkl') 

file_to_store = open('stored_object.pickle', 'wb')
pickle.dump(source_object, file_to_store)
file_to_store.close()

# my_pickled_object = pickle.dumps(my_object)
# print(f'This is my pickled object:\n{my_picked_object}\n')
# my_object.a_dict = None


# %%
#if __name__ == '__main__':

#    fname = proj_dir / 'OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis/code/data/output/full-list-variables.pkl'

#    source_obj = SourceCls()

#    source_obj.read_source()
#    source_obj.transform_wide_to_panel()
#   source_obj.add_basic_variables()
#    source_obj.store(fname)


#object = SourceCls()
#filehandler = open(fname, 'wb')
#pickle.dump(object, filehandler)




#    source_obj.load(fname)
#   source_obj.testing()


# %%
get_ipython().run_line_magic('debug', '')


# %%



