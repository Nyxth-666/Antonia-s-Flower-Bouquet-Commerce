# Antonia's — Team Member Development Guide

## Flower Bouquet Commerce Website

This guide explains how every team member should set up the Antonia's project after receiving access to the GitHub repository and how to properly work on their assigned tasks.

---

# 1. Before You Start

Make sure you have installed:

* Git
* Python 3.12 or 3.13
* Node.js
* npm
* Visual Studio Code
* A GitHub account

Check your installations:

```bash
python --version
git --version
node --version
npm --version
```

You should be able to see the installed versions.

---

# 2. Clone the Repository

Get the repository URL from the team leader.

Example:

```bash
git clone https://github.com/YOUR-USERNAME/Antonia-s-Flower-Bouquet-Commerce.git
```

Then enter the project:

```bash
cd Antonia-s-Flower-Bouquet-Commerce
```

Open the project in VS Code:

```bash
code .
```

---

# 3. Check the Repository

After cloning, check the available files:

```bash
git status
```

You should see something similar to:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

You can also check the branches:

```bash
git branch
```

Initially, you will probably only have:

```text
* main
```

This is normal.

---

# 4. Create Your Virtual Environment

Each developer should have their own Python virtual environment.

Do NOT copy another member's `venv` folder.

Create yours:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

You should now see:

```text
(venv)
```

at the beginning of your terminal.

Example:

```text
(venv) PS C:\Users\YourName\Antonia-s-Flower-Bouquet-Commerce>
```

---

# 5. Install Python Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs the project's Django and Python dependencies.

---

# 6. Install Node Dependencies

Run:

```bash
npm install
```

This installs the project's JavaScript/Tailwind dependencies.

Do not manually copy `node_modules` from another computer.

Every developer should generate their own `node_modules` by running:

```bash
npm install
```

---

# 7. Configure Your Environment

The repository contains:

```text
.env.example
```

Create your own:

```text
.env
```

Copy the contents of `.env.example` into `.env`.

Example:

```env
SECRET_KEY=your-local-secret-key
DEBUG=True

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

The `.env` file is personal/local and must NOT be pushed to GitHub.

Never commit:

```text
.env
```

---

# 8. Run Django Migrations

Run:

```bash
python manage.py migrate
```

This prepares your local database.

The local database may be created as:

```text
db.sqlite3
```

Do not commit your local `db.sqlite3` unless the team leader specifically instructs you to do so.

---

# 9. Check the Django Project

Run:

```bash
python manage.py check
```

You should get:

```text
System check identified no issues (0 silenced).
```

If you receive an error, fix it before starting development.

If you cannot solve the problem, contact your appropriate team leader.

---

# 10. Run the Website

Start Django:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Make sure the website loads.

Stop the server with:

```text
CTRL + C
```

---

# 11. Create Your Own Git Branch

NEVER work directly on `main`.

Before creating your branch:

```bash
git checkout main
```

Update your local `main`:

```bash
git pull origin main
```

Then create your branch.

---

# 12. Branch Naming Convention

Use the team category followed by the task.

### Frontend

```text
frontend/homepage
frontend/navbar
frontend/catalog
frontend/customization
```

### Backend

```text
backend/authentication
backend/products
backend/cart
backend/orders
```

### Database

```text
database/product-model
database/order-model
database/user-model
```

### Documentation

```text
docs/project-documentation
docs/user-guide
docs/database-documentation
```

### Figma

Figma work does not necessarily need a Git branch unless design files or related project files are being stored in the repository.

---

# 13. Example: Creating Your Branch

Suppose you are working on the homepage.

Run:

```bash
git checkout -b frontend/homepage
```

Check:

```bash
git branch
```

You should see:

```text
* frontend/homepage
  main
```

The `*` indicates your current branch.

---

# 14. Start Working

You can now begin your assigned task.

For example:

```text
frontend/homepage
        ↓
templates/home/
        ↓
index.html
```

The Frontend team may work with:

```text
templates/
static/css/
static/js/
static/images/
```

Backend members may work with:

```text
apps/
config/
```

Database members may primarily work with:

```text
apps/*/models.py
```

Documentation members may work with:

```text
README.md
docs/
```

---

# 15. Frontend Team

## Frontend Leader

John Kevin Aguilera

## Members

* Franz Jowen Rances
* John Benedict Fernandez
* Cielo Seco

The Frontend team is responsible for:

* HTML
* Tailwind CSS
* JavaScript
* Django templates
* Responsive design
* Frontend interactions
* Connecting templates to backend-provided data

---

## Frontend Working Areas

Main folders:

```text
templates/
static/
├── css/
├── js/
├── images/
└── src/
```

Do not randomly create HTML files in the project root.

For example:

```text
templates/catalog/
    product_list.html
    product_detail.html
```

---

## Frontend + Backend Communication

If the frontend needs data that does not exist yet:

Example:

```text
Frontend:
"I need the product name, image, price, category, and stock."
```

Contact the Backend/Database team instead of creating fake database logic yourself.

---

# 16. Backend Team

## Backend Leader

Joshua Barotea

## Members

* Jayvee Garcia
* Rafael Metran
* Dishiela Ingrid Camunag

Backend responsibilities include:

* Django views
* URLs
* Models coordination
* Authentication
* Business logic
* Forms
* Validation
* Cart logic
* Orders
* Favorites
* Backend functionality

Main working areas:

```text
apps/
config/
```

Example:

```text
apps/catalog/
├── admin.py
├── apps.py
├── models.py
├── urls.py
├── views.py
└── ...
```

---

# 17. Database Team

## Database Leader

Edrian Paul Domanico

## Members

* Mark Anthony Llanora
* Stephanie Marie Nanoy

Database responsibilities include:

* Database architecture
* ERD
* Django models
* Relationships
* Migrations
* Data integrity
* Database documentation

Main working areas:

```text
apps/*/models.py
```

Before making major database changes, coordinate with:

* Backend Leader
* Team Leader

---

# 18. Database Migration Rules

If you modify a model:

```python
class Product(models.Model):
    ...
