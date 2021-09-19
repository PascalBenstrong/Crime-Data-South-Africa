'''
author: Pascal
'''
import pandas as pd
from pandas import DataFrame

def get_data() -> DataFrame:
  # this is just to tell pandas that columns starting from 2005-2006 ... 2015-2016 have int values
  dtype_dict = {f'{x}-{x+1}':int for x in range(2005,2016)} 
  # read the csv as a DataFrame, with our column datatypes
  return pd.read_csv("SouthAfricaCrimeStats_v2.csv", dtype=dtype_dict, quotechar="'") 

def get_unique_values_for_column(column: str, data: DataFrame):
  '''
  Takes in:
    column: str
    data: DataFrame

  returns np.Array of unique values for column
  '''
  data = data[column].unique()
  data.sort()
  return data

def filter_by_column(column: str, value: str, data: DataFrame):
  '''
  Takes in:
      column: string
      value: string
      data: DataFrame

  returns DataFrame of the data filtered using the specified column and value.
  '''
  # here is our filter definition, we are precisely doing a case-insensitive filter on string
  filter_def = data[column].str.lower() == value.lower()
  # apply the filter_def 
  return data.loc[filter_def]

def get_available_stations_for_province(province: str, data: DataFrame):
  '''
  Takes in:
    province: str
    data: DataFrame

  returns unique stations for province
  '''
  data = filter_by_column("Province", province, data)
  return data["Station"].unique()

def get_beginning_periods(data: DataFrame):
  return [x.split("-")[0] for x in data.columns][3:]

def get_ending_periods(data: DataFrame):
  return [x.split("-")[-1] for x in data.columns][3:]

def get_data_for_period_and_province(period: str, province: str, data: DataFrame):
  '''
  Takes in:
      period: string
      province: string
      data: DataFrame

  returns DataFrame of the data for the specified period and province
  '''

  # get the starting column for the period
  # we create an array with the beginning values of the period
  # eg. ['2005-2006','2006-2007', ...] would produce ['2005', '2006', ...]
  # we then split the provided period and select the begging on the period and find its column
  # in our data
  column_start = 3 + get_beginning_periods(data).index(period.split("-")[0].strip())
  
  # here we doing a similar thing to column_start
  # except that we are selecting the ending of periods
  # we add one because the end value is exclusive in iloc
  column_end = 3 + get_ending_periods(data).index(period.split("-")[-1].strip())+1

  # we want to filter in the province column
  data = filter_by_column("Province", province, data)
  # select the data in the period column
  data = data.iloc[: ,column_start:column_end]

  return data

def get_data_for_station(station: str, data: DataFrame):
  '''
  Takes in:
      station: string
      data: DataFrame

  returns DataFrame of the data for the specified station
  '''

  # starting column for our number data
  column_start = 3
  # ending column
  column_end = data.shape[1]
  # we want to filter in the station column
  data = filter_by_column("Station", station, data)
  # select the data columns from column_start
  # to last column, there is an assumption here that all the remaining
  # columns are numbers
  data = data.iloc[:, column_start: column_end]

  return data

def get_data_for_truck_hijacking(data: DataFrame):
  # filter by category
  data = filter_by_column("Category","truck hijacking",data)
  return data["2010-2011"].sum()

def get_data_for_arson(data:DataFrame):
  # filter by more than one columns
  # first filter by category then province
  data = filter_by_column("Category", "Arson", data)
  filter_def = (data["Station"].str.lower() == "Boitekong".lower()) | (data["Province"].str.lower() == "Ngodwana".lower())
  data = data.loc[filter_def]["2009-2010"]
  return data.sum()

def get_data_for_crime_with_most_incidents(data: DataFrame):
  # group the data by category
  data = data.groupby("Category")
  # select the category and 2014-2015 columns
  data = data[["Category", "2014-2015"]]
  total_groups = data.sum()
  # select column with maximum value
  category = total_groups["2014-2015"].idxmax()
  # select row with maximum value
  total_max = total_groups.loc[category]

  total = total_max.iloc[0]

  return (category,total)

def get_period_with_lowest_murder_in_kzn(data: DataFrame):
  # filter by station
  data = filter_by_column("Station", "Nongoma", data)
  # filter by murder category
  data = filter_by_column("Category", "Murder", data)
  data = data.sum()
  d = dict(data.iloc[3:])
  k = list(d.keys())
  values = list(d.values())
  mink = min(values)
  index = values.index(mink)
  period = k[index]

  return (period,mink)

def get_station_with_no_attempted_murder(data: DataFrame):

  data = filter_by_column("Province", "North West", data)
  data = filter_by_column("Category", "Attempted murder", data)
  filter_def = data["2008-2009"] == 0
  data = data.loc[filter_def]["Station"]

  return list(data)