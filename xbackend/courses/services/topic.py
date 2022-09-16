from django.db.models.query_utils import Q
from rest_framework.status import *

from datetime import *

from courses.models import Topic
from courses.serializers import AdminTopicRequest, AdminTopicResponse

class TopicService():

    @classmethod
    def getAllTopics(cls,params=None):
        global createdon
        createdon = None
        print("<---- courses.services.TopicService.getAllTopics ---->")       

        try:
            if params:
                id = params.get('stid')
                name = params.get('stname')
                created = params.get('screatedat')

                if created:
                    createdon = datetime.strptime(created,'%Y-%m-%d')
                topics = Topic.objects.all()
                if id:
                    topics = topics.filter(id=id)
                if name:
                    topics = topics.filter(name__startswith=name)
                if created:
                    topics = topics.filter(created__date=createdon)

            else:
                topics = Topic.objects.defer('history', 'isDeleted')
            topicsResponse = AdminTopicResponse(topics, many=True)
            response,status = topicsResponse.data,HTTP_200_OK
            
        except ValueError:
           response,status = dict(error = "There is some error that i dont know"), HTTP_404_NOT_FOUND

        return response, status

    @classmethod
    def getTopic(cls, id):
        print("<---- courses.services.TopicService.getTopic ---->")

        try:
            topic = Topic.objects.get(id=id)
            topicResponse = AdminTopicResponse(topic)
            response, status = topicResponse.data, HTTP_200_OK
        except Topic.DoesNotExist:
            response, status = dict(error = "Topic not found"), HTTP_404_NOT_FOUND
        except Topic.MultipleObjectsReturned:
            response, status = dict(error = "Multiple topics found"), HTTP_400_BAD_REQUEST
            print("Multiple topics with one id, WTF!!")

        return response, status

    @classmethod
    def deleteTopic(cls, id, currentUser):
        print("<---- courses.services.TopicService.deleteTopic ---->")
        print(id)
        try:
            topic = Topic.objects.get(id=id)
            topic.delete(currentUser=currentUser)
            response, status = dict(message="Topic Deleted"), HTTP_200_OK
        except Topic.DoesNotExist:
            response, status = dict(error = "Topic not found"), HTTP_404_NOT_FOUND
        except Topic.MultipleObjectsReturned:
            response, status = dict(error = "Multiple topics found"), HTTP_400_BAD_REQUEST
            print("Multiple topics with one id, WTF!!")

        return response, status

    @classmethod
    def createTopic(cls, data, currentUser):
        print("<---- courses.services.TopicService.createTopic ---->")

        topicRequest = AdminTopicRequest(data = data)
        if topicRequest.is_valid():
            print("Data valid")
            print(topicRequest.validated_data)
            topic = Topic.objects.create(
                **dict(
                    topicRequest.validated_data,
                    createdBy = currentUser
                )
            )
            topicResponse = AdminTopicResponse(topic)
            response, status = topicResponse.data , HTTP_201_CREATED
        else:
            print("Data Invalid")
            print(topicRequest.errors)
            response, status = topicRequest.errors, HTTP_400_BAD_REQUEST

        return response, status

    @classmethod
    def updateTopic(cls, id, data, currentUser):
        print("<---- courses.services.TopicService.updateTopic ---->")

        topicRequest = AdminTopicRequest(data=data, partial=True)
        try:
            if topicRequest.is_valid():
                print("Data valid")
                print(topicRequest.validated_data)
                
                topic = Topic.objects.get(id=id)
                oldValue = topic.name
                topic.name = topicRequest.validated_data.get('name')

                topic.update(oldValue, currentUser)
                topicResponse = AdminTopicResponse(topic)
                response, status = topicResponse.data, HTTP_200_OK
            else:
                print("Data Invalid")
                print(topicRequest.errors)
                response, status = topicRequest.errors, HTTP_400_BAD_REQUEST
        except Topic.DoesNotExist:
            response, status = dict(error = "Topic not found"), HTTP_404_NOT_FOUND
        except Topic.MultipleObjectsReturned:
            response, status = dict(error = "Multiple topics found"), HTTP_400_BAD_REQUEST
            print("Multiple topics with one id, WTF!!")

        return response, status
