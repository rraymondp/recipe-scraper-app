from flask import Blueprint, render_template, request
import scraper

#Contains all of the routes 

views = Blueprint(__name__, "views")

@views.route("/")
@views.route("/index")
def home():
    return render_template("index.html")   #go to the index html page if the url prefix starts with / or /index


@views.route("/recipe")                    #if the url prefix starts with /recipe
def get_recipe_data():                     #retrieve the recipes data from the url
    url = request.args.get('url')          #gets the url from the html page
    html = scraper.scrape(url)
    json_data = scraper.parse(html)
    recipe_data = scraper.get_recipe_data(json_data)

    name = scraper.get_name(recipe_data)
    schema = scraper.get_schema(json_data)
    prep_time = scraper.get_prep_time(recipe_data)
    cook_time = scraper.get_cook_time(recipe_data)
    total_time = scraper.get_total_time(recipe_data)
    ingredients = scraper.get_ingredients(recipe_data)
    instructions = scraper.get_instructions(recipe_data)

    return render_template(                #goes to the recipe html page and replaces the template variables {{ }} with the values that were gathered here
        "recipe.html",
        name = name,
        schema = schema,
        prep_time = prep_time,
        cook_time = cook_time,
        total_time = total_time,
        ingredients = ingredients,
        instructions = instructions
        )
    