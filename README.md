<h1 align="center">Start Young UK Website by Team Young Coders</h1>

<div align="center">
<img src = "https://github.com/styuk1234/StartYoungUK-Website/blob/main/home/static/images/syuk-logo.png" />
<br>
<br>

[![Build and Deployment Status on Azure](https://github.com/styuk1234/StartYoungUK-Website/actions/workflows/main_startyoung-uk.yml/badge.svg)](https://github.com/styuk1234/StartYoungUK-Website/actions/workflows/main_startyoung-uk.yml)
[![CodeQL Status](https://github.com/styuk1234/StartYoungUK-Website/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/styuk1234/StartYoungUK-Website/actions/workflows/codeql-analysis.yml)

<img src = "https://img.shields.io/badge/Made_with-Django-blue?style=for-the-badge&logo=django" />
<img src = "https://img.shields.io/badge/Made_with-JavaScript-blue?style=for-the-badge&logo=javascript"/>
<img src = "https://img.shields.io/badge/Chatbot-Power_Virtual_Agents-blue?style=for-the-badge&logo=power-virtual-agents"/>
<img src = "https://img.shields.io/badge/Dashboard-PowerBI-blue?style=for-the-badge&logo=powerbi"/>
<img src = "https://img.shields.io/badge/Database-PostgreSQL-blue?style=for-the-badge&logo=postgresql" />
<img src = "https://img.shields.io/badge/CI/CD-Github_Actions-blue?style=for-the-badge&logo=github-actions" />
<img src = "https://img.shields.io/badge/Deployed_on-Azure_App_Services-blue?style=for-the-badge&logo=microsoft-azure" />

<br>
  
</div>

---

<b>Website by Team Young Coders in CodeFest 2022 Hackathon! 💖</b>

<b> UPDATE: This project won the first prize for the given problem statement by Start Young UK and Barclays. A blog on our journey to build this website is coming up soon! </b>

---

### About

StartYoungUK is a brand new NGO that is looking to grow its footprint within the UK to reach out to help more children in need, contact sponsors for their noble charity work, onboard mentors, and engage with more schools to help their children directly. They needed more advanced capabilities on their website to drive their growth, sponsorship, and engagement.

**StartYoungUK Website Overhaul** is an attempt by **Team Young Coders** to re-design the entire website as part of Barclays' CodeFest Hackathon 2022, sponsored by Microsoft! Our solution focuses on growing their sponsorship and engagement, which is a driving force behind their growth. Hence, we have tried to touch on all three pillars through our attempt. This repository contains the winning solution of the global round that happened across the United Kingdom, India, and the United States!

---

### Features

- Overhauled About, Contact Us, Buddy System and Home Page
- **Campaigns**: Allow admins to create campaigns on the fly and broadcast them on the home page for people to donate to!
- **Top Donors**: Showcase our top donors to motivate visitors to make donations to noble cause!
- **Donation Types**: Donations can be of multiple types, and we don't want to limit it to just the traditional way:
  - **Ad-hoc Donations**: Users can donate up to £50 on an ad-hoc basis by filling out simple details for donation. Donators receive a tax receipt and note of thanks provided they entered the correct email.
  - **Registered Donations**: For donations beyond £50, users can sign up as either individual or corporate. This is to ensure that no major financial transaction is being converted to white through charity donations and evading taxes.
  - **Recurring Donation Plan (RDP)**: Just like a Systematic Investment Plan (SIP) where one dedicates a fixed amount of money to an investment plan, SDP allows users to make systematic donations with a value and frequency of their choice!
  - **Donate in Kind**: Not all donations have to be made in monetary terms. It can be in terms of your volunteering time, your service, books, clothes, gifts donations, etc. One can express their interest in such kinds of donations on our website!
- **Two-step verification for Individuals/Corporate Registration**: When corporates sign up for our website, they are asked for their Company Registration Number (CRN), which is used as the second step to ensure the admin can verify the CRN to be valid. When the user completes registration, they can't immediately login, as they have to verify their email first by clicking on the link sent to their email. Once verified, they can log in, but the admin has a checkbox in the admin panel against each user called "is_verified", which when ticked after manual verification, gives the users full access to content like onboarded children information, schools, etc. The same logic is used for individuals, except that they aren't asked for their CRN as it's not applicable.
- **ReCAPTCHA protection from bot attacks on the registration/login**: ReCAPTCHA has been added to log-in and registration pages to avoid bot-based attacks.
- **Individual Features**:
  - **Mentor A Child - Recommender System**: A vanilla implementation of a recommender system using the highest overlap of common hobbies between a mentor and children database to recommend children to mentors for mentoring.
- **Corporate Features**:
  - **Start a Campaign**: Corporates can initiate campaigns with StartYoungUK, like match funding, etc. Corporates need to fill up basic details about the campaign and submit. An admin has full control to modify the campaigns if not deemed fit.
- **Chatbot using Power Virtual Agents**: We built a simple chatbot using Power Virtual Agents to help users new to the website navigate directly to things they want to do on the website, just by chatting with our bot! The bot provides links specific to the functionalities of our website.
- **Simplified Admin Experience**: The admin login provides admin complete control over managing the database of users, donations, campaigns, mentors, children, etc.
- **Statistics Dashboard using PowerBI**: PowerBI has been leveraged to generate a statistics dashboard for the admin, to get useful insights into how their website is growing, in terms of onboarding mentors, children, sponsors, mentor-mentee mapping, etc.
- **Leveraging Security Features of Azure**: Azure provides a lot of out-of-the-box security features in terms of HTTPS, VPN, Firewall, TLS, IAM, etc. Some of these features have been leveraged, placing trust in the Azure ecosystem to safeguard the information of different entities.

---

### Future scope of this project

- [ ] Allow registration of more personas like School and Child
- [x] Implement Update Profile feature for different user personas
- [x] Implement a common UI theme and page branding across all pages
- [x] Integrate Donation endpoints with Payment gateways to make them functional
- [ ] Use OAuth and IAM of Azure to register users more seamlessly
- [x] Extend ReCAPTCHA to ad-hoc donation forms
- [ ] Build a delayed chat feature between mentor and child to replace the current system of letter writing (Example: [Slowly](https://slowly.app/en/))
- [ ] Integrate Natural Language Processing (NLP) to moderate letter content before it's delivered to the child by leveraging Azure Content Moderation API
- [x] Introduce gift boxes in the Donate tab for people to make monetary donations specific to gift boxes that can help a child
- [x] Block edit capability of admin for any financial transaction table
- [x] Maximum website customization for admin from admin portal
- [x] Buddy Letter Tracking Feature for admins
- [x] Buddy Approval feature for admins
- [x] Export functionality for admin-related tables as CSVs
- [x]  Past donation history and receipt download for registered users

### Tech Stack of our Project

- Frontend: HTML, CSS, JavaScript, Bootstrap4, Jinja2
- Backend: Django (Python3)
- Database: PostgreSQL on Azure
- Chatbot: Power Virtual Agents
- Dashboard: PowerBI
- Libraries: Available in [requirements.txt](https://github.com/styuk1234/StartYoungUK-Website/blob/main/requirements.txt)).

#### This project still has scope for development, so you can also contribute to this project as follows:

- [Fork](https://github.com/styuk1234/StartYoungUK-Website) this Repository.
- Clone your Fork on a different branch:
  - `git clone -b <name-of-branch> https://github.com/styuk1234/StartYoungUK-Website.git`
- cd into the repository on the terminal and run `pip3 install -r requirements.txt`
- Delete the db.sqlite3 file in the root of this repository.
- Create a `.env` file based on the `.testenv` template in this repository.
- Next, run the following command: `python3 manage.py migrate`. This will create the required tables in your SQLite3 database.
- Create a Django superuser by the following command: `python3 manage.py createsuperuser`
- Enter your desired username and password values
- Finally, to run the project, enter in terminal: `python3 manage.py runserver`
- This will generate a link to open in localhost at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- To log in as a superuser, go to http://127.0.0.1:8000/admin

- After adding any feature:
  - Go to your fork and create a pull request.
  - We will test your modifications and merge changes.

### Enabling Paypal Donations

A secure (https) host is needed for the website to accept PayPal donations. In development, this can be achieved via installing Ngrok on your machine and running the project through the secure public gateway. Follow the steps below to do this:

- Install [ngrok](https://ngrok.com/download).
- Run `ngrok http 8000` to get a public URL.
- Start your Django project in a separate terminal window.
- In the terminal where ngrok is run, you should see a similar message:

      Forwarding https://569a-2a04-4a43-95bf-f3c0-95be-f1df-416d-f34b.eu.ngrok.io -> http://localhost:8000

- You can now access your Django project on the public URL and your application should now be able to accept PayPal donations!

---

<h3 align="center"><b>Developed with :heart: by Team Young Coders</b></h1>
