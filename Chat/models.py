from django.db import models
from DocSet.models import DocSet
import json


class Chat(models.Model):
    name = models.CharField(max_length=100)
    docSet = models.ForeignKey(DocSet, on_delete=models.DO_NOTHING, related_name='chats')
    history = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    # [
    #     {
    #         "role": "user",
    #         "content": "xxx"
    #     },
    #     {
    #         "role": "ai",
    #         "content": "xxx"
    #     },
    # ]

    def updateHistory(self, content):
        if self.history:
            history_list = json.loads(self.history)
            history_list.append(content)
            self.history = json.dumps(history_list)
        else:
            self.history = json.dumps([content])
        self.save()

    def getHistory(self):
        if self.history:
            return json.loads(self.history)
        else:
            return []
