from rest_framework.status import HTTP_200_OK
from courses.models import Topic
from courses.serializers import AdminTopicResponse

class TopicServices:
  @classmethod
  def topicList(cls):
    topics = Topic.objects.all()
    topicResponse = AdminTopicResponse(topics,many=True)
    return topicResponse.data,HTTP_200_OK