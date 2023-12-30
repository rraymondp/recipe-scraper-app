import requests
import extruct
from bs4 import BeautifulSoup
import isodate

def scrape(url):
    #added user-agent to combat 403 error
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    result = requests.get(url, headers=headers)
    print(result)

    return result

def parse(html_page):
    soup = str(BeautifulSoup(html_page.text, "html.parser"))

    data = extruct.extract(soup, syntaxes=["json-ld"], uniform=True) #extracts the json-ld data from the entire html document

    json_data_list = data.get("json-ld")                             #retrive the embedded json-ld from the html document which is in the form of a list of dictionaries [{'@context' : 'https://schema.org', '@graph' : ...}]

    json_data_dic = {}                                               #Converting the list of dictionaries into just a singular dictionary
    for item in json_data_list:
        json_data_dic.update(item)

    return json_data_dic
    
def get_recipe_data(json_ld):
    #check if json-ld has a graph object or not --> '@graph'
    if len(json_ld) <= 2:
        for i in range(len(json_ld["@graph"])):                 #Iterating through the '@graph' key to find the value that contains the recipe data
            if (json_ld["@graph"][i]["@type"] == "Recipe"):
                recipe_data = json_ld["@graph"][i]
    else:
        recipe_data = json_ld

    return recipe_data

def get_schema(json_dic):
    schema = json_dic["@context"]

    return schema

def get_name(results):
    name = results["name"]

    return name

def get_ingredients(results):
    ingredients = results["recipeIngredient"]

    return ingredients

def get_instructions(results):
    instructions = []
    for instruction in results["recipeInstructions"]:
        instructions.append(instruction["text"].replace("&nbsp;", ""))         #appends each of the instructions found in the json data into the instructions list as well as remove all instances of non-breaking spaces "ndsp;"

    return instructions

def get_prep_time(results):
    ptime = get_minutes(results["prepTime"])
    return ptime

def get_cook_time(results):
    ctime = get_minutes(results["cookTime"])
    return ctime

def get_total_time(results):
    total_time = get_minutes(results["totalTime"])
    return total_time

def get_minutes(time):
    mins = isodate.parse_duration(time).seconds // 60
    return mins
    
def output(food_name, schema, prep_time, cook_time, total_time, ingredients, instructions):
    print('\n')
    print("The Name of the Recipe is:")
    print("--------------------------")
    print(food_name)
    print('\n')

    print("The schema of the recipe website is:")
    print("------------------------------------")
    print(schema)
    print('\n')

    print("The prep time for the recipe website is:")
    print("------------------------------------")
    print(str(prep_time) + " mins")
    print('\n')

    print("The cook time for the recipe website is:")
    print("------------------------------------")
    print(str(cook_time) + " mins")
    print('\n')

    print("The total time for the recipe website is:")
    print("------------------------------------")
    print(str(total_time) + " mins")
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


def main():
    url = ""
    html = scrape(url)
    json_data = parse(html)
    recipe_data = get_recipe_data(json_data)

    name = get_name(recipe_data)
    schema = get_schema(json_data)
    prep_time = get_prep_time(recipe_data)
    cook_time = get_cook_time(recipe_data)
    total_time = get_total_time(recipe_data)
    ingredients = get_ingredients(recipe_data)
    instrcutions = get_instructions(recipe_data)

    output(name, schema, prep_time, cook_time, total_time, ingredients, instrcutions)







