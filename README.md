# Antonia's — Flower Bouquet Commerce Website

A full-stack flower bouquet commerce website developed for **Antonia's**, designed to provide customers with an elegant and convenient way to browse flowers, explore bouquets by occasion and type, customize arrangements, manage favorites, and place orders.

The system is developed using **Django, HTML, Tailwind CSS, and JavaScript**, with a structured backend and database architecture suitable for a complete e-commerce workflow.

---

## Tech Stack

### Frontend

* HTML5
* Tailwind CSS
* JavaScript

### Backend

* Python
* Django

### Database

* Django ORM
* SQLite for local development
* Production database may be configured later

### Development Tools

* Git
* GitHub
* Visual Studio Code
* Node.js
* npm

### Design

* Figma

---

# Project Features

The planned website navigation includes:

* Home
* Occasions
* By Types
* Customize
* About
* Contact Us
* Favorites
* Cart
* User Profile
* User Settings

The website will eventually support features such as:

* Flower and bouquet browsing
* Product categories
* Occasion-based flower browsing
* Flower-type browsing
* Bouquet customization
* Favorites
* Shopping cart
* Customer accounts
* User profiles
* User settings
* Order management
* Contact/inquiry forms
* Administrative management
* Product and inventory management

---

# Prerequisites

Before working on the project, install the following:

* Python 3.12 or 3.13
* Git
* Node.js
* npm
* Visual Studio Code
* GitHub account

Verify the installations:

```bash
python --version
git --version
node --version
npm --version
```

---

# First Setup of the Project

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/antonias-flower-commerce.git
```

Enter the project:

```bash
cd antonias-flower-commerce
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should see:

```text
(venv)
```

in your terminal.

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If dependencies are added or changed, update the requirements file:

```bash
pip freeze > requirements.txt
```

---

## 4. Install Node Dependencies

```bash
npm install
```

---

## 5. Configure Environment Variables

Create a local:

```text
.env
```

file.

Use `.env.example` as a reference.

Do not commit `.env` to GitHub.

---

## 6. Run Database Migrations

```bash
python manage.py migrate
```

---

## 7. Create a Django Admin Account

```bash
python manage.py createsuperuser
```

Follow the prompts.

---

## 8. Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Admin Access

The Django administration panel can be accessed locally at:

```text
http://127.0.0.1:8000/admin/
```

Each administrator should have their own Django account.

Do not share administrator passwords.

The admin panel will eventually be used to manage:

* Products
* Flowers
* Bouquets
* Categories
* Occasions
* Customization options
* Orders
* Customers
* Inventory
* Other system data

---

# Git Branching Strategy

The `main` branch is the stable project branch.

Members must NOT directly work on `main`.

Use feature branches instead.

Recommended naming:

```text
frontend/feature-name
backend/feature-name
database/feature-name
figma/feature-name
docs/feature-name
```

Examples:

```text
frontend/homepage
frontend/navbar
frontend/product-card

backend/user-authentication
backend/product-model
backend/cart

database/product-schema

docs/project-documentation
```

---

# Push Guide

## 1. Make Sure You Are on Your Feature Branch

```bash
git branch
```

Example:

```text
* frontend/homepage
  main
```

---

## 2. Check Your Changes

```bash
git status
```

---

## 3. Add Your Changes

```bash
git add .
```

---

## 4. Commit Your Changes

Use a clear commit message.

Example:

```bash
git commit -m "feat: create homepage layout"
```

Other examples:

```text
feat: add product model
fix: correct cart quantity calculation
style: improve navbar spacing
docs: update installation guide
refactor: reorganize catalog views
```

---

## 5. Push Your Branch

```bash
git push -u origin frontend/homepage
```

For future pushes:

```bash
git push
```

---

## 6. Create a Pull Request

Go to GitHub and create a Pull Request.

Set:

```text
base: main
compare: your-feature-branch
```

Explain:

* What you changed
* Why you changed it
* What you tested
* Any known issues

Wait for the appropriate leader to review your work.

Do not merge your own Pull Request unless you have been specifically authorized to do so.

---

# Pull Guide

Before beginning work, always make sure your local repository is updated.

## 1. Switch to Main

```bash
git checkout main
```

---

## 2. Pull the Latest Changes

```bash
git pull origin main
```

---

## 3. Return to Your Branch

```bash
git checkout your-branch-name
```

Example:

```bash
git checkout frontend/homepage
```

---

## 4. Update Your Feature Branch

```bash
git merge main
```

Resolve conflicts if necessary.

Then continue your work.

---

# Recommended Daily Workflow

Every development session should generally follow:

```text
1. git checkout main
2. git pull origin main
3. git checkout your-feature-branch
4. git merge main
5. Work on your assigned task
6. Test your changes
7. git status
8. git add .
9. git commit
10. git push
11. Create / update Pull Request
12. Wait for review
13. Leader merges into main
```

---

# Main Branch Policy

The `main` branch is the stable branch of the project.

Members should:

* Never directly develop on `main`
* Never force push to `main`
* Never delete `main`
* Never commit passwords or secret keys
* Never merge untested code
* Never overwrite another member's work
* Always use feature branches
* Always create Pull Requests
* Wait for leader approval before merging

Only authorized project leaders should merge approved work into `main`.

---

# Team Members

## Team Leader

**Joshua Barotea**

---

## Figma Design Team

### Figma Design Leader

**Mark Angelo Talento**

### Members

1. Savannah Mari De Mesa
2. Karl Louise Sebuc

---

## Front End Team

### Front End Leader

**John Kevin Aguilera**

### Members

1. Franz Jowen Rances
2. John Benedict Fernandez
3. Cielo Seco

---

## Back End Team

### Back End Leader

**Joshua Barotea**

### Members

1. Jayvee Garcia
2. Rafael Metran
3. Dishiela Ingrid Camunag

---

## Database Team

### Database Leader

**Edrian Paul Domanico**

### Members

1. Mark Anthony Llanora
2. Stephanie Marie Nanoy

---

## Documentation Team

### Members

1. Carl Demandante Chua
2. Gabriel Clinton Diaz

---

# Team Responsibilities

## Figma Design Team

Responsible for:

* UI/UX design
* Figma layouts
* Design system
* Colors
* Typography
* Components
* User flows
* Responsive designs

---

## Front End Team

Responsible for:

* HTML
* Tailwind CSS
* JavaScript
* Django templates
* Responsive layouts
* Frontend interactions
* Client-side functionality

---

## Back End Team

Responsible for:

* Django
* Models
* Views
* URLs
* Authentication
* Business logic
* Backend functionality
* Server-side validation

---

## Database Team

Responsible for:

* Database design
* ERD
* Django models
* Relationships
* Migrations
* Data integrity
* Database documentation

---

## Documentation Team

Responsible for:

* Technical documentation
* User documentation
* Installation instructions
* System documentation
* Screenshots
* Project reports

---

# Notes for Members

## 1. Always Pull Before Starting

Before working:

```bash
git checkout main
git pull origin main
```

Then update your feature branch.

---

## 2. Do Not Work Directly on Main

Never use:

```bash
git checkout main
```

and start developing there.

Use a feature branch.

---

## 3. Keep Commits Small

Avoid:

```text
final changes
```

Prefer:

```text
feat: add flower category model
```

or:

```text
fix: correct product image loading
```

---

## 4. Test Before Pushing

Before creating a Pull Request:

```bash
python manage.py check
```

Run the development server:

```bash
python manage.py runserver
```

Check the affected functionality.

---

## 5. Do Not Commit Secrets

Never commit:

```text
.env
passwords
API keys
SECRET_KEY
database passwords
personal credentials
```

---

## 6. Do Not Modify Another Team's Work Without Communication

If your task requires modifying another team's files, communicate with that team's leader first.

Example:

The Front End team needs to change a Django model.

Contact:

**Back End / Database team**

before making structural changes.

---

## 7. Database Changes Must Be Communicated

If you modify:

```text
models.py
```

you may need to create migrations:

```bash
python manage.py makemigrations
```

then:

```bash
python manage.py migrate
```

Notify the Database team when making significant database changes.

---

## 8. Resolve Merge Conflicts Carefully

Do not blindly choose:

```text
Accept Current
```

or:

```text
Accept Incoming
```

Understand what each side changed before resolving the conflict.

---

## 9. Keep the Project Organized

Do not randomly create files in the project root.

Follow the established structure:

```text
templates/
static/
apps/
docs/
tests/
```

---

## 10. Ask Before Changing Project Architecture

Changes to:

* Django settings
* Database architecture
* Authentication
* Main URLs
* Project structure
* Dependencies
* Deployment configuration

should be discussed with the appropriate leader first.

---

# Development Philosophy

Antonia's should be developed as a team project rather than as separate pieces of code.

The goal is to maintain:

* Clean code
* Consistent design
* Organized files
* Clear Git history
* Stable database structure
* Tested features
* Proper documentation
* Controlled access to the main branch

Every member is responsible for keeping the repository clean and maintainable.

---

# Project Status

**Status:** Initial Development

The current repository may initially contain only the project structure and configuration. Features will be progressively implemented by the assigned teams.

---

# Antonia's

**Flower Bouquet Commerce Website**

Built with:

```text
Django
HTML
Tailwind CSS
JavaScript
```
