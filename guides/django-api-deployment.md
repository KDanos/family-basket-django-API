![GA](https://cloud.githubusercontent.com/assets/40461/8183776/469f976e-1432-11e5-8199-6ac91363302b.png)

# Deployment of Django app on Heroku

## Install the Heroku CLI

- Install the Heroku Command Line Tools with Homebrew `brew tap heroku/brew && brew install heroku`

- If you have issues using Homebrew (likely because you're on Linux/Windows) [follow the recommended install pathway for your system](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)

- As a last resort, if all else has failed, you can use the NPM version of the CLI, by running `npm install -g heroku` as per the guide.
<br><br>

## Deploying a Django/React App to Heroku

#### Ensure you merge your latest code to the main branch. Heroku always uses the main branch regardless of which branch you're in when deployment commands are run.

* Ensure you've created your Heroku account before continuing on. You should also check your account/billing page on the Heroku website, which should show a number of free credits. If it says $0, let us know.
* You should have been committing to Git throughout this process, however if you have not for any reason, and your directory is not a git repo, then run `git init` and commit your changes.

### Set Up Heroku App

Run the following commands from the project root

* `heroku login`  - This will log you into the Heroku command line tools

* `heroku create --region=eu project-name` - replace `project-name` with a name of your choosing, Heroku will let you know if it is currently available (custom domains can be configured later from the Heroku dashboard, if you wish). 

* Remember this project name, it will be the project name in every subsequent terminal command using the `--app` flag.

On completion you will see two links in the terminal:
1. the deployment URL (usually in blue)
2. Git URL (usually in green)

### Handling the DEBUG setting
In the settings.py file, there's currently the following setting:
```python
DEBUG = True
```

This line of code tells Django whether or not we're in development or production. When set to `True`, Django invokes development mode, which outputs all of the errors directly to the screen. It also shows an index page at the route which we don't want in production. We need to handle this so that DEBUG is set to `True` in development and `False` in production.

We'll start by adding the following environment variable to heroku. Run the following in the terminal:

```bash
heroku config:set DEBUG=False
```

We will then use this variable to set the `DEBUG` setting to `True` or `False` in each relevant environment. In your `settings.py` file, update DEBUG to the below:
```python
DEBUG = env.bool('DEBUG', default=False)
```

This line is slightly different to other uses of environment variables. Environment variables are loaded as a string, but in Python this needs to explicitly be a boolean type, and this `env.bool()` method does the conversion for us. Additionally, the `default=False` means that if we forget to add the environment variable in production, it will default to production mode anyway.

In your local `.env` file, you can set this variable to "development" to enable DEBUG mode:
```bash
DEBUG=True
```

### Other settings

*Note: The following will replace any existing `CORS_ALLOWED_ORIGINS` setting. Ensure you don't have duplicates.*

Again, we'll start this section by adding some environment variables to heroku.

First, run the following command to get your backend URL. It will display under "Web URL":
```bash
heroku info
```

Then, run the following to add the necessary environment variables to your Heroku instance, replacing `deployed_url` with your Netlify URL for the frontend and your Heroku URL (the one we found above) for the backend.

*Important: Ensure you remove trailing slashes from both domains otherwise it will fail!*

```bash
heroku config:set DEPLOYED_FRONTEND_URL=deployed_url
```

Then:
```bash
heroku config:set DEPLOYED_BACKEND_URL=deployed_url
```

Next, in `settings.py`, above `INSTALLED_APPS` but after `DEBUG`, add the following:

*Note: For ALLOWED_HOSTS, we don't need the protocol (`http://`) as shown below - if you've added it, remove it. Both other settings SHOULD include the protocol. When your front-end is deployed, add this to the CORS_ALLOWED_ORIGINS & CSRF_TRUSTED_ORIGINS lists.*:

```python
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # local frontend urls without protocols

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173", # Local frontend url
    ]

    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000", # Local backend url
        "http://localhost:8000" # localhost for good measure
    ]

else:
    ALLOWED_HOSTS = [env('DEPLOYED_BACKEND_URL').replace('https://', '')] # removes protocol (https://)

    CORS_ALLOWED_ORIGINS = [
        env('DEPLOYED_FRONTEND_URL'), # Deployed frontend url only
    ]

    CSRF_TRUSTED_ORIGINS = [
        env('DEPLOYED_BACKEND_URL'), # Deployed backend url only
    ]
```

A brief description of those settings:

`ALLOWED_HOSTS` – Defines a list of hostnames (domains or IP addresses) that the Django app can serve. Prevents HTTP Host header attacks.

`CORS_ALLOWED_ORIGINS` – Specifies which origins (domains) are allowed to make cross-origin requests to the Django app. Used for handling Cross-Origin Resource Sharing (CORS).

`CSRF_TRUSTED_ORIGINS` – Lists external domains that are allowed to send cross-site requests with CSRF protection enabled, useful for APIs and third-party integrations.


### Tell Heroku to use Python
Run the following in the terminal, which ensures python is installed during the build process:

* `heroku buildpacks:add heroku/python`

* If you get an error here that says "Missing required flag app", then you need to add `--app project-name` to the end of the command, changing `project-name` to the project name you selected when creating your Heroku app above. This `--app` flag will likely need to be added to every request starting with `heroku` throughout this guide.

### Environment Variables

- Heroku doesn't have your .env file so we need to manually add each variable declared in your backend .env file to Heroku (no VITE variables needed here). Remember, these should be your production variables (explained further below).

- For each variable (one by one), run the following, switching `SECRET_KEY` for the variable name and `'your secret goes here'` for the value. I recommend using single quotes around each value as special characters will break the command. For example, for your SECRET_KEY:
```bash
heroku config:set SECRET_KEY='your secret goes here'
```

As mentioned, these should be your production variables so don't forget the following:

`DEBUG` - this should be set to False in production:
```bash
heroku config:set DEBUG=False
```

One by one, repeat the above for every environment variable you have set in your .env file. For example, you likely have at least; `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`. If you used the `django-cloudinary-storage` package - don't forget to include your cloudinary variables!

### Configuring static files with WhiteNoise
When we're in production, Heroku will store any static files (like images we've uploaded to our own file system using Django and all of Django's admin system CSS) in a single dedicated folder. As this is only necessary in production, we will ensure that when `DEBUG = False` we have the necessary config to allow it to do so. In your settings.py file, at the very top of the file, import the `os` package:
```python
import os
```

Then, find the `STATIC_URL` setting (usually towards the bottom) and replace it with the following. If you don't have one then just add this anywhere towards the bottom of the file:

```python
# This is the URL where the assets can be publicly accessed
STATIC_URL = '/static/'

# Tell Django the absolute path to store those assets - call the folder `staticfiles`
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# This production code might break development mode, so we check whether we're in DEBUG mode before setting the STATICFILES_STORAGE
if not DEBUG:
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Above, you can see that we're using [whitenoise](https://pypi.org/project/whitenoise/) to handle file storage. To configure it properly, we need to do 2 more things:

1. Install it: `pipenv install whitenoise`
2. Add the whitenoise middleware. Ensure the middleware is in the following order:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # New line, add this.
    # all other middleware
]
```

That's it for our settings.py file.

### Tell Django how to start your application

* Install Gunicorn (production-ready server): `pipenv install gunicorn`

* In the root of your project, create a new file called “Procfile”: `touch Procfile`

* THE FOLLOWING IS NOT A TERMINAL COMMAND. Add the below code into the `Procfile` file - don't forget to save it:

```
web: gunicorn project.wsgi
```

This line simply tells Heroku what to do to start your server. 

*IMPORTANT* If you have changed the name of your project folder, then replace the word `project` in the above command, to your folder name. For example:
```
web: gunicorn myprojectfolder:wsgi
```

## Pre-deployment checks

1. Ensure these new changes are committed and pushed to the main branch on Github. If you made these changes from a feature branch, now is time to commit and push them before merging them into main, either via a pull request or a local merge.

2. At this point, double check that all of your environment variables have been set correctly by running the command `heroku config` which will output all existing variables to the terminal. If any are missing or incorrect, be sure to fix them or reach out if you encounter any issues.

## Deployment

Heroku uses github for deployment. Run the following line to deploy your app:
```bash
git push heroku main
```

If the build fails at this point, the log in the terminal should point to the issue. Attempt to resolve any issues yourself before reaching out to us.

If you need to redeploy because of errors, once you have made your changes, run `git push heroku main` again. If it says "Already up to date", then you may need to add or remove a comment somewhere in your code so that git recognises a change - this will then allow you to add, commit and push to heroku to enact the changes.

### Removing the default Heroku Postgres provision

Once the deployment seems to have gone successfully and no build failures occur, we need to do some cleaning up. Heroku sometimes provisions a Postgres database on first deployment if the database settings point to a postgresql engine. We don't need it and it costs credits, so we'll remove it.

First, we'll check if we have it. Run the following in the terminal:
```bash
heroku addons
```

If you see a message saying "No add-ons for app appname." then skip to the "Finishing up / Redeploying" section.

If you see a list of addons, and "heroku-postgresql" is present, then run the following to destroy the unnecessary postgresql provision:
```bash
heroku addons:destroy heroku-postgresql
```

It will ask you to type the name of your app to confirm deletion; type it and hit enter.

You can double check this worked by running `heroku addons` again, which should now output a message like "No add-ons for app appname."

## Finishing up / Redeploying

### Seeding

If everything is looking okay, next step is to migrate and seed your database.

First, migrate your models to your production database:
```bash
heroku run python manage.py migrate
```

Then load in each seeds file one by one. The below example loads a seeds file inside of an app called "users". *Note: Order is important due to relationships - if you have any issues loading your data, let us know*:
```bash
heroku run python manage.py loaddata users/seeds.json
```

### Testing

Test your deployment by opening your production deploy with `heroku open` which will open your API in the browser. You should see a `Not Found` page as there is no endpoint on the root path. Most of the other routes aren't likely to work here either due to authentication, but a good litmus test to check that things are working is to go to `/admin` on your production site and sign in.

If you can sign in successfully with an existing user, you can now get testing the other routes in Postman!

### Errors and redeploying

#### Application Error
If you get an application error when navigating to the site, in the terminal, run `heroku logs --tail`. This will show you any errors that have occurred. Common issues are missing modules, missing variables etc. Try and solve any errors you find yourself, but reach out if you hit a dead-end.

#### 503 Error
This one might be more difficult to decipher as it largely comes with a more substantial error log, but the status code of any error in the log is usually highlighted in red. If you see a status code of `503` - then run the below:
```
heroku ps
```
If you see a message that says "No dynos on ..." then run the below:
```
heroku ps:scale web=1
```
This will start a web dyno which is responsible for running your web process in Procfile.

#### Errors Solved - Redploying
If the errors seem to have been fixed, redeployment is as simple as pushing to your heroku github repo:
```bash
git push heroku main
```
Of course, this process begins again should a new error occur, so start back with `heroku logs --tail`