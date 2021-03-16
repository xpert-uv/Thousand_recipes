
import pdb
from flask import jsonify
import requests
from keys import s_api

BASE_API = "https://api.spoonacular.com"


##################### Function for Food Recipes ###################################
def Search_recipe(recipename):
    """ This function will make request to api about lists of recipes based on keyword like: pasta, chicken, cake etc
     and returns the filtered data in json format. """

    response = requests.get(
        f'{BASE_API}/recipes/search?query={recipename}&apiKey={s_api}')
    json_response = response.json()
    if response.status_code != 200:
        return json_response
    else:
        result_list = []
        # for image url
        imageurl = json_response['baseUri']

        for r in json_response['results']:
            response = {'id': r['id'],
                        'title': r['title'],
                        'total_time': r['readyInMinutes'],
                        'image': imageurl + r['image']}
            result_list.append(response)

        final_response = {"result": result_list}
        return final_response


def Recipe_details(recipe_id):
    """ This function will make request to API about the recpie details base on id and returns the filtered data in json format"""

    response = requests.get(
        f'{BASE_API}/recipes/{recipe_id}/information?apiKey={s_api}')
    json_response = response.json()

    # API request to get Ingredients-by-id
    response_ing = requests.get(
        f'{BASE_API}/recipes/{recipe_id}/ingredientWidget.json?apiKey={s_api}')
    json_response_ing = response_ing.json()

    if response.status_code != 200:
        return json_response
    elif response_ing.status_code != 200:
        return json_response_ing
    else:
        # striping individual data of ingredients
        ingredietns_list = []
        ingredients_name = [x['name']
                            for x in json_response_ing['ingredients']]
        ingredients_amount = [x['amount']
                              for x in json_response_ing['ingredients']]
        ingredients_value = [x['us']['value'] for x in ingredients_amount]
        ingredietns_unit = [x['us']['unit'] for x in ingredients_amount]

        # zipping name, value, unit data to form a sentence and creating list of ingredietns

        for name, value, unit in zip(ingredients_name, ingredients_value, ingredietns_unit):
            ingredietns_list.append(f'{name} {value} {unit}')

        final_response = {'id': json_response['id'],
                          'title': json_response['title'],
                          'ingredients': ingredietns_list,
                          'total_time': json_response['readyInMinutes'],
                          'image': json_response['image'],
                          'description': json_response['summary'],
                          'instructions': json_response['instructions']}

        return final_response


############################# Functions for Wine and Wine paring #########################

def Search_wine(wine_name):
    """ This function will request the API about the Wine based on wine name/type  and returns the filtred data in json format.
        -Default numbers of wine searched return is 20.


    """
    response = requests.get(
        f'{BASE_API}/food/wine/recommendation?wine={wine_name}&number=20&apiKey={s_api}')
    json_response = response.json()
    if response.status_code != 200:
        return json_response
    else:
        wine_list = []
        for wines in json_response['recommendedWines']:
            wine = {'id': wines['id'],
                    'title': wines['title'],
                    'description': wines['description'],
                    'price': wines['price'],
                    'image': wines['imageUrl']
                    }
            wine_list.append(wine)

        final_response = {"wines": wine_list}
        return final_response


def Wine_paring_for_meal(food):
    """ This function will make a request to API and pair wine for select meal/food and
    returns data into jason format. """

    response = requests.get(
        f'{BASE_API}/food/wine/pairing?food={food}&apiKey={s_api}')
    json_response = response.json()
    if response.status_code != 200:
        return json_response
    else:

        wine_list = []
        for wines in json_response['productMatches']:

            wine = {'title': wines['title'],
                    'description': wines['description'],
                    'price': wines['price'],
                    'image': wines['imageUrl']
                    }
            wine_list.append(wine)

        final_response = {'wines': json_response['pairedWines'],
                          'description': json_response['pairingText'],
                          'wine': wine_list}

        return final_response


def Dish_paring_for_wine(wine):
    """ This function will make a request to API and pair dish for selected wine and returns data into jason format"""

    response = requests.get(
        f'{BASE_API}/food/wine/dishes?wine={wine}&apiKey={s_api}')
    json_response = response.json()
    if response.status_code != 200:
        return json_response
    else:
        final_response = {'paring': json_response['pairings']}

        return final_response
