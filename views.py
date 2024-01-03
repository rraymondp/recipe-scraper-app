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
    try:
        url = request.args.get('url')          #gets the url from the html page
        html = scraper.scrape(url)
        json_data = scraper.parse(html)
        recipe_data = scraper.get_recipe_data(json_data)
        article_data = scraper.get_article_data(json_data)

        name = scraper.get_name(recipe_data)
        schema = scraper.get_schema(json_data)
        prep_time = scraper.get_prep_time(recipe_data)
        cook_time = scraper.get_cook_time(recipe_data)
        total_time = scraper.get_total_time(recipe_data)
        ingredients = scraper.get_ingredients(recipe_data)
        instructions = scraper.get_instructions(recipe_data)
        thumbnail_url = scraper.get_thumbnail(article_data, recipe_data)
        
        error_statement = ""

        return render_template(                #goes to the recipe html page and replaces the template variables {{ }} with the values that were gathered here
            "recipe.html",
            name = name,
            schema = schema,
            prep_time = prep_time,
            cook_time = cook_time,
            total_time = total_time,
            ingredients = ingredients,
            instructions = instructions,
            thumbnail_url = thumbnail_url,
            url = url,
            )

    except Exception as error:
        if(type(error).__name__ == "MissingSchema" or type(error).__name__ == "SSLError"):
            error_statement = "Please enter a valid url :)"
        elif(type(error).__name__ == "ConnectTimeout"):
            error_statement = "Sorry we could not connect to this website, please try again :D"
        elif(type(error).__name__ == "KeyError"):
             error_statement = "Sorry this website is not supported at this time :("
        return render_template("index.html", error_statement = error_statement)
    