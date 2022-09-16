from functools import partial
from django.db.models.query_utils import Q
from rest_framework.decorators import action
from rest_framework.status import *

from datetime import *

from meta.models import File
from courses.models import Course, Topic, Agenda
from courses.serializers.course import CourseRequest, CourseResponse
from courses.models import CertificationTrack

class CourseService:
    
    @classmethod
    def create(cls, data, currentUser):
        print("<---- courses.services.CourseService.create ---->")

        courseRequest = CourseRequest(data = data,partial=True)
        if courseRequest.is_valid():
            validData = courseRequest.validated_data
            
            material = validData.pop('material', None)
            topics = validData.pop('topic', None)
            agenda = validData.pop('agenda', None)

            course = Course.objects.create(
                **dict(
                    validData,
                    createdBy = currentUser
                )
            )
            if topics:
                for t in topics:
                    tObj = Topic.objects.get(id=t.get('id'))
                    if t.get('action') == 'ADD':
                        course.topic.add(tObj)
                    elif t.get('action') == 'DELETE':
                        course.topic.remove(tObj)
            if material:
                print('This is material : ',material)
                for m in material:
                    mObj = File.objects.get(id=m.get('id'))
                    if m.get('action') == 'ADD':
                        course.material.add(mObj)
                    elif m.get('action') == 'DELETE':
                        course.material.remove(mObj)
            if agenda:
                for a in agenda:
                    course.agenda.add(Agenda.objects.create(**dict(a, createdBy=currentUser)))
                        
            courseResponse = CourseResponse(course)
            
            response, status = courseResponse.data, HTTP_201_CREATED
        else:
            print("Data invalid")
            print(courseRequest.errors)
            response, status = courseRequest.errors, HTTP_400_BAD_REQUEST

        return response, status

    @classmethod
    def update(cls, id, data, currentUser):
        print("<---- courses.services.CourseService.update ---->")

        courseRequest = CourseRequest(data=data, partial=True)
        try:
            if courseRequest.is_valid():
                print("Data valid")
                print('Validated Data  : ',courseRequest.validated_data)
                validData = courseRequest.validated_data.copy()

                material = validData.pop('material', None)
                topic = validData.pop('topic', None)
                agenda = validData.pop('agenda', None)

                oldValues = {}
                course = Course.objects.get(id = id)
                print("course found")

                for (k, v) in validData.items():
                    oldValues[k] =  getattr(course, k)
                    setattr(course, k, v)

                if topic:
                    for t in topic:
                        tObj = Topic.objects.get(id=t.get('id'))
                        if t.get('action') == 'ADD':
                            course.topic.add(tObj)
                        elif t.get('action') == 'DELETE':
                            course.topic.remove(tObj)

                if material:
                    for m in material:
                        mObj = File.objects.get(id=m.get('id'))
                        if m.get('action') == 'ADD':
                            course.material.add(mObj)
                        elif m.get('action') == 'DELETE':
                            course.material.remove(mObj)
                print('materials')
                if agenda:
                    for a in agenda:
                        aObjs = course.agenda.all()
                        if aObjs.filter(day=a.get('day')).count() > 0:
                            aObj = aObjs.filter(day=a.get('day'))[0]
                            aObj.value = a.get('value')
                            aObj.save()
                            print("agenda edited")
                        else:
                            course.agenda.add(Agenda.objects.create(**dict(a, createdBy=currentUser)))
                            print("agenda added")
                print('All are updated')
                course.update(oldValues, currentUser)

                courseResponse = CourseResponse(course)
                response, status = courseResponse.data, HTTP_200_OK
            else:
                print("Invalid Data : ",data)
                print(courseRequest.errors)
                response, status = courseRequest.errors, HTTP_400_BAD_REQUEST
        except Course.DoesNotExist:
            response, status = dict(error = "Couse not found"), HTTP_404_NOT_FOUND
        except Course.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Couses found"), HTTP_400_BAD_REQUEST
            print("Multiple Couses with one id, WTF!!")
            
        print(response)
        return response, status

    @classmethod
    def getCourse(cls, id):
        print("<---- courses.services.CourseService.get ---->")

        try:
            course = Course.objects.get(id = id)
            courseResponse = CourseResponse(course)
            response, status = courseResponse.data, HTTP_200_OK
        except Course.DoesNotExist:
            response, status = dict(error = "Course not found"), HTTP_404_NOT_FOUND
        except Course.MultipleObjectsReturned:
            response, status = dict(error = "Multiple courses found"), HTTP_400_BAD_REQUEST
            print("WTF!!")

        return response, status

    @classmethod
    def delete(cls, id,currentUser):
        print("<---- courses.services.CourseService.delete ---->")

        try:
            course = Course.objects.get(id=id)
            course.delete(currentUser=currentUser)
            response, status = dict(message="Course Deleted"), HTTP_200_OK
        except Course.DoesNotExist:
            response, status = dict(error="Course not found"), HTTP_404_NOT_FOUND
        except Course.MultipleObjectsReturned:
            response, status = dict(error = "Multiple courses found"), HTTP_400_BAD_REQUEST
            print("WTF!!")
        return response, status
    @classmethod
    def getAll(cls,params=None):
        print("<---- courses.services.CourseService.getAll ---->")
        try:
            if params:
                courseid = params.get('scid',None)
                title = params.get('stitle',None)
                isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None
                isNew = True if params.get('snew')=='true' else False if params.get('snew')=='false' else None
                created = params.get('screatedat')
                if created:
                    createdon = datetime.strptime(created,'%Y-%m-%d')
                else:
                    createdon = None                
                courses = Course.objects.all()
                if courseid:
                    courses = courses.filter(courseNum__contains=courseid).order_by('courseNum')
                if title:
                    courses = courses.filter(title__icontains=title).order_by('courseNum')
                if isActive in (True,False):
                    courses = courses.filter(isActive__exact = isActive).order_by('courseNum')
                if created:
                    courses = courses.filter(created__date=createdon).order_by('courseNum')
                if isNew:
                    courses = courses.filter(isNew__exact=isNew).order_by('courseNum')
            else:
                courses = Course.objects.all().order_by('courseNum')        
            coursesResponse = CourseResponse(courses, many=True)
            response, status = coursesResponse.data, HTTP_200_OK
        except ValueError:
            response,status = dict(error = "There is some error that i dont know"), HTTP_404_NOT_FOUND
        return response, status

    @classmethod
    def getAll2(cls,params=None):
        print("<---- courses.services.CourseService.getAll ---->")

        if params:
            courseNum = params.get('scid',None)
            title = params.get('stitle',None)
            topicId = params.get('stopicid',None)
            trackId = params.get('strackid',None)
           
            courses = Course.objects.all().filter(isActive = True)
            if courseNum:
                courses = courses.filter(courseNum__contains=courseNum)
            if title:
                courses = courses.filter(title__icontains=title)
            if topicId:
                topic = Topic.objects.get(id=topicId)
                courses = courses.filter(topic=topic)
            else:
                topic=None
            if trackId:
                courses=[]
                tracks = CertificationTrack.objects.get(id=trackId)
                requiredCourses = tracks.requiredCourses.all()
                optionalCourses = tracks.optionalCourses.all()
                for course in requiredCourses:
                    if course in Course.objects.all().order_by('courseNum'):
                        courses.append(course)
                for course in optionalCourses:
                    if course in Course.objects.all().order_by('courseNum'):
                        courses.append(course)
            else:
                tracks=None
        else:
            courses = Course.objects.filter(isActive = True).only('id', 'courseNum', 'title', 'isActive', 'isNew', 'created', 'createdBy')

        coursesResponse = CourseResponse(courses, many=True)
        response, status = coursesResponse.data, HTTP_200_OK
        return response, status
