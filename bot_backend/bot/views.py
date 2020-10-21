from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from bot.serializers import OhayouSerializer

from .models import Ohayou


class OhayouViewSets(ModelViewSet):
    queryset = Ohayou.objects.all()
    serializer_class = OhayouSerializer


    def create(self, request):
        serializer = OhayouSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Ohayou.objects.filter(text=serializer.validated_data["text"]).exists():
            return Response({"message": "既に存在しているレスポンスです"})
        Ohayou.objects.create(text=serializer.validated_data["text"])
        return Response({"message": f"{serializer.validated_data['text']} をあいさつレスポンスに追加しました"})


    @action(methods=["get"], detail=False)
    def generate(self, request):
        obj = Ohayou.objects.all().order_by("?").first()
        return Response({"message": obj.text})