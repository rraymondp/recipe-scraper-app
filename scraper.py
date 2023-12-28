import requests
import extruct
import pprint
from bs4 import BeautifulSoup

# pp = pprint.PrettyPrinter(indent=2)

#added user-agent to combat 403 error
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = "https://www.allrecipes.com/recipe/19247/soft-oatmeal-cookies/"
result = requests.get(url, headers=headers)

# print(result)

soup = str(BeautifulSoup(result.text, "html.parser"))            #extracts the html data and parses it 

data = extruct.extract(soup, syntaxes=["json-ld"], uniform=True) #extracts the json-ld data from the entire html document

json_data_list = data.get("json-ld")                             #retrive the embedded json-ld from the html document which is in the form of a list of dictionaries [{'@context' : 'https://schema.org', '@graph' : ...}]

json_data_dic = {}                                               #Converting the list of dictionaries into just a singular dictionary
for item in json_data_list:
    json_data_dic.update(item)

#check if json-ld has a graph object or not --> '@graph'
if len(json_data_dic) <= 2:
    for i in range(len(json_data_dic["@graph"])):                 #Iterating through the '@graph' key to find the value that contains the recipe data
        if (json_data_dic["@graph"][i]["@type"] == "Recipe"):
            recipe_data = json_data_dic["@graph"][i]
else:
    recipe_data = json_data_dic


    
# print(len(json_data_dic))
    

food_name = recipe_data["name"]
schema = json_data_dic["@context"]
ingredients = recipe_data["recipeIngredient"]

# print(ingredients)
 
instructions = []

for instruction in recipe_data["recipeInstructions"]:
    instructions.append(instruction["text"])

print('\n')
print("The Name of the Recipe is:")
print("--------------------------")
print(food_name)
print('\n')

print("The schema of the recipe website is:")
print("------------------------------------")
print(schema)
print('\n')

print("The ingredients for the recipe is:")
print("----------------------------------")
for ingredient in ingredients:
    print(ingredient)
print('\n')

print("The instructions for the recipe is:")
print("-----------------------------------")
for i in range(len(instructions)):
    print(str(i + 1) + ") " + instructions[i] + '\n')

# maybe add the prep and cook times for the recipe







