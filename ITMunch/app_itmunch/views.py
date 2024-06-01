import datetime
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
import requests #anaconda prompt -> conda activate [environment] -> conda install requests

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['goal', 'gender', 'birthday', 'height', 'current_weight', 'goal_weight', 'goal_date', 'activity']
        labels = {
            'birthday': 'Birthday (YYYY-MM-DD)',
            'height': 'Height (Centimeters)',
            'current_weight': 'Current weight (Kilograms)',
            'goal_weight': 'Goal weight (Kilograms)',
            'goal_date': 'Goal date (YYYY-MM-DD)',
        }

def index(request):
    """Index view for the application.

    Args:
        request (HttpRequest): The request object used to generate this response.
    
    Returns:
        HttpResponse: The rendered index page with profile and calories context.
    """
    
    if not request.user.is_authenticated: # redirect to login if user is not authenticated
        return redirect('app_itmunch:login')
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user) # get or create a profile for the user
    calories = calculate_calories(profile)
    return render(request, 'app_itmunch/index.html', {'profile': profile, 'calories': calories})

def login_view(request):
    """Login view for the application.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered login page with form context.
        HttpResponseRedirect: Redirects to the index page upon successful login.
    """
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid(): # authenticate the user with cleaned credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('app_itmunch:index')
    else: # empty authentication form to render the HTML page
        form = AuthenticationForm()
    return render(request, 'app_itmunch/login.html', {'form': form})

def register_view(request):
    """Register view for the application.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered registration page with form context.
        HttpResponseRedirect: Redirects to the questions page upon successful registration.
    """
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('app_itmunch:questions')
    else: # empty user creation form to render the HTML page
        form = UserCreationForm()
    return render(request, 'app_itmunch/register.html', {'form': form})

def logout_view(request):
    """Logout view for the application.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponseRedirect: Redirects to the login page after logout.
    """
    
    logout(request)
    return redirect('app_itmunch:login')

def questions_view(request):
    """Questions view for the application.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered questions page with form context.
        HttpResponseRedirect: Redirects to the index page upon successful form submission.
    """
    
    if not request.user.is_authenticated: # redirect to login if user is not authenticated
        return redirect('app_itmunch:login')
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user) # get or create a profile for the user
    if request.method == 'POST': # create a form with POST data and the user's profile instance
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('app_itmunch:index')
    else: # empty profile form to render the HTML page
        form = ProfileForm(instance=profile)
    if created:  # render questions page if the profile was just created
        return render(request, 'app_itmunch/questions.html', {'form': form})
    else:  # render edit profile page if the profile already exists
        return render(request, 'app_itmunch/edit.html', {'form': form})

def calculate_calories(profile):
    """Calculate daily calorie needs based on the profile.

    Args:
        profile (Profile): The user's profile containing weight, height, age, gender, activity level, and goal.

    Returns:
        int: The calculated daily calorie needs.
    """

    weight = float(profile.current_weight)
    height = float(profile.height)
    age = (datetime.date.today() - profile.birthday).days // 365 # calculate age based on today date
    if profile.gender == 'male': # calculate basal metabolic rate using Mifflin-St Jeor formula
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    multiplier = { # activity level multipliers
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    calories = int(bmr * multiplier[profile.activity]) # calculate calories based on activity level
    days_left = (profile.goal_date - datetime.date.today()).days # calculate difference between today and goal date
    if profile.goal == 'maintain_weight':
        if calories < 1500: # check if its above the minimum safe daily calories
            print(f"Your calculated daily calories ({calories}) are too low. Setting to minimum safe value ({1500}).") # TO-DO pass it as a message and print it as an alert
            calories = 1500
        return calories
    else:
        weight_change = float(profile.goal_weight) - float(profile.current_weight) # calculate weight difference between current and goal
        if days_left > 0: # check if its a positive number of days to reach the goal
            adjustment = (weight_change * 3500) / days_left # approximation 0.5kg accounts for about 3500 kcal of energy
            if profile.goal == 'lose_weight': # adjust calories based on the user's goal
                calories += adjustment - 500 
            elif profile.goal == 'gain_weight':
                calories += adjustment + 500
        else:
            print(f"Your goal date has passed. Setting daily calories to fixed adjustement.") # TO-DO pass it as a message and print it as an alert
            if profile.goal == 'lose_weight':  # adjust calories based on the user's goal
                calories -= 500 
            elif profile.goal == 'gain_weight':
                calories += 500
    if calories < 1500: # check if its above the minimum safe daily calories
        print(f"Your calculated daily calories ({calories}) are too low. Setting to minimum safe value ({1500}).") # TO-DO pass it as a message and print it as an alert
        calories = 1500
    return int(calories)

def nutrition_list_from_api(request, inputstring):
    """Retrieves nutritional data from the REST API

        Parameters
        ----------
        request (HttpRequest): 
            The request object used to generate this response.
        inputstring : str
            the search keyword typed into the search bar

        Raises
        ------
        HTTPError
            If status code from get request is 3xx or 4xx it raises an exception
        Exception
            If the response contains no food, an exception is raised TODO: change that
        """
    
    API_KEY = 'JcPgeDeZOfKWAs52cv2PNyAWTBcREDeyKg7hhFyM'
    api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={inputstring}&pageSize=10&sortBy=dataType.keyword&sortOrder=asc"
    
    response = requests.get(api_url)
    response.raise_for_status()
    data =response.json()
   
    if 'foods' not in data :
        raise Exception("No foods found") #should be displayed on front end without actually throwing an exception

    nutrition_list = []
    for food in data['foods']:
        food_dict = {
            "name": food['description'],
            "fat": None,
            "protein": None,
            "carbohydrates": None,
            "calories": None
        }

        for nutrient in food['foodNutrients']:
            if nutrient['nutrientName'] == 'Total lipid (fat)':
                food_dict["fat"] = nutrient['value']
            elif nutrient['nutrientName'] == 'Protein':
                food_dict["protein"] = nutrient['value']
            elif nutrient['nutrientName'] == 'Carbohydrate, by difference':
                food_dict["carbohydrates"] = nutrient['value']
            elif nutrient['nutrientName'] == 'Energy':
                 food_dict['calories'] = nutrient['value']

        nutrition_list.append(food_dict)
    return render(request, 'app_itmunch/recipe.html', {'food_dict': food_dict})

def save_recipeFormula(ingredients, name):
    """Saves the recipe in the database

    Args:
        ingredients : {
            'name' : str,
            'fat' : float,
            'protein' : float,
            'carbhydrates' : float,
            'calories' : int,
            'weight' : float
        }
            Ingredients which are selected from the Nutrition API with a selected weigtht from the recipe html page

        name : str
            Name of the recipe

    Returns:
        TODO: add return
    """
    if (ingredients is None or name is None): raise ValueError()

    total_weight=0
    for ingredient_element in ingredients:
        total_weight+=ingredient_element['weight']

    try:
        recipe = RecipeFormula.objects.create(name = name)
    except:
        return("Recipe already exists")
    
    for ingredient_element in ingredients:
        nutriment = Nutriment.objects.get_or_create(name = ingredient_element['name'], fat = ingredient_element['fat'], protein = ingredient_element['protein'], carbohydrates = ingredient_element['carbohydrates'], calories = ingredient_element['calories'])
        RecipeIngredient.objects.create(super = nutriment, weight = ingredient_element['weight']/total_weight*100, recipe = recipe)

    return
        

