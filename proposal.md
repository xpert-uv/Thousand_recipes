Project Proposal:

1.	What goal will your website be designed to achieve?
It will help the user to search for food recipes and cocktails recipes. Along with, suggest the matching wine for meal. 

2.	What kind of users will visit your site? In other words, what is the demographic of your users?
This website has wide range of users. Anybody, above the age of four can use this website. This application is for those who has even slightest interest in cooking, and those who wonder what wine should I drink with this meal? In addition, people form culinary world to every mom in household can use this website.

3.	What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.

4.	 What does your database schema look like?
User (id, username, password, first name, last name, email-(for sending validation code or email))
Food (id, Name, description/history, Ingredients, Methods, Prep-time, image_url)
Cocktails (id, Name, description/history, Ingredients, Methods, image_url)
Wine (id, Name, Image, description)
WinePair (id, Food, Wine; this will store the wine paired with food)
It may change as needed, still in working progess.

5.	 What kinds of issues might you run into with your API? 
-	Not sure yet

6.	Is there any sensitive information you need to secure?
-	User’s details like:
Username, password

7.	 What functionality will your app include? 
Restful API convention will be used and all the external api request will be from server side. Search tab should display the suggestions for keywords in real-time. 

8.	What will the user flow look like? 
Landing page with SingUp and LogIn button, Once loged-in Home page will provide the search bar and display results. Result will consist of image, Food name, description, prep time , Ingredients ,methods and save button.
Home page will have navbar allowing users to go back and forth. 
[Home | myRecipies | CoktailsRecpies | Wine | WineParing |          logout]  

9.	 What features make your site more than CRUD? Do you have any stretch goals?  
Authentication and Authorization, search features will be added.   
 
