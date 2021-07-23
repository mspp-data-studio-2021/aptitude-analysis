# %%
"""This module creates a class object for the data."""

# %%
import pandas as pd
import numpy as np

from setup_dct import get_mappings
from setup_dct import cleaning_highest_grade_attended
from setup_dct import aggregate_highest_degree_received

from setup_additional_vars import standarize_employer_information
from setup_additional_vars import aggregate_birth_information
from setup_additional_vars import calculate_afqt_scores
from setup_additional_vars import create_is_interviewed

# %%
# This list contains all variables that are processed for the panel, checked via testing.
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
TIME_VARYING += ['MONTH_OF_BIRTH', 'YEAR_OF_BIRTH', 'SURVEY_YEAR', 'REASON_NONINTERVIEW']
TIME_VARYING += ['HIGHEST_GRADE_COMPLETED', 'HIGHEST_GRADE_ATTENDED']
TIME_VARYING += ['HIGHEST_DEGREE_RECEIVED_1', 'HIGHEST_DEGREE_RECEIVED_2']
TIME_VARYING += ['CPSOCC70', 'INCOME_WAGES_SALARY', 'AMT_WORK_LMT', 'TYPE_WORK_LMT']
TIME_VARYING += ['POVSTATUS', 'HEALTH_INS', 'MAR_STATUS', 'REGION']

for start in ['EMP_HOURS_WK_', 'EMP_STATUS_WK_']:
    for week in ['1', '7', '13', '14', '20', '26', '40', '46', '52']:
        TIME_VARYING += [start + week]

for start in ['WAGE_HOURLY_JOB_', 'CPS_JOB_INDICATOR_JOB_', 'OCCALL70_JOB_']:
    for job in ['1', '2', '3', '4', '5']:
        TIME_VARYING += [start + job]

# %%
# These variables are created during processing and are part of a separate list, as they're
# not available when the data is transformed from wide to long format.
DERIVED_VARS = []
DERIVED_VARS += ['AFQT_RAW', 'IS_INTERVIEWED', 'HIGHEST_DEGREE_RECEIVED']

for start in ['OCCALL70_MOD_JOB_']:
    for job in ['1', '2', '3', '4', '5']:
        DERIVED_VARS += [start + job]

