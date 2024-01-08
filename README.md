## Create Virtual Environment
- Below commands were used in terminal to create/activate virtual environment
    - python -m venv env    (create virtual environment)
    - env\Scripts\activate  (activate virtual environment)

## Django Installation
- Below commands were used to install and set up django
    - pip3 install django    (install django)
    - django-admin startproject neupane_driving . (create a project named neupane_driving, dot at the end of the project name ensure that its created at the correct directory)


## Allauth Setup
- Below steps/command used to setup allauth
    - pip3 install django-allauth (install allauth)
    - update installed apps, authentication backend, templates and site_id settings on settings.py (Refer to Allauth DOCS)
    - update urls pattern and import include to urls.py of project level

## .gitignore file
   - type touch .gitignore command on terminal  (crete .gitignore file)
    - add below to .gitignore file
      ```

        *.sqlite3
        * .pyc
        __pycache__

      ```


## Freeze requirements
- pip3 freeze > requirements.txt

## Database Migrations
- python3 manage.py makemigrations --dry-run (check before making migrations)
- python3 manage.py makemigrations (making migrations)
- python3 manage.py migrate --plan    (check before migrate)
- python3 manage.py migrate    (migrate)


## Create templates/folder using CLI 
- mkdir templates (create templates)
- mkdir templates\allauth (create allauth folder inside the templates folder)


#### Copy all allauth templates from django site packages (Command used to copy this did not worked and still unknown on why command was not working therefore file was copied and paste manually : Further research and study needed to fix this issue on why command was not working in the terminal )
- ```
  copy -r  env/Lib/python3.8/site-packages/allauth/templates/*  ./templates/allauth/ 

  below error shown on terminal, 

  C:\Users\sb4_c\OneDrive\Desktop\Neupane-Driving\Driving-School\neupane_driving>copy -r  env/.pip-modules/lib/python3.8/site-packages/allauth/templates/*  ./templates/allauth// 
  The system cannot find the file specified.

  ```
- copy-r  - copy recursively
- dot slash (./) - current directory
- dot dot slash (../) - go one level up from current level
- star (*) - copy everything
- python 3.8 - current version of python (type puthon command on terminal to check the version of python used)
- ./templates/allauth/ at the end means copied everything to allauth folder which is inside the templates folder

### Above issue was then solved by copy and paste manually: 
  - Click on env folder > Lib > site-packages > allauth > then copy the templates folder then paste inside the allauth folder, which is inside the templates folder on project 


## Create App on project 
  - python3 manage.py startapp home (this will create the app name home inside the project)

## Install Django Crispy form
  - ```
    pip3 install django-crispy-forms
    pip3 install crispy-bootstrap4
    ```
  - update below on settings.py
    ```
    INSTALLED_APPS = [
    ...

    'crispy_forms',
    'crispy_bootstrap4',
    ]
    ```

  - Add below on settings.py 
     ```
     CRISPY_TEMPLATE_PACK = 'bootstrap4'
     ```







### Create env file to hide all secret keys :
  - 1. Create ***.env*** file on project level
  - 2. Add all the secrect keys inside .env file
  - 3. Finally include ***.env*** inside ***.gitignore*** , this will ensure that .env file wont push to github and only available in local machine

      - Step 1: Create a .env File
      - Create a file named .env in the root directory of your project. This file will contain your environment variables, including the SECRET_KEY. For example:
      ```SECRET_KEY='mysecretkey#120)ast!value'```, required quotation mark due to special characters

    - Step 2: Load Environment Variables in settings.py
      - In the Python script where you need to access environment variables, load the variables from the .env file as below:
      ```
        import os
       
        # Access the SECRET_KEY
        SECRET_KEY = os.getenv('SECRET_KEY')

        # Now you can use SECRET_KEY in your application
      ```


  #### Run below command if ***.env*** file still showing in github once commit and push after adding to ***.gitignore***
    - git rm -r --cached .env
    - then git add , commit and push as usual and check on github , ***.env*** file should not be there