```

run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

Test the project.

Then commit the migration files.

Example:

```text
apps/catalog/migrations/
├── 0001_initial.py
└── 0002_product_add_stock.py
```

Migration files should generally be committed to Git.

---

# 19. Figma Design Team

## Figma Design Leader

Mark Angelo Talento

## Members

* Savannah Mari De Mesa
* Karl Louise Sebuc

The Figma team is responsible for:

* UI design
* UX design
* Page layouts
* Components
* Colors
* Typography
* Responsive layouts
* User flows
* Design consistency

The Figma team should maintain the design system before major frontend implementation begins.

---

# 20. Documentation Team

## Members

* Carl Demandante Chua
* Gabriel Clinton Diaz

Documentation responsibilities include:

* Project documentation
* Technical documentation
* User documentation
* Installation guides
* Screenshots
* Database documentation
* Feature documentation
* Project reports

Main locations:

```text
README.md
docs/
```

---

# 21. Before You Start Working Each Day

Always update your branch first.

First:

```bash
git checkout main
```

Then:

```bash
git pull origin main
```

Return to your branch:

```bash
git checkout your-branch-name
```

Example:

```bash
git checkout frontend/homepage
```

Then update it:

```bash
git merge main
```

Now your branch contains the latest approved changes.

---

# 22. While Working

Save your work regularly.

Check what changed:

```bash
git status
```

You can see which files were modified.

Example:

```text
modified:
    templates/home/index.html

modified:
    static/js/main.js
```

---

# 23. Test Your Work

Before committing:

```bash
python manage.py check
```

If you changed backend functionality:

```bash
python manage.py test
```

Start the server:

```bash
python manage.py runserver
```

Test the feature in the browser.

---

# 24. Add Your Changes

When your feature works:

```bash
git add .
```

Then check:

```bash
git status
```

Make sure you are not accidentally adding:

```text
.env
venv/
node_modules/
db.sqlite3
```

---

# 25. Commit Your Changes

Use descriptive commit messages.

Good:

```bash
git commit -m "feat: create flower product card"
```

```bash
git commit -m "fix: correct cart quantity calculation"
```

```bash
git commit -m "style: improve navbar responsive layout"
```

```bash
git commit -m "docs: update installation guide"
```

Avoid:

```text
final
update
changes
test
asdf
final final
```

---

# 26. Push Your Branch

The first time:

```bash
git push -u origin your-branch-name
```

Example:

```bash
git push -u origin frontend/homepage
```

After the first push:

```bash
git push
```

---

# 27. Create a Pull Request

Go to the GitHub repository.

GitHub should show your recently pushed branch.

Create:

```text
Pull Request
```

Set:

```text
base: main
compare: your-branch-name
```

Example:

```text
frontend/homepage → main
```

---

# 28. Pull Request Description

Explain what you did.

Example:

```markdown
## Summary

Created the initial Antonia's homepage.

## Changes

- Added hero section
- Added featured flowers section
- Added responsive layout
- Added Tailwind styling

## Testing

- Tested Django development server
- Tested desktop layout
- Tested mobile layout
- Ran `python manage.py check`

## Notes

No database changes.
```

---

# 29. Wait for Review

Do NOT immediately merge your own Pull Request.

The appropriate leader should review it.

Examples:

```text
Frontend PR
    ↓
John Kevin reviews

Backend PR
    ↓
Joshua reviews

Database PR
    ↓
Edrian reviews

Figma
    ↓
Mark reviews
```

---

# 30. If the Leader Requests Changes

Do not create another Pull Request.

Continue working on the same branch.

Make the requested changes:

```bash
git add .
git commit -m "fix: address review feedback"
git push
```

The existing Pull Request will automatically update.

---

# 31. After Your Pull Request Is Merged

Once the leader merges your Pull Request:

```text
your branch
     ↓
Pull Request
     ↓
approved
     ↓
