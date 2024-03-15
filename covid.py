from collections import defaultdict, Counter
import re
import csv

def replace_range_with_average(data): #1
  for row in data:
    if '-' in row['age']: #deal with test cases that have range
      lower, upper = row['age'].split('-')
      lower = int(lower)
      upper = int(upper)
      row['age'] = str(round((lower + upper) / 2))
    else: #deal with test cases that have no range
      row['age'] = row['age']

"""
def replace_range_with_average(range): #1
  if '-' in range: #deal with test cases that have range
    lower, upper = range.split('-')
    lower = int(lower)
    upper = int(upper)
    return str(round((lower + upper) / 2))
  else: #deal with test cases that have no range
    return range
"""
  
"""
def date_format(date):
  return re.sub(r'(\d{2}).(\d{2}).(\d{4})', r'\2.\1.\3', date) #use regular expressions to rewrite the format
"""
def date_format(data): #2
  for row in data:
    #change date format for date columns listed and used regexps
    for column in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']:
      row[column] = re.sub(r'(\d{2}).(\d{2}).(\d{4})', r'\2.\1.\3', str(row[column]))

def missing_coordinates(data): #3
  province_coordinates = defaultdict(list)
  for row in data:
    if row['latitude'] != 'NaN' and row['longitude'] != 'NaN': #get all the latitudes and longitudes
      province_coordinates[row['province']].append((float(row['latitude']), float(row['longitude'])))  
  for row in data:
    if row['latitude'] == 'NaN' or row['longitude'] == 'NaN': #now go through again to fill it in
      province = row['province']
      if province_coordinates[province] is not None:
        #gets the sum of latitude and longitude and puts in inside, rounding to 2. 
        latitude_sum = sum(coordinate[0] for coordinate in province_coordinates[province])
        longitude_sum = sum(coordinate[1] for coordinate in province_coordinates[province])
        row['longitude'] = round(longitude_sum / len(province_coordinates[province]), 2)
        row['latitude'] = round(latitude_sum / len(province_coordinates[province]), 2)
      else:
        row['latitude'] = 'NaN'
        row['longitude'] = 'NaN'
  
def missing_city(data):
  province_cities = defaultdict(list)
  #get all the cities in the province
  for row in data:
    if row['city'] != 'NaN':
      province_cities[row['province']].append(row['city'])

  for row in data:
    if row['city'] == 'NaN':
      province = row['province']
      if province_cities[province]:
          #in each province, ccouting the city that ioccurs most
          counting_city = Counter(province_cities[province])
          #[0][0] ensures the city appears first in alphabetical order
          most_common_city = counting_city.most_common(1)[0][0]
          row['city'] = most_common_city

def missing_symptoms(data):
    province_symptoms = defaultdict(list)
    for row in data:
        if row['symptoms'] != 'NaN':
            symptoms = re.split('; *|;', row['symptoms']) # Split symptoms string by '; ' or ';'
            # Filter out values with special processing
            symptoms = [symptom.strip() for symptom in symptoms if not re.match(r'^\w+ \d+(\.\d+)? ?°?$|^\w+ \(\d+-\d+ ?°?\)$', symptom)]
            province_symptoms[row['province']].extend(symptoms)

    for row in data:
        if row['symptoms'] == 'NaN':
            province = row['province']
            if province_symptoms[province]:
                counting_symptom = Counter(province_symptoms[province])
                most_common_symptom = counting_symptom.most_common(1)[0][0]
                row['symptoms'] = most_common_symptom

with open("covidTrain.csv", 'r', newline = '') as csvfile:
  reader = csv.DictReader(csvfile)
  data = list(reader)

"""
for row in data: #write the output 
  row['age'] = replace_range_with_average(row['age'])
"""
"""
for row in data:
  for column in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']:
    row[column] = date_format(row[column])
"""

#run all the fuctions
replace_range_with_average(data)
date_format(data)
missing_coordinates(data)
missing_city(data)
missing_symptoms(data)

#gets the fieldnames
with open('covidResult.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys()) 
    writer.writeheader() #reader filed with field names
    writer.writerows(data)