from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from users.models.score import Score

from users.serializers.scoreresource import ScoreResource


class MyScoresView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        scores = Score.objects.filter(user=request.user)
        
        # سریالایز کردن آدرس‌ها
        scores_data = ScoreResource(scores, many=True).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'scores':scores_data}, status=status.HTTP_200_OK)