# %%
class SourceCls(object):
    """ This class contains all methods that prepare the source dataset for further uses.
    """
    def __init__(self):

        # Class attributes
        self.survey_years = None
        self.source_wide = None
        self.source_long = None
        self.dct = None

    def read_source(self, num_agents=None):
        """ Read the original file from the NLSY INVESTIGATOR.
        """
        # Read from original data from CSV file
        self.source_wide = pd.read_csv(r'C:/Users/bec10/OneDrive/Desktop/files/repos/aptitude-analysis/data/all-variables.csv', nrows=num_agents)

        # Process variable dictionary
        survey_years, dct = get_mappings()

        # Attach results as class attributes
        self.survey_years = survey_years
        self.dct = dct

    def add_basic_variables(self):
        """ Add some basic variables that are constructed from the original information.
        """
        # Distribute class attributes
        source_long = self.source_long

        # Process birth information
        source_long = aggregate_birth_information(source_long)

        # Compute the AFQT score 
        source_long = calculate_afqt_scores(source_long)

        # There are no missing values for these variables, so integer type can be enforced.
        for varname in ['MONTH_OF_BIRTH', 'YEAR_OF_BIRTH']:
            source_long[varname] = source_long[varname].astype('int64')

        source_long = aggregate_highest_degree_received(source_long)
        source_long = cleaning_highest_grade_attended(source_long)
        source_long = standarize_employer_information(source_long)
        source_long = create_is_interviewed(source_long)

        self.source_long = source_long

    def transform_wide_to_panel(self):
        """ Transform from wide to long format.
        """
        # Distribute class attributes
        survey_years = self.survey_years
        source_wide = self.source_wide
        dct = self.dct

        # Change from the original wide format to a typical panel structure
        self.source_long = wide_to_long(source_wide, survey_years, dct)
        self._set_missing_values()

    def _set_missing_values(self):
        """ This method ensures a uniform treatment of missing values.
        """
        # Distribute class attributes
        source_long = self.source_long

        # In the original dataset missing values are indicated by negative values
        for varname in TIME_VARYING + TIME_CONSTANT:
            cond = source_long[varname] < 0
            if np.sum(cond) > 0:
                source_long.loc[cond, varname] = np.nan

    def testing(self):
        """ This method performs some basic consistency checks for the constructed panel.
        """
        # Distribute class attributes
        source_long = self.source_long

        # There are several variables which can't have a missing value.
        varnames = []
        varnames += ['IDENTIFIER', 'RACE', 'GENDER', 'MONTH_OF_BIRTH', 'YEAR_OF_BIRTH']
        varnames += ['SURVEY_YEAR']
        for varname in varnames:
            np.testing.assert_equal(source_long[varname].notnull().all(), True)
    
        # The same is true for the all EMP_STATUS_ variables. There is one individual
        # whom does in fact have missing values in their employment status; drop them.
        subset = source_long.drop(9269, level='Identifier')
        np.testing.assert_equal(subset.filter(regex='EMP_STATUS_*').notnull().all().all(), True)

        # For all EMP_HOURS_ variables, non-missing values need to be positive
        assert source_long.filter(regex='EMP_HOURS_*').apply(lambda column: (column[column.notnull()] >= 0).all()).all()
    
        # There are several variables which are not supposed to vary over time.
        varnames = []
        varnames += ['IDENTIFIER', 'RACE', 'GENDER', 'MONTH_OF_BIRTH', 'YEAR_OF_BIRTH', 'AFQT_1']
        varnames += ['AFQT_RAW', 'ASVAB_ALTERED_TESTING', 'SAMPLE_ID']
        for varname in varnames:
            np.testing.assert_equal((source_long[varname].notnull().groupby(
                level='Identifier').std() == 0).all(), True)

        # Racial distribution is given on the NLSY website.
        values = source_long['RACE'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([7510, 3174, 2002], values)
    
        # Gender distribution is given on the NLSY website.
        values = source_long['GENDER'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([6403, 6283], values)

        # Sample ID distribution is given on the NLSY website.
        values = source_long['SAMPLE_ID'].loc[:, 1979].value_counts().values
        np.testing.assert_almost_equal([2279, 2236, 1105, 1067, 901, 751, 742, 729, 609, 405,
                                        346, 342, 226, 218, 203, 198, 162, 89, 53, 25], values)

        # A bit is known about the AFQT_1 variable from the codebook.
        stat = source_long['AFQT_1'].groupby(level='Identifier').first().isnull().sum()
        np.testing.assert_equal(stat, 808)
        stat = (source_long['AFQT_1'].min(), source_long['AFQT_1'].max())
        np.testing.assert_equal(stat, (1, 99))
        stat = source_long['AFQT_1'].mean()
        np.testing.assert_equal(stat, 40.906044788684966)

        # ASVAB_ALTERED_TESTING
        values = source_long.groupby(level='Identifier').first()['ASVAB_ALTERED_TESTING'].value_counts().values
        np.testing.assert_equal([11625, 127, 85, 41, 36], values)

        # The variable CPSOCC70 is used to impute OCCALL70_MOD_JOB_1 in 1979 and 1993.
        for year in [1979, 1993]:
            cond = source_long['CPSOCC70'][:, year].equals(source_long['OCCALL70_MOD_JOB_1'][:, year])
            np.testing.assert_equal(cond, True)

        ''' Check the distribution of selected variables at random.
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

        # Confirm all included variables are mentioned at the beginning of the module.
        varnames = TIME_CONSTANT + TIME_VARYING + DERIVED_VARS
        np.testing.assert_equal(set(source_long.columns.values), set(varnames))

    def store(self, fname):
        """ Store the dataset for further processing.
        """
        # Distribute class attributes
        source_long = self.source_long

        # Write out persistent storage
        source_long.to_pickle(fname)

    def load(self, fname):
        """ Store the dataset for further processing.
        """
        # Distribute class attributes
        self.source_long = pd.read_pickle(fname)
        print(type(fname))
        


# %%
def wide_to_long(source_wide, additional_level, dct):
    """ Set up an empty dataframe in the wide-to-long format with the right index structure. This
    maintains the mapping between the index in the datafrmae in the NLSY respondent ID.
    """
    caseid = [x + 1 for x in source_wide.index]
    multi_index = pd.MultiIndex.from_product([caseid, additional_level], names=['Identifier', 'Survey Year'])
    pd_long = pd.DataFrame(index=multi_index)

    # It's useful to have a column that corresponds to each of the two indices.
    pd_long['IDENTIFIER'] = pd_long.index.get_level_values('Identifier')
    pd_long['SURVEY_YEAR'] = pd_long.index.get_level_values('Survey Year')

    for long_name in dct.keys():
        # Initialize the column with missing values.
        pd_long[long_name] = np.nan
        for year in additional_level:
            # For variables not be defined for each year, missing values remain.
            if year not in dct[long_name].keys():
                continue
            # Assign the variable name to the corresponding year.
            pd_long.loc[(slice(None), year), long_name] = source_wide[dct[long_name][year]].values

    # Some variables do not have any missing values, so integer type can be imposed.
    for varname in ['IDENTIFIER', 'SURVEY_YEAR', 'RACE', 'GENDER']:
        pd_long[varname] = pd_long[varname].astype('int64')

    return pd_long

# %%
def cpsocc_counts(year, source_long):
    """ This function returns counts for each of the bins of the variable CPSOCC70.
    """
    bins = []
    bins += [(1, 195), (201, 245), (260, 285), (301, 395), (401, 575), (580, 590)]
    bins += [(601, 715), (740, 785), (801, 802), (821, 824), (901, 965), (980, 984)]

    counts = _get_counts_year(source_long['CPSOCC70'], bins, year)

    return counts

# %%
def occall_counts(year, num, source_long):
    """ This function returns counts for each of the bins of the variable OCCALL70_.
    """
    bins = []
    bins += [(1, 195), (201, 245), (260, 285), (301, 395), (401, 575), (580, 590), (601, 715)]
    bins += [(740, 785), (801, 802), (821, 824), (901, 965), (980, 984)]

    counts = _get_counts_year(source_long['OCCALL70_JOB_' + str(num)], bins, year)

    return counts

# %%
def wage_hourly_counts(year, num, source_long):
    """ This function returns counts for each of the bins of the variable.
    """
    bins = []
    bins += [(0, 1), (1, 99), (100, 199), (200, 299), (300, 399), (400, 499), (500, 599)]
    bins += [(600, 699), (700, 799), (800, 899), (900, 999), (1000, np.inf)]

    counts = _get_counts_year(source_long['WAGE_HOURLY_JOB_' + str(num)], bins, year)

    return counts

# %%
def emp_hours_counts(year, week, source_long):
    """ This function returns counts for each of the bins of the variable EMP_HOURS.
    """
    bins = []
    bins += [(0, 0), (1, 9), (10, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69)]
    bins += [(70, 79), (80, 89), (90, 99), (100, np.inf)]

    label = 'EMP_HOURS_WK_' + str(week)
    counts = _get_counts_year(source_long[label], bins, year)
    counts += [source_long[label].loc[:, year].isnull().sum()]

    return counts

# %%
def emp_status_counts(year, week, source_long):
    """ This function returns counts for each of the bins of the variable EMP_STATUS.
    """
    bins = []
    bins += [(100, np.inf), (0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (7, 7)]

    counts = _get_counts_year(source_long['EMP_STATUS_WK_' + str(week)], bins, year)

    return counts

# %%
def _get_counts_year(series, bins, year):
    """ This function gets the counts within each bin of a particular year.
    """
    counts = []
    for bounds in bins:
        lower, upper = bounds
        counts += [series.loc[:, year].between(lower, upper).sum()]

    return counts


# %%
# Save the object as a pkl file for further analysis
if __name__ == '__main__':

    fname = 'C:/Users/bec10/OneDrive/Desktop/files/repos/aptitude-analysis/data/all-vars.pkl'

    source_obj = SourceCls()

    source_obj.read_source()
    source_obj.transform_wide_to_panel()
    source_obj.add_basic_variables()
    source_obj.store(fname)

    source_obj.load(fname)
    source_obj.testing()


# %%
