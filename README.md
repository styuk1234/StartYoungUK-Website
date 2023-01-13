<h1 align="center">StartYoungUK Website Overhaul by Team Young Coders</h1>

<div align="center">
<img src = "https://github.com/arghyadeep99/CodeFest-StartYoungUK-YoungCoders/blob/main/home/static/images/startyounguk-logo.jpg" width="250" />

<br>
<img src = "https://img.shields.io/badge/Made_with-Django-blue?style=for-the-badge&logo=django" />
<img src = "https://img.shields.io/badge/Made_with-JavaScript-blue?style=for-the-badge&logo=javascript"/>
<img src = "https://img.shields.io/badge/Chatbot-Power_Virtual_Agents-blue?style=for-the-badge&logo=power-virtual-agents"/>
<img src = "https://img.shields.io/badge/Dashboard-PowerBI-blue?style=for-the-badge&logo=powerbi"/>
<img src = "https://img.shields.io/badge/Database-Azure_SQL-blue?style=for-the-badge&logo=microsoft-sql-server" />
<img src = "https://img.shields.io/badge/CI/CD-Github_Actions-blue?style=for-the-badge&logo=github-actions" />
<img src = "https://img.shields.io/badge/Deployed_on-Azure_App_Services-blue?style=for-the-badge&logo=microsoft-azure" />


<br>

</div>

---

<b>Submission for CodeFest Hackathon by Barclays 💖</b> 

<b> UPDATE: This project won the first prize for the given problem statement by Start Young UK and Barclays. A blog on our journey to build this website is coming up soon! </b>

---

### About

StartYoungUK is a brand new NGO that is looking for growing its footprint within UK to reach out to help more children in need, contact sponsors for their noble charity work, onboard mentors and engage with more schools to help their children directly. They were in need of more advanced capabilities on their website to drive their growth, sponsorship and engagement.

**StartYoungUK Website Overhaul** is an attempt by **Team Young Coders** to re-design the entire website as part of Barclays' CodeFest Hackathon 2022, sponsored by Microsoft! Our solution focusses on growing their sponsorship and engagement, which is a driving force behind their growth. Hence, we have tried to touch on all three pillars through our attempt. This repository contains the winning solution of the global round that happened across the United Kingdom, India and the United States!

---

#### Start Young UK Website Screenshots

