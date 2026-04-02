from flask import Flask, url_for, render_template, request, redirect, session
from flask_session import Session
import math
from services.sessions_service import get_passid_hash, login_required, retrieve_created, create_personal_data, delete_entry
from services.medicine_service import first_letter_capital, search_medicine, search_medicine_by_licence, get_medicine_ingredient, replace_and_symbol, get_medicine_list, get_personal_data, get_known_medicines, get_ingredientlicence_by_name, get_similar_medicines, get_known_licences, get_product_name

app = Flask(__name__)
# app.register_blueprint(main)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def homepage():

    # medicine_name_list = get_medicine_list()
    #return render_template("index.html", medicine_name_list = medicine_name_list)
    
    return redirect("/search?search=")

@app.route("/index")
def index(): 

    medicine_name_list = get_medicine_list()
    return render_template("index.html", medicine_name_list = medicine_name_list)

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/search")
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

# @app.route("/symptoms")
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

@app.route("/medicine/<licence_no>")
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


@app.route("/medicine")
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

@app.route("/instruction")
def instruction():

    return render_template("instruction.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        entered_user = request.form.get("username")
        entered_password = request.form.get("password").encode("utf-8")

        if not entered_user or not entered_password:
            return render_template("login.html", error = "Incorrect username or password")

        user_id = get_passid_hash(entered_user, entered_password)

        if user_id == []:
            return render_template("login.html", error = "Incorrect username or password")

        session["user_id"] = user_id

        return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/dashboard")
@login_required
def dashboard():

    known = get_known_medicines()
    past_entries = retrieve_created()

    if len(known) == len(past_entries):

        current_page = request.args.get("page")
        if current_page == None or not current_page.isnumeric:
            current_page = 1
        current_page = int(current_page)

        no_result = len(past_entries)
        no_pages = math.ceil(no_result / 20)
        if no_pages < 1:
            no_pages = 1

        entries_to_display = past_entries[(20 * (current_page - 1)) : (20 * current_page)]

        return render_template("dashboard.html", past_entries = past_entries, current_page = current_page, no_pages = no_pages, entries_to_display = entries_to_display)

    else:
        return redirect("/medicine")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "GET":
        known_medicines = get_known_licences() 
        medicine_name_list = get_medicine_list()

        target_name = request.args.get("product_name")
        if not target_name:
            return render_template("create.html", medicine_name_list = medicine_name_list)
        
        target_name = target_name.upper()
        dbdata = get_ingredientlicence_by_name(target_name)
        
        target_licence = dbdata["licence_no"]
        if target_licence in known_medicines:
            message = "Listing for this Medicines has already been created."
            return render_template("error.html", error = message)

        active_ingredients = dbdata["active_ingredients"]

        similar_medicines = get_similar_medicines(active_ingredients, target_licence)  #list of lic and name with same ingredients
        
        #ensure no repeated medicatinos
        length = len(similar_medicines)
        count = 0
        while count < length:
            if similar_medicines[count]["licence_no"] in known_medicines:
                similar_medicines.pop(count)
                length -= 1
            
            count += 1



        return render_template("create.html", medicine_name_list = medicine_name_list, target_name = target_name, target_licence = target_licence, similar_medicines = similar_medicines )

    if request.method == "POST":

        target_licences = request.form.get("multiple-licence-no").split(", ")
        dosage = request.form.get("dosage")
        interval = request.form.get("interval")
        times = request.form.get("times-per-day")
        max = request.form.get("max-dosage")
        drug_int = request.form.get("drug-interaction")
        side_effects = request.form.get("side-effects")
        contraindication = request.form.get("contraindications")


        # with open("Medicine Data/test.txt", 'w') as f:

        #     f.write(str(target_licences))
        #     f.write(dosage + "\n")
        #     f.write(interval + "\n")
        #     f.write(times + "\n")
        #     f.write(max + "\n")
        #     f.write(drug_int + "\n")
        #     f.write(side_effects + "\n")
        #     f.write(contraindication + "\n")

        # return redirect("/")


        user_id = int(session.get("user_id"))
        to_create = []
        to_add = {
                "licence_no": "",
                "product_name": "",
                "dosage": dosage,
                "times_per_day": times,
                "hourly_interval": interval,
                "max_dosage_per_day": max,
                "side_effects": side_effects,
                "drug_interaction": drug_int,
                "contraindication": contraindication,
                "created_by": user_id,
        }
        
        for licences in target_licences:
            name = get_product_name(licences)
            name = first_letter_capital(name)
            copy_add = to_add.copy()
            copy_add["licence_no"] = licences
            copy_add["product_name"] = name
            to_create.append(copy_add)

        result = create_personal_data(to_create)

        # try:
        #     with open("Medicine Data/test.txt", 'a') as f:
        #         f.write(result)
        # except:
        #     pass

        if result:
            return redirect(url_for("dashboard"))
        else:
            return render_template("error.html", error = result)

        
        

@app.route("/delete")
@login_required
def delete():

    to_delete = request.args.get("num")

    delete_entry(to_delete)

    return redirect('/dashboard')
