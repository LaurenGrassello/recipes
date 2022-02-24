from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

from flask_app.controllers import recipes 


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.under_30_min = data['under_30_min']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []


    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL("recipes").query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes


    @classmethod
    def new_recipe(cls,data):
        query = "INSERT INTO recipes (user_id, name, description, under_30_min, instructions, date_made, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(description)s, %(under_30_min)s, %(instructions)s, %(date_made)s ,NOW(), NOW());"
        return connectToMySQL("recipes").query_db(query, data)

    
    @classmethod
    def select_recipe_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL("recipes").query_db(query,data)
        return cls(results[0])

    
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query,data)


    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_min = %(under_30_min)s, instructions = %(instructions)s, date_made = %(date_made)s WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)


    @staticmethod
    def validate_recipe(data):
        is_valid = True 
        if len(data['name']) < 3:
            flash("Recipe name must be at least 3 characters.", "new_recipe")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.", "new_recipe")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "new_recipe")
            is_valid = False
        if data['date_made'] == " ":
            is_valid = False
            flash("Date must be included", "new_recipe")
        return is_valid
        