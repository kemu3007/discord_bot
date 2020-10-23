import datetime

import requests
from pyquery import PyQuery
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from bot.serializers import OhayouSerializer
from bot_backend.env import env

from .models import Ohayou


class HoloduleView(APIView):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    }
    youtube_api_url = "https://www.googleapis.com/youtube/v3/videos?id={}&part=snippet,liveStreamingDetails&fields=items(id,snippet(title),liveStreamingDetails(scheduledStartTime))&key={}"
    holodule_url = "https://schedule.hololive.tv/simple/hololive"

    def prepare_data(self, response: PyQuery):
        stream_urls = [
            PyQuery(a).attr("href")
            for a in response("a")
            if "youtube" in PyQuery(a).attr("href")
        ]
        video_info = [
            PyQuery(a).text()
            for a in response("a")
            if "youtube" in PyQuery(a).attr("href")
        ]
        video_ids = [
            url.replace("https://www.youtube.com/watch?v=", "") for url in stream_urls
        ]
        youtube_responses = requests.get(
            self.youtube_api_url.format(",".join(video_ids), env.str("API_KEY"))
        )
        youtube_dict = {
            response["id"]: response for response in youtube_responses.json()["items"]
        }
        message = ""
        for index, video_id in enumerate(video_ids):
            if "liveStreamingDetails" in youtube_dict[video_id]:
                if datetime.datetime.now() < datetime.datetime.strptime(
                    youtube_dict[video_id]["liveStreamingDetails"][
                        "scheduledStartTime"
                    ],
                    "%Y-%m-%dT%H:%M:%SZ",
                ):
                    message += f"{video_info[index]} {youtube_dict[video_id]['snippet']['title']} ({stream_urls[index]}) \n"
        return message

    def get(self, request):
        response = PyQuery(self.holodule_url)
        return Response({"message": self.prepare_data(response)})


class OhayouViewSets(ModelViewSet):
    queryset = Ohayou.objects.all()
    serializer_class = OhayouSerializer

    def create(self, request):
        serializer = OhayouSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Ohayou.objects.filter(text=serializer.validated_data["text"]).exists():
            return Response({"message": "既に存在しているレスポンスです"})
        Ohayou.objects.create(text=serializer.validated_data["text"])
        return Response(
            {"message": f"{serializer.validated_data['text']} をあいさつレスポンスに追加しました"}
        )

    @action(methods=["get"], detail=False)
    def generate(self, request):
        obj = Ohayou.objects.all().order_by("?").first()
        return Response({"message": obj.text})
