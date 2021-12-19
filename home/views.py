from django.shortcuts import redirect, render
from rest_framework.views import APIView

class HomeView(APIView):
    def get(self, request):
        return redirect('homepage')
