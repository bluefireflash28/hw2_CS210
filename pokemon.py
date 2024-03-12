import csv

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
        file_output.write(f"Percentage of fire type Pokemons at or above level 40 = {rounded_percentage}")


percentage_fire_above_level('pokemonTrain.csv')
