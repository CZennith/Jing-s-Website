from flask import Blueprint, render_template, request, redirect, session
import math
from services.sessions_service import get_passid_hash, login_required
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

# @main.route("/symptoms")
# def symptoms():
#     symptom_name_list = get_symptom_list()
    
#     # when symptom to medicine list come retrieve license nos connected to symptom and list them out 

#     symptom_to_search = request.args.get("symptoms")
#     current_page = request.args.get("page")
#     if current_page == None or not current_page.isnumeric:
#         current_page = 1
#     current_page = int(current_page)

#     medicine_results = search_medicine_by_symptom(symptom_to_search)

#     no_result = len(medicine_results)
#     no_pages = math.ceil(no_result / 20)
#     if no_pages < 1:
#         no_pages = 1

#     medicine_to_display = medicine_results[(20 * (current_page - 1)) : (20 * current_page)]


#     return render_template("symptoms.html", medicine_to_search = medicine_to_search, no_pages = no_pages, medicine_to_display = medicine_to_display, current_page = current_page, medicine_results = medicine_results, medicine_name_list = medicine_name_list)

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


@main.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        entered_user = request.form.get("username")
        entered_password = request.form.get("password").encode("utf-8")

        user_id = get_passid_hash(entered_user, entered_password)

        if user_id == []:
            return render_template("log-in.html", error = "Incorrect username or password")

        session["user_id"] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("log-in.html")


@main.route("/dashboard")
@login_required
def dashboard():

    past_entries = []

    return render_template("dashboard.html", entries = past_entries)

