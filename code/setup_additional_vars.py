""" This module creates or modifies some variables for analysis.
"""
# %%
import numpy as np
from numpy.testing import assert_equal


# %%
def create_is_interviewed(df):
    """This function creates an indicator evaluated TRUE if an individual was interviewed
    that year based on the information about the reasons for non-interviews. 
    """
    df['IS_INTERVIEWED'] = df['REASON_NONINTERVIEW'].fillna(0) == 0

    for year in [1995, 1997, 1999, 2001, 2003, 2005, 2007, 2009, 2011]:
        df.loc[(slice(None), year), 'IS_INTERVIEWED'] = False

    return df

# %%
def standarize_employer_information(df):
    """ This function merges the employer-specific information on an individual's occupation
    into a new variable using the CPS70 codes. See additional information at:
    https://www.nlsinfo.org/content/cohorts/nlsy79/topical-guide/employment/jobs-employers
    """
    # Create a set of new variables to signal to users that a modification took place.
    for i in range(1, 6):
        df['OCCALL70_MOD_JOB_' + str(i)] = df['OCCALL70_JOB_' + str(i)]

    # The information on #1 is missing in 1979 and 1993 as it is identical with CPSOCC70.
    for year in [1979, 1993]:
        cond = df['SURVEY_YEAR'] == year
        df.loc[cond, 'OCCALL70_MOD_JOB_1'] = df.loc[cond, 'CPSOCC70']

    # For the years 1980 - 1992 there is an indicator variable that maps the CPSOCC70 information
    # to the OCCALL70 variable.
    #
    # NOTE: There are two open questions that are ignored here: (1) There exist two variables in
    # 1990 that read ``INT CHECK - IS JOB #01 SAME AS CURRENT JOB?'' (R3340000, R3342400). The
    # realizations of both variables are not identical. (2) There are a few individuals where
    # the CPSOCC indicator takes a value of one for more than one of the 5 OCCALL70 variables. 
    for i in range(1, 6):
        cond = (df['CPS_JOB_INDICATOR_JOB_' + str(i)] == 1)
        df.loc[cond, 'OCCALL70_MOD_JOB_' + str(i)] = df.loc[cond, 'CPSOCC70']

    return df

# %%
def calculate_afqt_scores(df):
    """This function calculates the Aptitude, Achievement, and Intelligence (AFQT) scores, 
    with the Numerical Operations score adjusted along the lines described in NLSY Attachment 106. 
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

    # There are a couple of variables for which AFQT_RAW can be computed where there is no AFQT_1
    # available. The variable AFQT_1 is set to NAN by the NLSY team if the test procedure was
    # altered, i.e. if variable R06148 (ASVAB_ALTERED_TESTING) takes value 67. However, others have
    # noticed that there are additional issues/considerations as well.
    #
    #   PROFILES, ASVAB VOCATIONAL TEST - NORMAL/ALTERED TESTING
    #
    #       11625   51      COMPLETED
    #          41   52      COMP-CONVERTED REFUSAL
    #         127   53      COMP-PROBLEM REPORTED
    #          85   54      COMP-SPANISH INSTR. CARDS
    #          36   67      COMP-PRODECURES ALTERED
    #
    # NLSY staff, on guidance for how to deal with 51, 52, 53, and 54, essentially stated that detailed 
    # information is not available anymore on the meaning of the different realizations. 
    # This code chooses to follow the original decision of the NLSY staff to only set 67 to NAN.
    cond = df['ASVAB_ALTERED_TESTING'].isin([67])
    df.loc[cond, 'AFQT_RAW'] = np.nan

    # Unit test; reconstruct the AFQT_1 variable from the inputs.
    assert_equal(_test_afqt(df), True)

    return df

# %%
def aggregate_birth_information(df):
    """ This function aggregates the birth information that was collected in 1979 and 1981. See
    https://www.nlsinfo.org/content/cohorts/nlsy79/topical-guide/household/age for more details
    """
    def _construct_birth_info(agent):
        """ This method constructs the correct birth variable for each respondent.
        """
        # Store the original information for now for debugging and testing purposes.
        for substring in ['YEAR_OF_BIRTH', 'MONTH_OF_BIRTH']:
            for year in [1979, 1981]:
                agent[substring + '_' + str(year)] = agent[substring][:, year].values[0]
            # Start with a clean slate and always prefer the information from 1981
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
    # Breaking the logic of the code a bit, copies of the object are drawn from here.
    df_internal = df.copy(deep=True)

    # Adjust for missing values here, even though this is also done later in the code
    # for all variables.
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
