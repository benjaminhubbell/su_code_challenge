from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, Instructor
from rest_framework.views import APIView
from rest_framework.response import Response

class ListCourses(APIView):

    # Method use to handle GET request
    def get(self, request):

        # Get query string param for campus
        campus = request.query_params.get('campus')
        
        # Get courses from database, filter if campus query string exists
        coursesFromDb = Course.objects.all() if campus is None else Course.objects.filter(classCampus = campus)
        
        courses = []

        for item in coursesFromDb:
            
            # Create empty dictionary object each iteration
            courseObject = {}

            # Add desired properties from course object
            courseObject["id"] = item.id
            courseObject["classNumber"] = item.classNumber
            courseObject["courseSubj"] = item.courseSubj
            courseObject["courseNum"] = item.courseNum
            courseObject["courseIdSubjNum"] = item.courseIdSubjNum
            courseObject["courseCredits"] = item.courseCredits
            courseObject["courseTitle"] = item.courseTitle
            courseObject["courseDescription"] = item.courseDescription
            courseObject["classSection"] = item.classSection
            courseObject["classStartDate"] = item.classStartDate
            courseObject["classEndDate"] = item.classEndDate
            courseObject["classMeetingDays"] = item.classMeetingDays
            courseObject["classMeetingTimes"] = item.classMeetingTimes
            courseObject["instructorId"] = item.instructor_id

            # Attempt to access Intructor object associated with this course
            try:
                instructor = Instructor.objects.get(netId = item.instructor_id)
                
                courseObject["instructorLastName"] = instructor.lastName
                courseObject["instructorFirstName"] = instructor.firstName
                courseObject["instructorEmailAddress"] = instructor.emailAddress
                courseObject["instructorDisplayName"] = instructor.displayName

            # If exception, course has no instructor, so fill properties with empty strings
            except Instructor.DoesNotExist:
                
                courseObject["instructorLastName"] = ""
                courseObject["instructorFirstName"] = ""
                courseObject["instructorEmailAddress"] = ""
                courseObject["instructorDisplayName"] = ""
            
            # Add this created course object to the list of courses to be added to results
            courses.append(courseObject)

        # Return object containing created course list and the number of courses in said list
        return Response({'count': coursesFromDb.count(), 'results': courses})