## Unresolved Issues

  - Unable to display sold out button on the product details page if stock quantity is 0 or below ....
    - as a temporary solution, error message will be displayed once entered quantity exceed the stock quantity
  - For Some reason image product image directly added while adding the products from admin pannel are not showing in the page 
    - as a temporary solution first product will be added with image, size, color and stock and then save, after then select Product images option on admin and select the Variation to match the product variation and then save , this will ensure that all images will display correctly 
    - NOTE : if multiple images for the product then first image of the product will be added to basket and checkout success 
  - Sort by A-Z and Z-A not working : NOT FIXED YET

## Issues and resolution

### Issue with virtual env set up, 
    ```
    'virtualenv' is not recognized as an internal or external command,
    operable program or batch file.
    ```

- Thanks to youtube video [https://www.youtube.com/watch?v=oL6pwOK253I], this helped me to understand the concept and fixed the problem

- Thanks to youtube video [https://www.youtube.com/watch?v=eJdfsrvnhTE], this helped to setup django on VScode

### Error on terminal while using touch command to create .gitignore  (touch .gitignore)

- command below used to install touch
 - npm install touch-cli -g

### image was not displaying when <img class="card-img-top img-fluid" src="{{ MEDIA_URL }}no-image.jpg"/>
 - below line of code was needed to add inside the context processor of django setting :
    - ```
        'django.template.context_processors.media',
        
      ```

### Issue with understanding in JS DOM manipulation in order to select the child element 
  - Thanks to youtube video of [WebMasterCampus](https://www.youtube.com/watch?v=g6DB3boXtFY), this video helped me to understand and refresh my knowledge, I was able to solve this issue after watching this video

### Unable to login to django admin server
  ```
    update allowed host in django setting from ALLOWED_HOSTS = [] to ALLOWED_HOSTS = ['*'], this solved an issue
  
  ```

### Issue during Render Deployment:
 - 1. Below error was shown on deploy logs :
    - ***django.core.exceptions.ImproperlyConfigured: allauth.account.middleware.AccountMiddleware must be added to settings.MIDDLEWARE***
    - below line of code was added on MIDDLERWARE on django settings to fix this issue:
        ```
        MIDDLEWARE = [
            # Rest of the codes...
        
            'allauth.account.middleware.AccountMiddleware',
            # Rest of the codes
            ]
        ```

 - 2. Another error as below once above error fixed:
    - ***botocore.exceptions.ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden***
    - thi issue was related to AWS setup however upon checking on AWS S3 buckets all secret keys no issue identified, I then delete all Environment Variables from Render Setting and add them again which fixed proble.

 - 3. Another issue related to user accout as Rendor deployment failed and erro message was printed "no auth_user found"
    - This was issue related to database migration which should have been solved by running command , python3 manage.py migrate however it didnt fixed the problem
    - Issue was caused by late migration as databse was setup and django, allauth were installed however no migration was created and migration was only created late after adding few other apps to project such as home, profile, checkout etc which was causing problem, I then open the migration file and tried to correct inside the migration file which then resulted profile app and other apps migrated before allauth , it means when I had to correct the migration file and migrate them in correct order which was not easy to fix. therefore I created new project and moved all the codes and start over again


### The correct way to use the data attribute in both HTML and JavaScript is to maintain the same naming convention. If you use data-max-stock in HTML, you should use .data('max-stock') in JavaScript.

### Issue on payment page as input section to enter card details was not showing once I setup strip payment
  - This issue was fixed by renaming the file name : 
    - I had javascript file on checkout app for stripe and file name was ***stripe_element.js*** for some reason this was causing an error, I then changed filename to ***stripe.js*** which then solved the problem above


### Issue with image not displaying in product page:
  ```
  BEFORE

    {% if woman.images.all %}
      <a href="{% url 'product_details' woman.id %}">
          <img class="card-img-top img-fluid" src="{{ woman.images.first.image.url }}" alt="{{ woman.product_name }}">
          <!-- if 2nd image needed then use :  {{ woman.images.all.1.image.url }}-->
      </a>
    {% else %}
    <a href="{% url 'product_details' woman.id %}">
        <img class="card-img-top no-image img-fluid" src="{{ MEDIA_URL }}no-image.jpg" alt="{{ woman.product_name }}">
    </a>
  {% endif %}

  ```


  ```
  AFTER

      {% if woman.product_images.all %}
        <a href="{% url 'product_details' woman.id %}">
            <img class="card-img-top img-fluid" src="{{ woman.product_images.first.image.url }}" alt="{{ woman.product_name }}">
            <!-- if 2nd image needed then use :  {{ woman.images.all.1.image.url }}-->
        </a>
      {% else %}
        <a href="{% url 'product_details' woman.id %}">
            <img class="card-img-top no-image img-fluid" src="{{ MEDIA_URL }}no-image.jpg" alt="{{ woman.product_name }}">
        </a>
      {% endif %} 


    NOTE: If your ProductImage model has a related_name specified, as in related_name="product_images", then you should indeed use that related name to access the images associated with a WomanProduct instance.


    NOTE: If you don't have a specific related_name set for the ProductImage model, you can still access the related images using the default reverse relation. By default, Django would use the lowercase name of the related model followed by "_set" as the reverse relation.

    Here's how you can modify your template to access the images without a related_name:

    ```
      {% if woman.productimage_set.all %}
        <img src="{{ woman.productimage_set.first.image.url }}" alt="{{ woman.product_name }}">
      {% else %}
          <img src="{{ MEDIA_URL }}no-image.jpg" alt="{{ woman.product_name }}">
      {% endif %}
    

    NOTE: woman.productimage_set.all retrieves all related ProductImage instances associated with the WomanProduct. woman.productimage_set.first.image.url accesses the URL of the first image associated with the WomanProduct. Please note that productimage_set is the default reverse relation, and the lowercase name of the ProductImage model is used with "_set" appended. If you have changed the related_name or used a different convention, adjust it accordingly.
    
    ```
  ```

### Django error as below on basket view while dealing with error message display login on product quantity :
  - Exception Type:	NoReverseMatch
  - Exception Value: Reverse for 'product_details' with no arguments not found. 1 pattern(s) tried: ['product/(?P product_id>[0-9]+)/\\Z']

    ```
    Before 
      # all other codes ....
      else:
        messages.error(request, f"Sorry, we only have only {variation.stock_quantity} stock for {product.product_name} with the selected size and color, please ammend the quantity or choose another variation")
        return redirect(reverse('product_details'))

    After, (issue solved)

      # all other codes....
      else:
        messages.error(request, f"Sorry, we only have only {variation.stock_quantity} stock for {product.product_name} with the selected size and color, please ammend the quantity or choose another variation")
        return redirect(reverse('product_details', args=[product_id]))

    ```

### Error during Render Deloyment as Render was asking to upgrade postgres as current version was not compatible with the version of djnago used:
  - I have fixed this by updating django installed as upon research i found that , Django versions within the 3.2 to 3.3 are designed to work with a range of compatible database versions, and they often maintain compatibility with minor updates to those databases therefore i choose django 3.2 on my project which fixed an issue
  ```
    pip install Django==3.2.* 

    Note : This command installs the latest patch version of Django 3.2. The asterisk (*) ensures that you get the latest patch version within the Django 3.2 series.
  ```

### Payment error while completing the payment after adding more than 3 indivisual product on basket, however no issue if product limit to 3 only, tried more quantity with same product but no issue and issue occur when more than 3 different products :
 - Django was pointing error on cache_checkout_data view which the fixed by updating below line of code:
    ```
    Before,
     "basket": json.dumps(request.session.get("basket", {}))


     After, 
      "basket": json.dumps(request.session.get("basket", {}))[:500]
    ```
    - 'json.dumps(...): This converts the Python object (in this case, the "basket" data) into a JSON-formatted string. This is necessary because Stripe's metadata fields often expect data in JSON format.
    - [:500]: This slices the resulting JSON string to include only the first 500 characters. The purpose of this is to limit the length of the serialized JSON data.

    - Putting it all together, this line of code retrieves the "basket" data from the session, converts it to a JSON string, and then truncates the string to a maximum length of 500 characters. This truncated JSON string is then used as the value for the "basket" key in the metadata of a Stripe PaymentIntent.

    - ***IMPORTANT*** : ***As of January 2022, Stripe has limitations on the size of metadata associated with a PaymentIntent. According to Stripe's documentation, metadata must be a dictionary where each key and value is a string with a maximum length of 500 characters.***

    ***If you attempt to store a JSON string representing 1000 products in the metadata field, the total length of the string is likely to exceed the allowed limit. This can result in a Stripe API error similar to what you've encountered.***

    ***To handle a large number of products, consider alternative strategies, such as:***

      ***Use External Storage:***

       - Store the basket data in an external database or storage system, and only store a reference or key in the metadata. Retrieve the complete data when needed.

      ***Batch Processing:***

       - If possible, process the products in batches rather than sending all 1000 products in a single request. This could involve dividing the products into smaller groups and processing them sequentially.
      
      ***Dynamic Loading:***

       - Load the basket data dynamically when needed, instead of storing it in the PaymentIntent metadata. Retrieve the data when processing the payment.

      ***Limit the Number of Products:***

       - Depending on your use case, consider whether it's necessary to include all 1000 products in the metadata. If not, limit the number of products based on what is essential for the payment process.

    
### Django error message related to profile urls.py as below:
  ```
    The current path, accounts/profile/, didn’t match any of these.
  ```

  - Issue was related to profile and project level url :

    ```
      Before,
        urls.py file (on profile app)

        urlpatterns = [
        path('', views.profile, name='profile'),
        path('order_history/<order_number>', views.order_history, name='order_history'),
        ]

        urls.py file (on project level url)

        urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path('', include('home.urls')),
        path('product/', include('product.urls')),
        path('basket/', include('basket.urls')),
        path('checkout/', include('checkout.urls')),
        path('accounts/', include('profiles.urls')),
    ] 



      After, 
        urls.py file (on profile app)

        urlpatterns = [
        path('profile/', views.profile, name='profile'), # change on this line
        path('order_history/<order_number>', views.order_history, name='order_history'),
        ]

        urls.py file (on project level url)

        urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path('', include('home.urls')),
        path('product/', include('product.urls')),
        path('basket/', include('basket.urls')),
        path('checkout/', include('checkout.urls')),
        path('accounts/', include('profiles.urls')), # Change on this line
    ] 


    NOTE: When you use include('some_app.urls'), it effectively appends the specified app's URL patterns to the current namespace. In your case, the allauth.urls include is set up to handle authentication-related URLs, and it uses the namespace accounts:

    This means that all authentication-related URLs, including login, logout, password reset, etc., will be prefixed with /accounts/. It's a common convention to use a consistent prefix for authentication-related URLs, and accounts/ is a typical choice.

    Now, when you include your profiles.urls, you want to keep the consistency, especially if your profiles app is handling user profile-related views. Therefore, you include it under the accounts namespace as well:

    This approach makes it clear and organized. It groups authentication-related URLs under /accounts/ and user profile-related URLs also under /accounts/, keeping a logical structure.
    
    ```

### Issue during login/signup setup as verification message did not showed up on screen and no activation link seen on console to verify user after signing up:
  - Below settings were needed on django settings to fix this issue :
    ```
      # Email setting

      EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
      
      ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
      ACCOUNT_EMAIL_REQUIRED = True
      ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
      ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
      ACCOUNT_USERNAME_MIN_LENGTH = 4
      LOGIN_URL = '/accounts/login/'
      LOGIN_REDIRECT_URL = '/'
      ACCOUNT_CONFIRM_EMAIL_ON_GET = True
      ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

    ```

## STRIPE INSTALLATION :
- I have used scoop to install stripe on VScode using [Stripe Doc](https://stripe.com/docs/stripe-cli#install)
  - Below steps were taken
   - Run below command on Command prompt/ Powershell or terminal
    ```scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git```

    ```scoop install stripe```

    ```stripe login```

  - It should install stripe by now
   - Run below command on Command prompt/ Powershell or terminal to check 
    ```stripe```

## Project Deployment to RENDER:
  
  - Create a database
    1. Login to [ElephantSQL](https://www.elephantsql.com/)
    2. Click on Create New Instance
    3. Set up your plan
      - Give your plan a Name (this is commonly the name of the project)
      - Select the Tiny Turtle (Free) plan
      - You can leave the Tags field blank
    4. Select “Select Region”
    5. Select a data center near you
    6. Then click “Review”
    7. Check your details are correct and then click “Create instance”
    8. Return to the ElephantSQL dashboard and click on the database instance name for this project
    9. you will then see your database ull for this instance
    

  - Render Preparation :
    1. Install, gunicorn, psycopg2-binary, dj_database_url
      ```
      pip3 install gunicorn
      pip3 install psycopg2-binary
      pip3 install dj_database_url
      ```
    2. import dj_database_url in settings.py
      ```
      import dj_database_url
      ```

    3. Freeze requirements.txt 
    
      ```
      pip3 freeze > requirements.txt
      ```
    4. create build.sh file inside the project/same level as manage.py file and add below inside the build.sh

      ```
      build.sh

      set -o errexit
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py makemigrations && python manage.py migrate

      ```

    5. In your settings.py file add the following code below the declaration of your ALLOWED_HOSTS variable

      ```
      # Add Render.com URL to allowed hosts
      RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
      if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

      ```
    6. Unlike Heroku, Render does not require a Procfile - so Add, commit and push your changes to GitHub.

    7. Preparation for static file :
      - Below settings required on settings.py to ensure static files are loaded on deployed site
           ```
            STATIC_URL = '/static/'
            STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
            STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

            MEDIA_URL = 'media/'
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            ```
      
      - Add below on project level urls.py
        ```
          urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
          urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        ```

      - Run below command on terminal 
        ```
          python3 manage.py collectstatic
        ```

      - git status, git add and git commit now

  - Web Service Creation on Render:

    1. Navigate to Render.com and log in
    2. Click “New +”
    3. Click “Web Service”
    4. Search for relevant repo and click “Connect”
    5. Setting :
      - A brief explanation of each setting is given below.
        *  Add a Name
        * Ensure the following settings match
            - Setting Name =	Value
            - Root Directory = blank
            - Environment	 = Python 3
            - Region	= Frankfurt (EU Central)
              - For those outside of Europe, a more localized region may be preferred.
            - Branch	main

        * Set the Build Command = ./build.sh
          - Using ./ before a file name in the command line is a common way to execute the file.
        
        * Set the Start Command
          -  gunicorn <PROJECT_NAME>.wsgi:application

        * Ensure the Free plan $0/month is selected or any other paid plan is selected

        * Update Environment Variable:
          - PYTHON_VERSION = 3.10.11 (CHeck your own version)
          - DATABASE_URL = click on the instance created on ElephentSQL dashboard and copy URL
          - WEB_CONCURRENCY = 4
          - add other variables as per requirements

        * Access to env.py
          - If you used an env.py file to store your environment variables, and have access to it, please follow the steps below:
            - Scroll down and click “Advanced”
            - Click “Add Environment Variable”
            - Copy the content of your existing env.py file
            - Paste in the copied text to the File contents text area input and ensure the Filename is env.py

    6. Click “Create Web Service”
    7. Wait for deployment…
    8. Deployment completed!


  ## Manage Staticfiles on deployed site:
  - Below link has all the steps that required manage staticfiles on Render deployment, also when DEBUG set to false then static files were not serving on deployed site which was also fixed with the help of below link.
  - [https://render.com/docs/deploy-django#static-files](Getting Started with Django on Render)
    - Note : you might see below command for installation : **poetry add 'whitenoise[brotli]'** simply use **pip3 install whitenoise**

  ## Create Django Superuser for deployed site 
    1. Log in to the Render dashboard: Open your web browser and navigate to https://dashboard.render.com. Sign in with your Render account credentials.
    2. Select your app: From the Render dashboard, locate and click on the name of your Django app.
    3. Go to the Shell tab: Within the app's details page, find and click on the "Shell" tab. This will open a terminal-like interface where you can run commands.
    4. Run the createsuperuser command: In the Shell tab, enter the following command to create a superuser:
      ```
        python manage.py createsuperuser
      ```


## Amazon Web Service
  - AWS was used in this project to host static and media files for this project.
  - AWS account was creating by completing the sign-up process through the [AWS website](https://aws.amazon.com/).

  1. Create the bucket
    - Below steps were taken to create the bucket
        - Create a new bucket on the AWS S3 service
        - From the main dashboard search for S3 and then select get started option
        - Select Create bucket button and give the bucket name and select your region
        - Uncheck the block public access and acknowledge that the bucket will now be public
        -  Select create bucket.
  
  2. Bucket settings.
   - Select bucket properties settings and turn on static website hosting
   - Add index.html (or home.html, whichever appropriate) to index field and  and error.html to the error and save.

   - Select bucket Permissions settings now, click on the Cross-origin resource sharing (CORS),edit and add below config :
       ```
       [
          {
              "AllowedHeaders": [
                  "Authorization"
              ],
              "AllowedMethods": [
                  "GET"
              ],
              "AllowedOrigins": [
                  "*"
              ],
              "ExposeHeaders": []
          }
       ]

       ```
    - On the bucket policy option, click on generate policy and Select S3 bucket policy
    - Add * to the principal field to select all principals (if * not added)
    - Choose the action to get object.
    - Paste in your ARN which is available on the previous page. (bucket name > permission > bucket policy > edit edit bucket policy > then copy ARN )
    - Click, add statement
    - Then click, generate policy.
    - Now copy and paste your new policy into the bucket policy.
    - Add /* at the end of "Resourse object if not present to allow access to all resources in this bucket
      ```
      it should looks like below : 

      {
         "Version": "2012-10-17",
         "Id": "Policy1635692466356",
         "Statement": [
            {
                  "Sid": "Stmt1635692462924",
                  "Effect": "Allow",
                  "Principal": "*",
                  "Action": [
                     "s3:GetObject",
                     "s3:PutObject",
                     "s3:DeleteObject"
                  ],
                  "Resource": "arn:aws:s3:::neupane-kitchen/*"
            }
         ]
      }

      ```
    - Click on your bucket > permissions > Edit access control list (ACL) > find Everyone (public access) option and check list

  3. Create a User

   - Back in the AWS main dashboard search for IAM and follow the process below : 
    - Firstly create a group to put user in.
    - Click create a new group and name it.
    - Click through to the end and save the group.
    - Create a policy.
    - In our group click, policy and then, create policy.
    - Select the JSON tab and then import managed policies from Action tab next to Json tab.
    - Search for S3 and select AmazonS3FullAccess and import.
    - In the resources section paste in our ARN from before.
      - use 2 ARN as below in Resource section  :
        ```
        "Resource": [
          "arn:aws:s3:::neupane-driving",
          "arn:aws:s3:::neupane-driving/*"
        ]

        first line is the bucket itself and second rule for all files/folders in the bucket
        ```

    - click through to review the policy.
    - Fill in name and description and then click generate policy.
    - Back in your group click the group just created > permissions > Click Add permissions tab > Select attach policy option .
    - you will now see option, Entities attached section next to permission tab
    - Click attach policy and search for policy you have just created and click attaach policy
    
    - Select Users from the sidebar and then click, add user.
    - Create a user name and select programmatic access then click next.
    - Then select your group to add your user to.
    - Click through to the end and then click create user.
    - download the CVS file and save it as it contains the users keys

    (note: CVS file must be download and keep it safe/secret at this stage as after this process its not possible to download CVS file again)

  4. Connecting to Django
    - Once AWS has been set up now this needs to be connect to Django. Steps below were taken to accomplish this.
    - Head up to the gitpod terminal and use below command to install ***boto3 and django storages*** packages

      ```
       pip3 install boto3
       pip3 install django-storages
      ``` 

    
   - Then freeze the requirements by using below command in the terminal
       ```
       pip3 freeze > requirements.txt
       ```
   - Back to the settings.py add some settings as below:
   - first add storages into installed apps in settings.py
   - Back to Render setting create an environmental variable "USE_AWS" and set it to True in order only run this code when on Render.
   - Now add below settings to the settings.py
    
      ```
        if "USE_AWS" in os.environ:

            # Bucket Config

            AWS_STORAGE_BUCKET_NAME = '<bucket name>'
            AWS_S3_REGION_NAME = '<your region>'
            AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
            AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

            # static and media file storage
            
            STATICFILES_STORAGE = 'custom_storages.StaticStorage'
            STATICFILES_LOCATION = 'static'
            DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
            MEDIAFILES_LOCATION = 'media'

            # Override static and media URLs in production

            STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
            MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

      ```

  - Create a custom_storages.py file on workspace to tell Django that in production we want to use s3 to store our static and media files.
  - import S3Boto3Storage to the top of the custom_storages.py file
  - Create new classes inside the custom_storages.py file and add location variable as below.


    ``` 
      from django.conf import settings
      from storages.backends.s3boto3 import S3Boto3Storage

  
      class StaticStorage(S3Boto3Storage):
      location = settings.STATICFILES_LOCATION

      class MediaStorage(S3Boto3Storage):
      location = settings.MEDIAFILES_LOCATION
    ```

5. To obtain the values for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY while deploying to Render, you can follow these steps:

  - Log in to the AWS Management Console.

  - Open the IAM (Identity and Access Management) service.

  - In the left navigation pane, click on "Users."

  - Select the IAM user that you want to generate the access key for, or create a new IAM user if needed.

  - Open the "Security credentials" tab for the selected user.

  - Scroll down to the "Access keys" section and click on the "Create access key" button.

  - A dialog box will appear displaying the access key ID and secret access key. Copy these values or click on the "Download .csv file" button to download a CSV file containing the access key details.

  - Note: It is important to copy the secret access key because it will not be visible in the console after closing the dialog box. If you lose the secret access key, you'll need to create a new access key.


- All setup process has now completed.

6. Add media to AWS.
   - Below steps were taken to add the media to AWS
   - Head back to AWS s3 and create a new folder called media.
   - Select upload and add image files.
   - Then select to grant public access.
   - And then upload the files.

## Sending Real Email from deployed site
   - Gmail setup
    1. Login to Gmail and go to setting
    2. Settings > Accounts & Imports > Other Google Accounts
    3. Go to Security tab under signing into google and click GET STARTED
    4. Google may ask you to enter your password, once password entered then select verification method (Text or call to receive code)
    5. Turn on 2 step verification
    5. You will now see App password option, on this screen you will see Select app and Select device option
    6. Select Mail under app and select other under device option and type Django or anything you prefer
    7. Click Generate, you will then see 16 digit password which is your EMAIL_HOST_PASSWORD

  - Email settings in django settings
    - add below code :

    ```
    if 'DEVELOPMENT' in os.environ:
      DEFAULT_FROM_EMAIL = 'neupanedrivingschool@example.com'
      EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    else:
      EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      EMAIL_USE_TLS = True
      EMAIL_PORT = 587
      EMAIL_HOST = 'smtp.gmail.com'
      EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
      EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
      DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    ```
  - Add below to the Environment variable in Render:
    ```
      EMAIL_HOST_USER = email address that was used to get 16 digit password
      EMAIL_HOST_PASSWORD = 16 digit password from above
    ```

  - How to server static files on django server during production (local server):
    - Inorder to serve staticfiles on local server make sure **DEBUG = True** on settings.py, if Debug value is set to False then static file wont serve hence no css and javascript effect.


## Add domain to deployed site
  - Inorder to connect site with custom domain buy your domain name from [Godaddy](https://account.godaddy.com/) or any other platform

  - ***Render Setup***
    - Go to settings of your deployed and under General tab choose Change Instance type and select one of the paid instance as free stance wont work provide SSL certificate that required for DNS setup
    - Under Custom domain tab select Add custom Domain and enter the nomain name purchased from GoDaddy (www.neupanedrivingschool.com)
    - It will then display [Two domain name](media/domain.jpg), one start with wwww and another without www (In my case, it was www.neupanedrivingschool.co.uk and neupanedrivingschool.co.uk)
    - Domain with www will show url (neupane-driving.onrender.co.uk) and domain without www will show IP address (216.24.57.1), both of these needed on GoDaddy DNS setting
  - ***GoDaddy setup***
    - Login to GoDaddy and choose the domain you have purchased and select DNS
    - Under DNS management Tab Choose CNAME (or Select Add New Record and manually)and add below (edit/pupdate as necessary as some of the details will be there already)

    - ```
        Type = CNAME
        Name = www
        Value = url from domain setting page of Render (url with www)(neupane-driving.onrender.co.uk)
        TTL = default/1.5hr or any others
      ```

    - Under DNS management Tab Choose A (or Select Add New Record and manually)and add below (edit/pupdate as necessary as some of the details will be there already)
      - ```
        Type = A
        Name = @
        Value = IP address from domain setting page of Render
        TTL = choose one 
        Seconds = 600 or select one 
        ```

    - Now click Save

    - Back to Custom domain setting screen of Render, Click "Verify" on both domain name
    - Render will now automatically issue SSL certificate verified

    - All process now completed and app is now connceted with domain name




 


