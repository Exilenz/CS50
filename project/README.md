# Password manager
#### Video Demo:  <(https://youtu.be/nhSDZ8jrCl0)>
#### Description:
- Welcome to Password Manager, my final project for CS50 2024.
- The aim of this Flask app is to store and manage your passwords at one place.
- App is programed in Flask, using Python, SQLite, Jinja, Boostarp and JavaScript-As run the program you will get on Log in page.
- Log in is required so you have to either Log in or if you don't have account yet then you have to register.
- On the top of your screen there is nav bar, on left site is name of the project that you can click and it will take you to the index.html page. On the right side of nav bar you can click log in or register.
- If you are going to register you will have to fill in your username, password and then confirm your password then you will click blue Register button, your password will be hashed.
- When username is already taken or password are not matching you will see the red line (flash) with instructions, if your registration will be successfull you will get green flash.
- After logging in you will see your accounts table.
- Right side of navbar now have options to Log out for logging out and Add account for adding account.
- You can add your account by clicking green Add new account button and then fill in website/platform, username and password and click Submit button, there is also possibility to click Generate strong password, if you click it you will get new random generated password that should be strong.
- There is restriction for adding new account, website and username needs to be unique.
- If input will be against the restriction, you will get red flash with instructions. If your input will pass this condition you will get green flash
- As database and table will be updated you will see your added account details, however password will not be visible. You have to click button Show and your password will appear, then button will change to Hide and you can hide your password again.
- There is blue Edit button after clicking this button your account detail will be displayed and you can change website/platform, username and password, you will confirm changes by clicking Apply button. There is also possibility to generate new strong password. You still can't use already existing combination of website/platform and username, if so you will get red flash.
- If you will fullfill the requirements you will have a green flash.
- Table will be updated and you will see the changes that you made
- There is also button Delete for deleting the entire account, after clicking this your account will be deleted and you will get green flash.
- When you click Log out button on the nav bar you will be logged out, session will end green flash will appear and log in page will be displayed.

#### Design Choices
- utilizing Boostarp for nav bar, icons, responsive design and improved styling.
- utilizing Javascript for Show/hide password button on index.html page
- utilizing Jinja mainly for extending base.html page
- utilizing sqlite3 for databases

#### app.py
- Python coded back-end of the password manager, navigating through the pages.
- hash
- routing index, register, login, log out, account adding, account editing, account deleting
- working with databases
- flashes
-

#### password_manager.db
- Database file storing 2 tables, users and passwords.
- Users table - is used for registration and loggin in / out users. Contains autoincremented integer ID that is also primary key, Text form of unique username and text form of password.
- Passwords table - this is used for creating, updating and deleting of the accounts. Contains autoincremented integer ID that is also primary key for each account, integer of user_id that helps to see which user posted account and is has foreign key of id from users table, website that is in form of text, username with form of text, password in form of text. Combination of username and website needs to be unique.

#### base.html
- Sort of template, storing nav bar that is used by other .html files, it also modifies alerts(flashes)

#### index.html
- Serves as overview of accounts added by logged user (displaying the passwords table).
- It also has option for adding, editing and deleting accounts.
- The styles for buttons and table are stored here.

#### login.html
- Storing form and styles for logging in the users
- Delete and Edit buttons and it styles are stored here
#### register.html
- Storing form and styles for registering the new users

#### add_accout.html
- Storing styles for adding new account Add account button
- Generate strong password button and script

#### edit_accout.html
- Storing styles for adding new account Apply account button
- Generate strong password button and script