main
```

You can safely update your local repository.

```bash
git checkout main
git pull origin main
```

Then start your next task.

---

# 32. Starting Another Task

Do NOT continue using an old completed feature branch for an unrelated task.

Instead:

```bash
git checkout main
git pull origin main
```

Create a new branch:

```bash
git checkout -b frontend/product-details
```

Then work on the new feature.

---

# 33. If You Encounter a Merge Conflict

You may eventually see:

```text
CONFLICT
```

Do not panic.

First contact the appropriate team member/leader if you are unsure.

Never blindly select:

```text
Accept Current
```

or:

```text
Accept Incoming
```

Understand both changes before resolving the conflict.

After resolving:

```bash
git add .
git commit
```

Then continue.

---

# 34. If Something Is Broken After Pulling

First check:

```bash
git status
```

Then:

```bash
python manage.py check
```

If dependencies changed:

```bash
pip install -r requirements.txt
```

If Node dependencies changed:

```bash
npm install
```

If database migrations changed:

```bash
python manage.py migrate
```

---

# 35. Important Files

Do not modify these casually:

```text
config/settings.py
config/urls.py
requirements.txt
package.json
package-lock.json
```

Changes to these files can affect the entire team.

Contact the appropriate leader before making significant changes.

---

# 36. Files You Must Never Push

Never commit:

```text
.env
venv/
node_modules/
db.sqlite3
__pycache__/
```

Also never commit:

```text
passwords
API keys
secret keys
database credentials
personal credentials
```

---

# 37. Team Communication

Before making changes that affect another team, communicate first.

Example:

### Frontend needs a new database field

Contact:

```text
Frontend → Backend → Database
```

### Database changes a model

Inform:

```text
Database → Backend → Frontend
```

### Backend changes an URL

Inform:

```text
Backend → Frontend
```

### Design changes a page

Inform:

```text
Figma → Frontend
```

The goal is to prevent one team from unexpectedly breaking another team's work.

---

# 38. Recommended Team Workflow

The overall development process is:

```text
              MAIN
                │
                ↓
          Pull latest code
                │
                ↓
         Create own branch
                │
                ↓
          Do assigned task
                │
                ↓
             TEST
                │
                ↓
             COMMIT
                │
                ↓
              PUSH
                │
                ↓
        CREATE PULL REQUEST
                │
                ↓
         GitHub Actions CI
                │
                ↓
         Leader Code Review
                │
          ┌─────┴─────┐
          │           │
       Changes      Approved
          │           │
          ↓           ↓
       Push again    MERGE
                      │
                      ↓
                    MAIN
```

---

# 39. Quick Start Cheat Sheet

For most members, the entire setup can be summarized as:

```bash
# Clone
git clone https://github.com/YOUR-USERNAME/Antonia-s-Flower-Bouquet-Commerce.git

# Enter project
cd Antonia-s-Flower-Bouquet-Commerce

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install Node packages
npm install

# Configure .env
# Copy .env.example → .env

# Prepare database
python manage.py migrate

# Check Django
python manage.py check

# Update main
git checkout main
git pull origin main

# Create your branch
git checkout -b frontend/your-feature

# Work...

# Check changes
git status

# Commit
git add .
git commit -m "feat: describe your change"

# Push
git push -u origin frontend/your-feature

# Create Pull Request on GitHub
```

---

# 40. Golden Rules

### Rule 1

**Never work directly on `main`.**

### Rule 2

**Always pull before starting work.**

### Rule 3

**One task = one feature branch.**

### Rule 4

**Test before committing.**

### Rule 5

**Write meaningful commit messages.**

### Rule 6

**Never commit `.env`, `venv`, `node_modules`, or secrets.**

### Rule 7

**Do not merge your own Pull Request.**

### Rule 8

**Communicate before changing another team's files.**

### Rule 9

**Database changes must be communicated to the Database and Backend teams.**

### Rule 10

**If you're unsure, ask the appropriate leader before making structural changes.**

---

# Antonia's Team

## Team Leader

Joshua Barotea

## Figma Design

**Leader:** Mark Angelo Talento

* Savannah Mari De Mesa
* Karl Louise Sebuc

## Front End

**Leader:** John Kevin Aguilera

* Franz Jowen Rances
* John Benedict Fernandez
* Cielo Seco

## Back End

**Leader:** Joshua Barotea

* Jayvee Garcia
* Rafael Metran
* Dishiela Ingrid Camunag

## Database

**Leader:** Edrian Paul Domanico

* Mark Anthony Llanora
* Stephanie Marie Nanoy

## Documentation

* Carl Demandante Chua
* Gabriel Clinton Diaz

---

# Final Workflow

Every member should remember:

```text
CLONE
  ↓
SETUP
  ↓
UPDATE MAIN
  ↓
CREATE BRANCH
  ↓
WORK
  ↓
TEST
  ↓
COMMIT
  ↓
PUSH
  ↓
PULL REQUEST
  ↓
LEADER REVIEW
  ↓
CI CHECK
  ↓
MERGE
  ↓
UPDATE MAIN
  ↓
NEXT TASK
```

This workflow keeps the Antonia's repository organized, prevents accidental changes to `main`, and allows multiple teams to work on the project simultaneously.
