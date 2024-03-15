import csv
from collections import defaultdict

#Problem 1.1
def percentage_fire_above_level(fileName):
    total_fire_Count = 0  #take total amount of pokemon
    fire_Count = 0 #total amount of fire pokemon with level 40
    with open(fileName, 'r') as file:
        reader = csv.DictReader(file) #turns the rows into key and the values the rest of the columns
        for row in reader:
            if row['type'] == 'fire':
                total_fire_Count += 1
                if float(row['level']) >= 40:
                    fire_Count += 1
    percentage = (fire_Count / total_fire_Count) * 100 #gain the percentage
    rounded_percentage = round(percentage)
    with open('pokemon1.txt', 'w') as file_output:
        file_output.write(f"Percentage of fire type Pokemons at or above level 40 = {rounded_percentage}") #final output for the first function

#Problem 1.2 and 1.3
def fill_missing_values(fileName):

    #Problem 1.2
    weakness_type_count = defaultdict(lambda: defaultdict(int))
    with open(fileName, 'r') as file:
        reader = csv.DictReader(file) #creates a Dict Reader named reader. It reads each row of the CSV file as a dictionary where the keys are the column headers
        next(reader) #skips the first row as it assumes the csv file contains a header row
        for row in reader:
            if row['type'] != 'NaN': #checks whether the 'type' column of current row is not 'NaN'
                weakness_type_count[row['weakness']][row['type']] += 1 #incremets the count off 'weakness' and 'type'
    dict(weakness_type_count)
    most_common_type = {}
    for weakness, type_counts in weakness_type_count.items():
        print("Weakness", weakness)
        print("Typecount", type_counts)
        # Sort the type counts by count in descending order
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        # Get the most common type (first item in the sorted list)
        #print(sorted_types[0][0])
        most_common_type[weakness] = sorted_types[0][0]

    #Problem 1.3
    total_attack_above_40 = 0
    total_defense_above_40 = 0
    total_hp_above_40 = 0
    count_attack_above_40 = 0
    count_defense_above_40 = 0
    count_hp_above_40 = 0
    total_attack_below_40 = 0
    total_defense_below_40 = 0
    total_hp_below_40 = 0
    count_attack_below_40 = 0
    count_defense_below_40 = 0
    count_hp_below_40 = 0

    with open(fileName, 'r') as file:
        reader = csv.DictReader(file)
        #calculating all the averages
        for row in reader:
            if row['atk'] == 'NaN' or row['def'] == 'NaN' or row['hp'] == 'NaN':
                continue

            attack = float(row['atk'])
            defense = float(row['def'])
            hp = float(row['hp'])
            level = float(row['level'])

            if level > 40:
                total_attack_above_40 += attack
                total_defense_above_40 += defense
                total_hp_above_40 += hp
                count_attack_above_40 += 1
                count_attack_above_40 += 1
                count_hp_above_40 += 1
            else:
                total_attack_below_40 += attack
                total_defense_below_40 += defense
                total_hp_below_40 += hp
                count_attack_below_40 += 1
                count_defense_below_40 += 1
                count_hp_below_40 += 1

        
        #make sure to check to make sure no division by 0 errors
        average_attack_above_40 = total_attack_above_40 / count_attack_above_40 if  count_attack_above_40 != 0 else 0
        average_defense_above_40 = total_defense_above_40 / count_attack_above_40 if count_defense_above_40 != 0 else 0
        average_hp_above_40 = total_hp_above_40 / count_hp_above_40 if count_hp_below_40 != 0 else 0
        average_attack_below_40 = total_attack_below_40 / count_attack_below_40 if count_attack_below_40 != 0 else 0
        average_defense_below_40 = total_defense_below_40 / count_defense_below_40 if count_defense_below_40 != 0 else 0
        average_hp_below_40 = total_hp_below_40 / count_hp_below_40 if count_hp_below_40 != 0 else 0

        with open(fileName, 'r') as file:
            reader = csv.DictReader(file)
            next(reader)
            data = list(reader)

            for row in data:
                if row['type'] == 'NaN' and row['weakness'] in most_common_type:
                    row['type'] = most_common_type[row['weakness']]

                if row['atk'] == 'NaN' or row['def'] == 'NaN' or row['hp'] == 'NaN':
                    level = float(row['level'])
                    if level > 40:
                        if row['atk'] == 'NaN':
                            row['atk'] = round(average_attack_above_40, 1)
                        if row['def'] == 'NaN':
                            row['def'] = round(average_defense_above_40, 1)
                        if row['hp'] == 'NaN':
                            row['hp'] = round(average_hp_above_40, 1)
                    else:
                        if row['atk'] == 'NaN':
                            row['atk'] = round(average_attack_below_40, 1)
                        if row['def'] == 'NaN':
                            row['def'] = round(average_defense_below_40, 1)
                        if row['hp'] == 'NaN':
                            row['hp'] = round(average_hp_below_40, 1)
        
        with open('pokemonResult.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def pokemon_type_personality_mapping(fileName):
    #Problem 1.4
    types_personality_mapping = defaultdict(list)

    with open(fileName, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            types_personality_mapping[row['type']].append(row['personality']) #creates a dictionary where key is type and the values will be personality

    with open('pokemon4.txt', 'w') as output:
        output.write("Pokemon type to personality mapping:\n\n") #writing the output to the file
        for key in types_personality_mapping:
            values = ', '.join(types_personality_mapping[key])
            output.write(f"\t{key}: {values}\n")
            
def average_hp_for_stage_3(fileName):
    count = 0
    total_hp = 0

    with open(fileName, 'r') as file:
        reader = csv.DictReader(file) 
        for row in reader:
            if float(row['stage']) == 3.0: #checks to see if the pokemon is at stage 3.0
                total_hp += float(row['hp'])
                count += 1
    average = round(total_hp/count) if count != 0 else 0 #calculates the average but checks for test case in case the count is 0
    with open("pokemon5.txt", 'w') as output:
        output.write(f"Average hit point for Pokemons of stage 3.0 = {average}") #return the output
    
  

percentage_fire_above_level('pokemonTrain.csv')
fill_missing_values('PokemonTrain.csv')
pokemon_type_personality_mapping('pokemonResult.csv')
average_hp_for_stage_3("pokemonResult.csv")

