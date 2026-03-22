from flask import Blueprint, render_template, request, redirect
import math
from services.medicine_service import search_medicine, search_medicine_by_licence, get_medicine_ingredient, replace_and_symbol, get_medicine_list, get_personal_data, get_known_medicines
main = Blueprint("main", __name__)

@main.route("/")
def homepage():

    # medicine_name_list = get_medicine_list()
    #return render_template("index.html", medicine_name_list = medicine_name_list)
    
    return redirect("/search?search=")

@main.route("/index")
def index(): 

    medicine_name_list = get_medicine_list()
    return render_template("index.html", medicine_name_list = medicine_name_list)

@main.route("/about")
def about():

    return render_template("about.html")

@main.route("/search")
def search():
    medicine_name_list = get_medicine_list()
 
    medicine_to_search = request.args.get("search")
    current_page = request.args.get("page")
    if current_page == None or not current_page.isnumeric:
        current_page = 1
    current_page = int(current_page)

    medicine_results = search_medicine(medicine_to_search)
    no_result = len(medicine_results)
    no_pages = math.ceil(no_result / 20)
    if no_pages < 1:
        no_pages = 1

    medicine_to_display = medicine_results[(20 * (current_page - 1)) : (20 * current_page)]



    return render_template("search.html", medicine_to_search = medicine_to_search, no_pages = no_pages, medicine_to_display = medicine_to_display, current_page = current_page, medicine_results = medicine_results, medicine_name_list = medicine_name_list)

@main.route("/medicine/<licence_no>")
def medicine_by_license(licence_no):

    licence_no = licence_no
    medicine_info = search_medicine_by_licence(licence_no)
    
    try:
        personal_info = get_personal_data(licence_no)
    except KeyError:
        personal_info = None


    if medicine_info == None:
        return render_template("error.html")
    
    for_info_strength = replace_and_symbol(medicine_info["strength"])
    
    medicine_ingredient = medicine_info["active_ingredients"]
    medicine_ingredients = get_medicine_ingredient(medicine_ingredient)
    number_repititions = len(medicine_ingredients)


    return render_template("medicine_info.html", medicine_info = medicine_info, medicine_ingredients = medicine_ingredients, for_info_strength = for_info_strength, number_repititions = number_repititions, personal_info = personal_info)


@main.route("/medicine")
def medicine():
    known_medicine = get_known_medicines()

    current_page = request.args.get("page")
    if current_page == None or not current_page.isnumeric:
        current_page = 1
    current_page = int(current_page)

    no_result = len(known_medicine)
    no_pages = math.ceil(no_result / 20)
    if no_pages < 1:
        no_pages = 1

    known_medicine_to_display = known_medicine[(20 * (current_page - 1)) : (20 * current_page)]


    return render_template("medicine.html", known_medicine_to_display = known_medicine_to_display, current_page = current_page, no_pages = no_pages)

@main.route("/instruction")
def instruction():

    return render_template("instruction.html")