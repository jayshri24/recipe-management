# 🍳 Acme Recipe Management Backend

A **GraphQL-powered Recipe Management Application** built using **Django**, **Django REST Framework**, and **Graphene Django**, allowing authenticated users to manage ingredients and recipes seamlessly.

---

## 🚀 Objective

Acme Inc. is creating a recipe management application where users can create and manage 
ingredients and recipe. Create a backend application utilizing Django, Django Rest Framework and 
Graphene or Strawberry Django (for GraphQL).

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Framework** | Django (latest) |
| **API** | GraphQL (Graphene Django) |
| **Auth** | Django Authentication |
| **Database** | PostgreSQL / SQLite / MySQL
| **Optional Deployments** | Heroku / Render / Netlify (for bonus points) |

---

## 🧠 Features & Specifications

We require GraphQL queries for the following: 
- Create, Update, Delete ingredients in/from the database. 
- List all ingredients from the database and also have filters and pagination while listing. 
- Create a recipe and connect few ingredients to it (in the same request). 
- Get details of a recipe and see all its ingredients 
    - We want a calculated ingredient_count field for the recipe Node, which will give us the count of ingredients attached to a recipe. This should be a calculated field and not a database field. 
- Add/remove ingredients from a recipe 
#### Important Points to be included in the implementation 
- Basic Django authentication can be used, but the GraphQL endpoints have to be allowed only for authenticated users. Do not implement login/signup web pages. We are okay to use createsuperuser management command to create a user. You may need to create a REST API endpoint to get the user’s signed-in access_token. 
- Make sure that the code is clean and easy to read / understand. 
- Make sure you use GraphQL (Graphene Django or Strawberry) for listing and mutations. 
- Bonus points for using Django rest framework serializers with the GraphQL mutations. 


## Toolkit  
Acme Inc. is very opinionated about their tech stack. The tools should be:  
- Framework: Django (Latest version) 
- Data storage – You can store the data anywhere you want; you can use Heroku PostgreSQL, or any other free PostgreSQL database on cloud. 
- All responses must be in json format. 
---

## Next Steps

- Build the app  
- Push the code to your GitHub account into a public repo and share the repo with us. The code that you sent to us should be runnable error free on our side. 
- Deploy the app in any free service such as Netlify, Heroku, etc and send us the link to the app (This is optional, but will get bonus points) 


Feel free to contact me at arun.thomas@twistedmountainanimation.com for any queries.
 




// this are the useful mutation

// mutation {
//   tokenAuth(username: "admin", password: "Admin@123") {
//     token
//   }
// }

// query{
//   allIngredients(limit:5){
//     id
//     name
//   }
// }

// query {
//   allRecipes {
//     id
//     title
//   }
// }

// mutation {
//   createIngredient(name: "test") {
//     ingredient {
//       id
//       name
//     }
//   }
// }


// mutation {
//   createRecipe(
//     title: "Tea",
//     ingredients: [
//       {name: "Salt"},
//       {name: "Sugar"}
//     ]
//   ) {
//     recipe {
//       id
//       title
//       ingredientCount
//     }
//   }
// }

// mutation {
//   addIngredientsToRecipe(recipeId: 1, ingredientIds: [2, 3]) {
//     recipe {
//       id
//       title
//       ingredientCount
//     }
//   }
// }

// mutation {
//   removeIngredientsFromRecipe(recipeId: 1, ingredientIds: [3]) {
//     recipe {
//       id
//       title
//       ingredientCount
//     }
//   }
// }

// mutation {
//   updateIngredient(id: 10, name: "updated test") {
//     ingredient {
//       id
//       name
//     }
//   }
// }

// mutation {
//   deleteIngredient(id: 2) {
//     ok
//   }
// }
