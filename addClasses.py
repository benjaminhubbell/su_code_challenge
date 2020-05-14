import json
import sqlite3
from columns import courseFields, facilityFields, instructorFields, \
biographyFields, jobTitleFields



# Summary: Method to connect to database
# Parameters:
#   dbFile - Path to db which we are connecting to
def connect(dbFile):

    connection = None

    try:
        connection = sqlite3.connect(dbFile)
    except Error as e:
        print(e)

    return connection



# Summary: Method to determine of instructor exists with the database already
# Parameters:
#   connection - Database connection
#   netId - The netId (PK) of the instructor
def doesInstructorExist(connection, netId):
    
    # Create sql statement
    # String params:
    #   1 - netId of the instructor
    sql = \
    """ SELECT
            *
        FROM courses_instructor
        WHERE
            netId = '{0}'
    """.format(netId)

    cursor = connection.cursor()

    # Execute sql statement
    cursor.execute(sql)

    # return boolean indicating whether any rows were returned from sql query
    return len(cursor.fetchall()) > 0



# Summary: Method to create a facility object in database
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing the facility
def createFacility(connection, obj):
    
    # Create sql statement
    # String params:
    #   1 - CSV of fields for facility table
    #   2 - CSV of ?s for populating values to insert
    sql = \
    """ INSERT INTO courses_facility
        ({0})
        VALUES ({1})
    """.format(', '.join(facilityFields), ', '.join("?" * len(facilityFields)))
    
    cursor = connection.cursor()

    
    try:
        # Create a tuple of the data to insert and execute query
        cursor.execute(sql, tuple(obj[x] for x in facilityFields))
    except sqlite3.Error as e:
        print(e)



# Summary: Method to create an instructor object in database
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing the instructor
def createInstructor(connection, obj):
    
    # Create sql statement
    # String params:
    #   1 - CSV of fields for instructor table
    #   2 - CSV of ?s for populating values to insert
    sql = \
    """ INSERT INTO courses_instructor
        ({0})
        VALUES ({1})
    """.format(', '.join(instructorFields), ', '.join("?" * len(instructorFields)))
    
    cursor = connection.cursor()

    
    try:
        # Create a tuple of the data to insert and execute query
        cursor.execute(sql, tuple(obj[x] for x in instructorFields))
    except sqlite3.Error as e:
        print(e)

    # Add each biography in instructor object to database
    for x in obj["biographies"]:
        x["instructor_id"] = obj["netId"]
        createBiography(connection, x)

    # Add each job title in instructor object to database
    for x in obj["jobTitles"]:
        x["instructor_id"] = obj["netId"]
        createJobTitle(connection, x)



# Summary: Method to create a course object in database
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing the course
#   hasInstructor - Boolean indicating whether course has been assigned an instructor
def createCourse(connection, obj, hasInstructor):

    # If course does not have instructor, remove last item from courseFields
    # as there will be no associated instructor_id, which is the last item
    fields = courseFields if hasInstructor else courseFields[0:-1]

    # Create sql statement
    # String params:
    #   1 - CSV of fields for course table
    #   2 - CSV of ?s for populating values to insert
    sql = \
    """ INSERT INTO courses_course
        ({0})
        VALUES ({1})
    """.format(', '.join(fields), ', '.join("?" * len(fields)))

    cursor = connection.cursor()

    
    try:
        # Create a tuple of the data to insert and execute query
        cursor.execute(sql, tuple(obj[x] for x in fields))
    except sqlite3.Error as e:
        print(e)



# Summary: Method to create a facility object in biography
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing the biography
def createBiography(connection, obj):

    # Create sql statement
    # String params:
    #   1 - CSV of fields for biography table
    #   2 - CSV of ?s for populating values to insert
    sql = \
    """ INSERT INTO courses_biography
        ({0})
        VALUES ({1})
    """.format(', '.join(biographyFields), ', '.join("?" * len(biographyFields)))
    
    cursor = connection.cursor()

    
    try:
        # Create a tuple of the data to insert and execute query
        cursor.execute(sql, tuple(obj[x] for x in biographyFields))
    except sqlite3.Error as e:
        print(e)


# Summary: Method to create a job title object in database
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing the job title
def createJobTitle(connection, obj):
    
    # Create sql statement
    # String params:
    #   1 - CSV of fields for job title table
    #   2 - CSV of ?s for populating values to insert
    sql = \
    """ INSERT INTO courses_jobtitle
        ({0})
        VALUES ({1})
    """.format(', '.join(jobTitleFields), ', '.join("?" * len(jobTitleFields)))
    
    cursor = connection.cursor()

    try:
        # Create a tuple of the data to insert and execute query
        cursor.execute(sql, tuple(obj[x] for x in jobTitleFields))
    except sqlite3.Error as e:
        print(e)



# Summary: Method to start the process of adding a course to the database
# Parameters:
#   connection - Database connection
#   obj - Dictionary object representing one course
def createObjects(connection, obj):
    
    # If object contains an instructor, assign it here, otherwise none
    instructor = None if len(obj["instructorsFullInfo"]) < 1 else obj["instructorsFullInfo"][0]

    course["instructor_id"] = 0
    hasInstructor = instructor is not None
    
    # If course has instructor assigned and that instuctor does not already exists
    # in database, then add instructor to database
    if (hasInstructor and not doesInstructorExist(connection, instructor["netId"])):
        createInstructor(connection, instructor)

    # Add instructor id to dictionary to be used as foreign key
    if hasInstructor:
        course["instructor_id"] = instructor["netId"]
    
    # Add course to database
    createCourse(connection, course, hasInstructor)

    # Add each facility to database
    for x in obj["facilities"]:
        x['course_id'] = obj["id"]
        createFacility(connection, x)



# Create database connection
connection = connect("db.sqlite3")

# Open local file with courses data
with open("static_classes.json") as myFile:
    
    # Create dictionary with courses data
    data = json.load(myFile)
    
    # Use database connection
    with connection:
    
        # Iterate over each course in courses dictionary
        for course in data:
            
            # Create entry in database for each course
            createObjects(connection, course)