# CSE 330 Creative Project 
  - [Contributor:](#contributor)
  - [Documentation:](#documentation)
    - [How to run the project?](#how-to-run-the-project)
    - [Functions:](#functions)
    - [Environment:](#environment)

## Contributor:

Jiajun Sun-502363-[ShawnsFantasticWorld](https://github.com/ShawnsFantasticWorld)

Xianchun Zeng-502315-[xianChunZ](https://github.com/xianChunZ)

## Documentation:

### How to run the project?



- Configure database information and migrate in setting.py in Q_bearAdmin. 

  - Specific steps are as follows:

  - The database configuration is located in the Q_bear\Q_bearAdmin\Q_bearAdmin\settings.py file, the specific code is as follows (the encoding method of the database is UTF-8):

    ```mysql
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dbname',
            'USER': 'username',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    ```

  - Execute the python manage.py makemigrations and python manage.py migrate commands in sequence in the Q_bear\Q_bearAdmin directory to migrate the database. If the migration is unsuccessful, you can create a migrations directory under the Q_bear\Q_bearAdmin\myAdmin directory, and then create an empty file named init.py in the migrations directory.

- Enter the Q_bear directory, open the cmd console in the current directory, first use 'npm install' to install dependencies, and enter 'npm run dev' to start the front-end project.

- Enter the Q_bearAdmin directory, open the cmd console in the current directory. First active venv environment by using 'ssource venv/bin/activate' command, then enter 'python manage.py' runserver to start the backend project.

- Open the browser and enter http://ec2-18-219-104-96.us-east-2.compute.amazonaws.com:8080/ to access the system.

### Functions:

- Survey design
  - Survey design
  - Create questionnaire
  - Edit questionnaire
  - Publish questionnaire
  - Delete questionnaire
  - Share questionnaire
- Result analysis
  - Answer statistics
  - Data visualization
- Backstage management
  - Ban user
  - Delete questionnaire

### Environment:

- Node.js：v10.15.1
- Vue.js：2.0
- Python：3.7.0
- Django：2.1.2
