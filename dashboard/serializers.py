# serializers.py
from rest_framework import serializers
from .models import Category, Round, Tournament
from video.models import Participant
from video.models import Like, Comment
from datetime import date
from accounts.models import Register
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# serializers.py
from rest_framework import serializers
from .models import Competition
from video.models import Participant

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_id = self.context.get('user_id')
        register = Register.objects.filter(user=user_id).first()
        is_participated = Participant.objects.filter(competition=instance, user=register).first()
        participants = Participant.objects.filter(competition=instance)

        representation['category'] = instance.category.name if instance.category else None
        representation['is_participated'] = True if is_participated else False
        representation['stage'] = instance.stage.name if instance.stage else None
        representation['is_close'] = instance.end_date < date.today()
        representation['is_done'] = True if is_participated and (is_participated.file_uri or 'media' in is_participated.video.url) else False
        if instance.competition_type == 'competition':
            representation['reg_open'] = instance.registration_open_date <= date.today() and instance.registration_close_date >= date.today()
            representation['reg_close'] = instance.registration_close_date < date.today()
        else:
            representation['reg_open'] = None
            representation['reg_close'] = None
        representation['remaining_slots'] = instance.max_participants - participants.count() if instance.max_participants else 0
        return representation

class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'



class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_id = self.context.get('user_id')
        register = Register.objects.filter(user=user_id).first()

        is_participated = Participant.objects.filter(tournament=instance, user=register).first()
        participants = Participant.objects.filter(tournament=instance)
        
        competition_ids = representation.get('competitions', [])

        current_competition = Competition.objects.filter(is_active=True, id__in=competition_ids).first()
        current_competition_serailzer = CompetitionSerializer(current_competition)

        representation['category'] = instance.category.name
        representation['stage'] = instance.stage.name
        representation['competition_type'] = 'tournament'
        representation['is_participated'] = True if is_participated else False
        representation['is_close'] = instance.end_date < date.today()
        representation['is_done'] = True if is_participated and (is_participated.file_uri or 'media' in is_participated.video.url) else False
        representation['reg_open'] = instance.registration_open_date <= date.today() and instance.registration_close_date >= date.today()
        representation['reg_close'] = instance.registration_close_date < date.today()
        representation['remaining_slots'] = instance.max_participants - participants.count()
        representation['competitions'] = current_competition_serailzer.data
        return representation

# class MyCompetitionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Participant
#         fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     user_id = self.context.get('user_id')
    #     is_participated = Participant.objects.filter(competition=instance, user=user_id).first()
    #     representation['category'] = instance.category.name
    #     representation['is_participated'] = True if is_participated else False
    #     representation['is_done'] = True if is_participated.file_uri else False
    #     representation['is_live'] = instance.start_date <= date.today()
    #     return representation
    