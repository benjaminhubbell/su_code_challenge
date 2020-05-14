In order to fulfill the requirements for the coding challenge, I made a web application using Django REST framework. Here in the root directory, you will find the `addClasses.py` file. This is the file which can be run independent of the webserver running to add data to the database which represents the data in `static_classes.json`. It uses the `columns.py` file to provide column names for the queries that it runs.

The endpoint `/api/class` will provide a JSON response containing all courses which have been added, and the data is presented to match the example that was given in the requirements. Adding a query string parameter of `campus` will allow you to filter these results to only those classes which match your input parameter. The code which provides this endpoint is in the file `/su_code_challenge/courses/views.py`.

The tests for this endpoint can be found in the file `/su_code_challenge/courses/tests.py`. I have written tests with my own sample data to demonstrate:
  1. A successful 200 response
  2. A successful retreival of all data from endpoint `/api/class`
  3. A successful retreival of filtered data from endpoint `/api/class` with query string parameter `campus=MAIN`