#### 1. Homepage
[homepage-screencast.webm](https://user-images.githubusercontent.com/33197180/193996609-e6255009-6f92-4fd6-99ae-8305564a51f5.webm)

#### 2. Chatbot
[chatbot-screencast.webm](https://user-images.githubusercontent.com/33197180/193992426-333b5f0c-e80d-4180-a6e8-4e55ac32f074.webm)

#### 3. About Page
[about-screencast.webm](https://user-images.githubusercontent.com/33197180/194051685-05dc6cee-7086-4bd5-a9f5-403006f5a2fb.webm)

#### 4. Contact Us Page
[contact-screencast.webm](https://user-images.githubusercontent.com/33197180/194051287-0946140a-1702-4074-87b2-5c6ed05ee72a.webm)

#### 5. Buddy System Page
[buddy-screencast.webm](https://user-images.githubusercontent.com/33197180/194052240-06a45b9c-a722-456c-83ce-6c76870abc9c.webm)

#### 6. Donate Page
[donate-screencast.webm](https://user-images.githubusercontent.com/33197180/194054216-ff627aac-b968-4908-ac23-3c2add502315.webm)


---

### Features

* Overhauled About, Contact Us, Buddy System and Home Page
* **Campaigns**: Allow admins to create campaigns on the fly and broadcast on home page for people to donate to!
* **Top Donors**: Showcase our top donors to motivate visitors to make donations for noble cause!
* **Donation Types**: Donations can be of multiple types, and we don't want to limit it to just the traditional way:
  * **Ad-hoc Donations**: Users can donate upto £50 on an ad-hoc basis by filling out simple details for donation. Donators receive a tax receipt and note of thanks provided they entered a correct email.
  * **Registered Donations**: For donations beyond £50, users can sign up as either individual or corporate. This is to ensure that no major financial transaction is being converted to white through charity donations and evade taxes.
  * **Systematic Donation Plan (SDP)**: Just like Systematic Investment Plan (SIP) where one dedicates a fixed amount of money to an investment plan, SDP allows users to make systematic donations with a value and frequency of user's choice!
  * **Donate in Kind**: Not all donations have to be made in monetary terms. It can be in terms of your volunteering time, your service, books, clothes, gifts donation, etc. One can express their interests for such kind of donations on our website!
* **Two-step verification for Individuals/Corporate Registration**: When corporates sign up for our website, they are asked for their Company Registration Number (CRN), which is used as the second step to ensure the admin can verify the CRN to be valid. When the user completes registration, they can't immediately login, as they have to verify their email first by clicking on the link sent on their email. Once verified, they can login, but the admin has a checkbox in the admin panel against each user called "is_verified", which when ticked after manual verification, gives the users full access to content like onboarded children information, schools, etc. The same logic is used for individuals, except that they aren't asked for their CRN as it's not applicable.
* **ReCAPTCHA protection from bot attacks on registration/login**: ReCAPTCHA has been added to login and registration pages to avoid bot-based attacks.
* **Individual Features**: 
  * **Mentor A Child - Recommender System**: A vanilla implementation of a recommender system using highest overlap of common hobbies between a mentor and children database to recommend children to mentors for mentoring.
* **Corporate Features**:
  * **Start a Campaign**: Corporates can initiate campaigns with StartYoungUK, like match funding, etc. Corporates need to fill up basic details about the campaign and submit. An admin has full control to modify the campaigns if not deemed fit. 
* **Chatbot using Power Virtual Agents**: We built a simple chatbot using Power Virtual Agents to help users new to the website navigate direcly to things they want to do on the website, just by chatting to our bot! The bot provides links specific to the functionalities of our website.
* **Simplified Admin Experience**: The admin login provides admin complete control over managing database of users, donations, campaigns, mentors, children, etc. 
* **Statistics Dashboard using PowerBI**: PowerBI has been leveraged to generate statistics dashboard for the admin, to get useful insights into how their website is growing, in terms of onboarding mentors, children, sponsors, mentor-mentee mapping, etc. 
* **Leveraging Security Features of Azure**: Azure provides a lot of out-of-the-box security features in terms of HTTPS, VPN, Firewall, TLS, IAM, etc. Some of these features have been leveraged, placing trust on the Azure ecosystem to safeguard the information of different entities.

---

### Future scope of this project

* [ ] Allow registration of more personas like School and Child
* [ ] Implement Update Profile for different user personas
* [ ] Implement a common UI theme and page branding across all pages, including admin page
* [ ] Integrate Donation endpoints with Payment gateways to make them functional
* [ ] Use OAuth and IAM of Azure to register users more securely onto our website
* [ ] Extend ReCAPTCHA to ad-hoc donation forms
* [ ] Build a delayed chat feature between mentor and child to replace current system of letter writing (Example: [Slowly](https://slowly.app/en/))
* [ ] Integrate Natural Language Processing (NLP) to moderate letter content before it's delivered to child by leveraging Azure Content Moderation API
* [ ] Introduce gift boxes in Donate tab for people to make monetary donations specific to gift boxes that can help a child
* [ ] Implement curated newsletter based on user persona (Mentor, Corporate, Child) for registered users, that can be opted out any time
* [ ] Block edit capability of admin for any financial transaction table

### Tech Stack of our Project

* Frontend: HTML, CSS, JavaScript, Bootstrap4, Jinja2
* Backend: Django (Python3)
* Database: Microsoft SQL for Azure
* Chatbot: Power Virtual Agents
* Dashboard: PowerBI
* Libraries: Available in [requirements.txt](https://github.com/arghyadeep99/CodeFest-StartYoungUK-YoungCoders/blob/main/requirements.txt).

#### This project still has scope of development, so you can also contribute to this project as follows:
* [Fork](https://github.com/arghyadeep99/CodeFest-StartYoungUK-YoungCoders) this Repository.
* Clone your Fork on a different branch:
	* `git clone -b <name-of-branch> https://github.com/arghyadeep99/CodeFest-StartYoungUK-YoungCoders.git`
* cd into the repository on terminal and run `pip3 install -r requirements.txt`
* Delete the db.sqlite3 file in root of this repository.
* Next, run the following command: `python3 manage.py migrate`. This will create the required tables in your SQLite3 database.
* Create a Django superuser by the following command: `python3 manage.py createsuperuser`
* Enter your desired username and password values
* Finally, to run the project, enter in terminal: `python3 manage.py runserver`
* This will generate a link to open in localhost at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* To login as a superuser, go to http://127.0.0.1:8000/admin

* After adding any feature:
	* Go to your fork and create a pull request.
	* We will test your modifications and merge changes.


---
<h3 align="center"><b>Developed with :heart: by Team Young Coders</b></h1>
