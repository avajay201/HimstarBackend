# serializers.py
from rest_framework import serializers
from .models import Category, Round, Tournament
from video.models import Participant
from payments.models import PaymentDetails
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
        if is_participated and is_participated.temp_video:
            representation['temp_video'] = is_participated.temp_video.url
        representation['stage'] = instance.stage.name if instance.stage else None
        if instance.competition_type == 'competition':
            representation['is_close'] = instance.end_date < date.today()
        representation['is_done'] = True if is_participated and (is_participated.file_uri or (is_participated.video and 'media' in is_participated.video.url)) else False
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


        current_competition = instance.competitions.filter(is_active=True).first()
        print('current_competition>>>>', current_competition)
        is_participated = Participant.objects.filter(competition=current_competition, user=register).first()
        participants = Participant.objects.filter(competition=current_competition)
        current_competition_serailzer = CompetitionSerializer(current_competition)

        payment = PaymentDetails.objects.filter(user=register, tournament=instance).first()

        representation['category'] = instance.category.name
        # representation['stage'] = instance.stage.name
        representation['competition_type'] = 'tournament'
        # representation['is_participated'] = True if is_participated else False
        representation['is_participated'] = True if is_participated else False
        if is_participated and is_participated.temp_video:
            representation['temp_video'] = is_participated.temp_video.url
        representation['is_close'] = instance.end_date < date.today()
        representation['is_done'] = True if is_participated and ((is_participated.file_uri or (is_participated.video and 'media' in is_participated.video.url)) and is_participated.is_paid) else False
        representation['reg_open'] = current_competition.registration_open_date <= date.today() and current_competition.registration_close_date >= date.today()
        representation['reg_close'] = current_competition.registration_close_date < date.today()
        representation['remaining_slots'] = instance.max_participants - participants.count()
        representation['is_paid'] = True if payment else False
        representation['competition'] = current_competition_serailzer.data
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
    