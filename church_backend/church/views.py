from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import user_registerSerializer, helping_handSerializer,donateSerializer,timingsSerializer
from .models import user_register, helping_hand, donate, user_register,timings
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


class user_registerView(APIView):

    def post(self, request):
        serializer = user_registerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            subject = "Registration Successful - Welcome to PHC Church"
            message = "Dear user,\n\nYour registration has been successfully completed. Thank you for joining PHC Church.\n\nBlessings,\nPHC Team"

            recipient_email = serializer.validated_data.get('email')  # safer than serializer.data

            if recipient_email:
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email],
                        fail_silently=False
                    )
                except Exception as e:
                    return Response({"error": f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            user = get_object_or_404(user_register, id=id)
            serializer = user_registerSerializer(user)
            return Response(serializer.data)
        else:
            users = user_register.objects.all()
            serializer = user_registerSerializer(users, many=True)
            return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(user_register, id=id)
        serializer = user_registerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(user_register, id=id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class user_loginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use filter to avoid MultipleObjectsReturned
        user = user_register.objects.filter(email=email).first()

        if user and password == user.password:  # In production, use hashed passwords!
            serializer = user_registerSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class HelpingHandView(APIView):
    def get(self, request, user_id=None):
        print("Received user_id:", user_id)
        if user_id:
            helpings = helping_hand.objects.filter(user__id=user_id)
        else:
            helpings = helping_hand.objects.all()

        serializer = helping_handSerializer(helpings, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user')
        image = request.FILES.get('image')

        try:
            user = user_register.objects.get(id=user_id)
        except user_register.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        helping = helping_hand.objects.create(
            user=user,
            name=user.name,
            email=user.email,
            phone=user.phone,
            image=image
        )

        serializer = helping_handSerializer(helping)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        helping_id = request.data.get('id')
        try:
            helping = helping_hand.objects.get(id=helping_id)
            helping.delete()
            return Response({'message': 'Entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except helping_hand.DoesNotExist:
            return Response({'message': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

    
class DonateView(APIView):
    def post(self, request):
        serializer = donateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        print("Received user_id:", user_id)

        if user_id:
            donations = donate.objects.filter(id=user_id)
        else:
            donations = donate.objects.all()

        serializer = donateSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        donate_id = request.data.get('id')
        try:
            donation = donate.objects.get(id=donate_id)
        except donate.DoesNotExist:
            return Response({'message': 'Donation entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = donateSerializer(donation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        donate_id = request.data.get('id')
        try:
            donation = donate.objects.get(id=donate_id)
            donation.delete()
            return Response({'message': 'Donation entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except donate.DoesNotExist:
            return Response({'message': 'Donation entry not found'}, status=status.HTTP_404_NOT_FOUND)


# All Uses Count  
class user_count(APIView):
    def get(self, request):
        user_count = user_register.objects.count()
        return Response({'user_count': user_count})

# All users TO Display the data
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = user_register.objects.all()
    serializer_class = user_registerSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import timings, user_register
from .serializers import timingsSerializer


class TimingSend(APIView):
    def post(self, request):
        serializer = timingsSerializer(data=request.data)
        if serializer.is_valid():
            saved_timing = serializer.save()

            subject = "New PHC Church Timetable Added"
            message = (
                f"Dear Member,\n\n"
                f"A new church timetable entry has been added:\n\n"
                f"Day: {saved_timing.day}\n"
                f"Start Time: {saved_timing.startTime}\n"
                f"End Time: {saved_timing.endTime}\n"
                f"Description: {saved_timing.description}\n\n"
                f"Stay blessed,\nPHC Church"
            )

            recipient_list = list(
                user_register.objects
                .exclude(email__isnull=True)
                .exclude(email__exact='')
                .values_list('email', flat=True)
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False
                )
            except Exception as e:
                return Response(
                    {"error": f"Email sending failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimingView(APIView):
    def get(self, request, pk=None):
        if pk:
            timing = get_object_or_404(timings, pk=pk)
            serializer = timingsSerializer(timing)
            return Response(serializer.data)
        else:
            all_timings = timings.objects.all()
            serializer = timingsSerializer(all_timings, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        timing = get_object_or_404(timings, pk=pk)
        serializer = timingsSerializer(timing, data=request.data)

        if serializer.is_valid():
            updated = serializer.save()

            subject = "PHC Church Timetable Updated"
            message = (
                f"Dear Member,\n\n"
                f"The following church timetable entry has been updated:\n\n"
                f"Day: {updated.day}\n"
                f"Start Time: {updated.startTime}\n"
                f"End Time: {updated.endTime}\n"
                f"Description: {updated.description}\n\n"
                f"Please take note of the changes and attend accordingly.\n\n"
                f"Blessings,\nPHC Church"
            )

            recipient_list = list(
                user_register.objects
                .exclude(email__isnull=True)
                .exclude(email__exact='')
                .values_list('email', flat=True)
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False
                )
            except Exception as e:
                return Response(
                    {"error": f"Email sending failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        timing = get_object_or_404(timings, pk=pk)
        timing.delete()
        return Response(
            {'message': 'Timing entry deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class TimingSend(APIView):
    def post(self, request):
        serializer = timingsSerializer(data=request.data)
        if serializer.is_valid():
            saved_timing = serializer.save()

            subject = "New PHC Church Timetable Added"
            message = (
                f"Dear Member,\n\n"
                f"A new church timetable entry has been added:\n\n"
                f"Day: {saved_timing.day}\n"
                f"Start Time: {saved_timing.startTime}\n"
                f"End Time: {saved_timing.endTime}\n"
                f"Description: {saved_timing.description}\n\n"
                f"Stay blessed,\nPHC Church"
            )

            recipient_list = list(
                user_register.objects
                .exclude(email__isnull=True)
                .exclude(email__exact='')
                .values_list('email', flat=True)
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False
                )
            except Exception as e:
                return Response(
                    {"error": f"Email sending failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimingView(APIView):
    def get(self, request, pk=None):
        if pk:
            timing = get_object_or_404(timings, pk=pk)
            serializer = timingsSerializer(timing)
            return Response(serializer.data)
        else:
            all_timings = timings.objects.all()
            serializer = timingsSerializer(all_timings, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        timing = get_object_or_404(timings, pk=pk)
        serializer = timingsSerializer(timing, data=request.data)

        if serializer.is_valid():
            updated = serializer.save()

            subject = "PHC Church Timetable Updated"
            message = (
                f"Dear Member,\n\n"
                f"The following church timetable entry has been updated:\n\n"
                f"Day: {updated.day}\n"
                f"Start Time: {updated.startTime}\n"
                f"End Time: {updated.endTime}\n"
                f"Description: {updated.description}\n\n"
                f"Please take note of the changes and attend accordingly.\n\n"
                f"Blessings,\nPHC Church"
            )

            recipient_list = list(
                user_register.objects
                .exclude(email__isnull=True)
                .exclude(email__exact='')
                .values_list('email', flat=True)
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False
                )
            except Exception as e:
                return Response(
                    {"error": f"Email sending failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        timing = get_object_or_404(timings, pk=pk)
        timing.delete()
        return Response(
            {'message': 'Timing entry deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
