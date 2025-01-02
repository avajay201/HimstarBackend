# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Category
from django.shortcuts import get_object_or_404
from .models import Competition, Category, Round, Tournament, CompetitionMedia
from .serializers import CategorySerializer,CompetitionSerializer, RoundSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated
from video.models import Participant
from django.utils.timezone import now
from django.db.models import Count
from accounts.models import Register


# class CompetitionListCreateView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         competitions = Competition.objects.all()
#         serializer = CompetitionSerializer(competitions, many=True, context={'user_id': user_id})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CompetitionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all categories
class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Retrieve a single category by ID
class CategoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class CompetitionDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             competition = Competition.objects.get(pk=pk)
#         except Competition.DoesNotExist:
#             return Response({'detail': 'Competition not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = CompetitionSerializer(competition)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             competition = Competition.objects.get(pk=pk)
#         except Competition.DoesNotExist:
#             return Response({'detail': 'Competition not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = CompetitionSerializer(competition, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             competition = Competition.objects.get(pk=pk)
#         except Competition.DoesNotExist:
#             return Response({'detail': 'Competition not found.'}, status=status.HTTP_404_NOT_FOUND)

#         competition.delete()
#         return Response({'detail': 'Competition deleted.'}, status=status.HTTP_204_NO_CONTENT)


# API View for Round
class RoundListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rounds = Round.objects.all()
        serializer = RoundSerializer(rounds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoundDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            round_instance = Round.objects.get(pk=pk)
        except Round.DoesNotExist:
            return Response({'detail': 'Round not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoundSerializer(round_instance)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            round_instance = Round.objects.get(pk=pk)
        except Round.DoesNotExist:
            return Response({'detail': 'Round not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoundSerializer(round_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            round_instance = Round.objects.get(pk=pk)
        except Round.DoesNotExist:
            return Response({'detail': 'Round not found.'}, status=status.HTTP_404_NOT_FOUND)

        round_instance.delete()
        return Response({'detail': 'Round deleted.'}, status=status.HTTP_204_NO_CONTENT)


# API View for Participant






# Custom API to eliminate participants (Elimination logic for rounds)
class EliminateParticipantsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, round_id):
        try:
            round_instance = Round.objects.get(pk=round_id)
        except Round.DoesNotExist:
            return Response({'detail': 'Round not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Eliminate participants (custom logic, for example, eliminating 20%)
        participants = round_instance.participants.all()
        eliminated_count = int(len(participants) * 0.20)
        eliminated_participants = participants[:eliminated_count]

        for participant in eliminated_participants:
            participant.is_active = False
            participant.save()

        return Response({'detail': f'{eliminated_count} participants have been eliminated.'}, status=status.HTTP_200_OK)


# Custom API to start the next round of a tournament
class StartNextRoundView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'detail': 'Tournament not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the tournament has more rounds and start the next round
        if tournament.current_round < tournament.total_rounds:
            tournament.current_round += 1
            tournament.save()
            return Response({'detail': f'Round {tournament.current_round} has started.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No more rounds left in the tournament.'}, status=status.HTTP_400_BAD_REQUEST)


class CompetitionsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        category_id = request.GET.get('category_id')
        # active_competitions = Competition.objects.filter(
        #     is_active=True,
        #     start_date__lte=now().date(),
        #     end_date__gte=now().date(),
        #     competition_type='competition',
        # )
        # upcoming_competitions = Competition.objects.filter(
        #     is_active=True,
        #     start_date__gt=now().date(),
        #     end_date__gt=now().date(),
        #     # registration_open_date__gt=now().date(),
        #     # registration_close_date__gt=now().date(),
        #     competition_type='competition',
        # )
        active_competitions = Competition.objects.filter(
            is_active=True,
            registration_open_date__lte=now().date(),
            registration_close_date__gte=now().date(),
            competition_type='competition',)
        upcoming_competitions = Competition.objects.filter(
            is_active=True,
            start_date__gt=now().date(),
            registration_open_date__gt=now().date(),
            competition_type='competition',)

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            active_competitions = active_competitions.filter(category=category)
            upcoming_competitions = active_competitions.filter(category=category)
        active_competitions_serializer = CompetitionSerializer(active_competitions, many=True, context={'user_id': user_id})
        upcoming_competitions_serializer = CompetitionSerializer(upcoming_competitions, many=True, context={'user_id': user_id})
        return Response({'active': active_competitions_serializer.data, 'upcoming': upcoming_competitions_serializer.data}, status=status.HTTP_200_OK)

class MyCompetitions(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        register = Register.objects.filter(user=request.user.id).first()
        participants = Participant.objects.filter(user=register).values_list('competition', flat=True)
        competitions = Competition.objects.filter(id__in=participants)
        serializer = CompetitionSerializer(competitions, many=True, context={'user_id': request.user.id})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TournamentsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        category_id = request.GET.get('category_id')
        tournaments = Tournament.objects.filter(
            is_active=True,
            end_date__gte=now().date(),
        )
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            tournaments = tournaments.filter(category=category)
        serializer = TournamentSerializer(tournaments, many=True, context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

class LeaderBoard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        competition_id = request.data.get('competition_id')
        competition = get_object_or_404(Competition, id=competition_id)

        # Get participants with likes count
        participants = Participant.objects.filter(competition=competition).annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')

        # Format response
        response_data = []
        for index, participant in enumerate(participants):
            response_data.append({
                'id': index + 1,
                'username': participant.user.user.username,
                'profile_picture': participant.user.profile_image.url if participant.user.profile_image else None,
                'likes': participant.likes_count,
            })

        return Response(response_data, status=200)

class ParticularCompetition(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user_id = request.user.id
        competition = Competition.objects.filter(id=id).first()
        if not competition:
            return Response({'detail': 'Competition not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompetitionSerializer(competition, context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)
