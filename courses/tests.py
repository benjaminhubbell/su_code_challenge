from .models import Course, Instructor
from rest_framework.test import APITestCase, APIClient
import json

# Class to test API
class CoursesTests(APITestCase):

    client = APIClient()

    # Method to set up our temporary database objects
    def setUp(self):

        instructor = Instructor.objects.create(netId="bdhubbel", lastName="Hubbell", firstName="Benjamin", emailAddress="bdhubbel@syr.edu", \
        displayName="Benjamin Hubbell", nameLastFirstInitial="Hubbell, B", campusPhone="", campusBuilding="", campusOfficeRoom="", \
        photoUrl="syr.edu", curriculumVitaePublicAccessFlag=False, curriculumVitaeUrl="syr.edu")
        
        Course.objects.create(id="1234.5678", classNumber=12345, courseSubj="CIS", courseNum=600, courseIdSubjNum="CIS600", \
        courseCredits=3.0, courseTitle="Advanced Programming Concepts", courseDescription="You're gonna code a bunch, I promise.",\
        classSection="M001", classStart="2020-05-18T00:00:00", classEnd="2020-06-26T00:00:00", classCampus="ONL", classMon=False, \
        classTue=False, classWed=False, classThu=False, classFri=False, classSat=False, classSun=False, classSessionCode="6W1", \
        classAcadCareer="GRD", classLocationCode="MC", classInstructionMode="O6", classEnrollmentCapacity=30, classEnrollmentTotal=0, \
        classNotes="Did I mention you're gonna code a lot?", lastUpdate="2020-05-11T06:56:04.84", isGrad=False, isOnline=False,\
        classStartDate="2020-05-18T00:00:00", classEndDate="2020-06-26T00:00:00", classMeetingDays = "Tu, Th", classMeetingTimes="12:00pm - 1:40pm",\
        syllabusAccessFlag=False, syllabusAuthOnly=False, syllabusContentFileId=False, syllabusUrl=False, professorOfRecord=None, \
        instructor=instructor)

        Course.objects.create(id="8765.4321", classNumber=54321, courseSubj="CSE", courseNum=600, courseIdSubjNum="CSE600", \
        courseCredits=3.0, courseTitle="Advanced Circuits", courseDescription="You're gonna make a bunch of circuits, I promise.",\
        classSection="M001", classStart="2020-05-18T00:00:00", classEnd="2020-06-26T00:00:00", classCampus="MAIN", classMon=False, \
        classTue=False, classWed=False, classThu=False, classFri=False, classSat=False, classSun=False, classSessionCode="6W1", \
        classAcadCareer="GRD", classLocationCode="MC", classInstructionMode="O6", classEnrollmentCapacity=30, classEnrollmentTotal=0, \
        classNotes="Electricity and stuff!!", lastUpdate="2020-05-11T06:56:04.84", isGrad=False, isOnline=False,\
        classStartDate="2020-05-18T00:00:00", classEndDate="2020-06-26T00:00:00", classMeetingDays = "Tu, Th", classMeetingTimes="12:00pm - 1:40pm",\
        syllabusAccessFlag=False, syllabusAuthOnly=False, syllabusContentFileId=False, syllabusUrl=False, professorOfRecord=None, \
        instructor=instructor)

    # Test for a successful response
    # Passing Criteria:
    #   A status code of 200, indicating the GET request was successful
    def test_response_success(self):

        # issue GET request at endpoint `/api/courses`
        response = self.client.get('/api/classes/')

        # assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

    # Test for expected results when sending GET request to retreive all data
    # Passing Criteria:
    #   Count equals two, indicating that both courses which were created were returned
    #   Results list includes both courses which were created
    def test_data_match(self):

        # issue GET request at endpoint `/api/courses`
        response = self.client.get('/api/classes/')
        
        # convert response content to dictionary
        responseDict = json.loads(response.content.decode("utf-8"))
        
        # verify there were two results
        countSuccess = (responseDict["count"] == 2)

        # verify the first result matches the object we created
        data = responseDict["results"][0]
        firstItemSuccess = (data["id"] == "1234.5678" and data["classNumber"] == 12345 and data["courseSubj"] == "CIS" and data["courseNum"] == 600 and \
        data["courseIdSubjNum"] == "CIS600" and data["courseCredits"] == 3.0 and data["courseTitle"] == "Advanced Programming Concepts" and \
        data["courseDescription"] == "You're gonna code a bunch, I promise." and data["classSection"] == "M001" and \
        data["classStartDate"] == "2020-05-18T00:00:00" and data["classEndDate"] == "2020-06-26T00:00:00" and data["classMeetingDays"] == "Tu, Th" and \
        data["classMeetingTimes"] == "12:00pm - 1:40pm" and data["instructorLastName"] == "Hubbell" and data["instructorFirstName"] == "Benjamin" and \
        data["instructorEmailAddress"] == "bdhubbel@syr.edu" and data["instructorDisplayName"] == "Benjamin Hubbell")
        
        # verify the second result matches the object we created
        data = responseDict["results"][1]
        secondItemSuccess = (data["id"] == "8765.4321" and data["classNumber"] == 54321 and data["courseSubj"] == "CSE" and data["courseNum"] == 600 and \
        data["courseIdSubjNum"] == "CSE600" and data["courseCredits"] == 3.0 and data["courseTitle"] == "Advanced Circuits" and \
        data["courseDescription"] == "You're gonna make a bunch of circuits, I promise." and data["classSection"] == "M001" and \
        data["classStartDate"] == "2020-05-18T00:00:00" and data["classEndDate"] == "2020-06-26T00:00:00" and data["classMeetingDays"] == "Tu, Th" and \
        data["classMeetingTimes"] == "12:00pm - 1:40pm" and data["instructorLastName"] == "Hubbell" and data["instructorFirstName"] == "Benjamin" and \
        data["instructorEmailAddress"] == "bdhubbel@syr.edu" and data["instructorDisplayName"] == "Benjamin Hubbell")

        # assert that each of our success conditions are true
        self.assertTrue(countSuccess and firstItemSuccess and secondItemSuccess)

    # Test to check if the campus filter is working
    # Passing Criteria:
    #   Count equals one, indicating that only the single course on MAIN campus was returned
    #   Results list includes only the single course on MAIN campus
    def test_campus_filter(self):

        # issue GET request at endpoint `/api/courses` with query string campus=MAIN
        response = self.client.get('/api/classes/', { "campus": "MAIN"})

        # convert response content to dictionary
        responseDict = json.loads(response.content.decode("utf-8"))

        # verify there was one result
        countSuccess = responseDict["count"] = 1
        
        # verify the first result matches the object we created which has property campus = MAIN
        data = responseDict["results"][0]
        itemSuccess = (data["id"] == "8765.4321" and data["classNumber"] == 54321 and data["courseSubj"] == "CSE" and data["courseNum"] == 600 and \
        data["courseIdSubjNum"] == "CSE600" and data["courseCredits"] == 3.0 and data["courseTitle"] == "Advanced Circuits" and \
        data["courseDescription"] == "You're gonna make a bunch of circuits, I promise." and data["classSection"] == "M001" and \
        data["classStartDate"] == "2020-05-18T00:00:00" and data["classEndDate"] == "2020-06-26T00:00:00" and data["classMeetingDays"] == "Tu, Th" and \
        data["classMeetingTimes"] == "12:00pm - 1:40pm" and data["instructorLastName"] == "Hubbell" and data["instructorFirstName"] == "Benjamin" and \
        data["instructorEmailAddress"] == "bdhubbel@syr.edu" and data["instructorDisplayName"] == "Benjamin Hubbell")

        # assert that each of our success conditions are true
        self.assertTrue(countSuccess and itemSuccess)