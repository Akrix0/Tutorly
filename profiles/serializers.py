from django.db import transaction

from rest_framework import serializers

from .models import TutorSubject, Availability, TutorCard
from core import exceptions, utils

class TutorSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorSubject
        fields = ["subject", "price_per_hour", "currency"]

class AvailabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Availability
        fields = ["weekday", "start_time", "end_time"]

class TutorProfileCreateSerializer(serializers.ModelSerializer):
    subjects = TutorSubjectSerializer(many=True)
    availabilities = AvailabilitySerializer(many=True)

    class Meta:
        model = TutorCard
        fields = ["birth_date", "experience_years", "country", "subjects", "availabilities"]

    def validate(self, attrs):
        age = utils.get_age(attrs["birth_date"])
        if attrs["experience_years"] >= age - 12:
            raise exceptions.InvalidDataError("experience_years")

        if age <= 14:
            raise exceptions.TooYoungError()

        availabilities = attrs["availabilities"]
        for i in range(len(availabilities)):
            first = availabilities[i]
            for j in range(i + 1, len(availabilities)):
                second = availabilities[j]
                if first["weekday"] == second["weekday"]:
                    if utils.check_overlap(first["start_time"], first["end_time"], second["start_time"], second["end_time"]):
                        raise exceptions.TimeIntervalsOverlapError()

        for availability in availabilities:
            if availability["start_time"] >= availability["end_time"]:
                raise exceptions.InvalidTimeRangeError()

        subjects = attrs["subjects"]
        for i in range(len(subjects)):
            first = subjects[i]
            for j in range(i + 1, len(subjects)):
                second = subjects[j]
                if first["subject"] == second["subject"]:
                    raise exceptions.DuplicateSubjectsError()

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        subjects = validated_data.pop("subjects")
        availabilities = validated_data.pop("availabilities")
        tutor_card = TutorCard.objects.create(**validated_data)
        for subject in subjects:
            TutorSubject.objects.create(tutor_card=tutor_card, **subject)
        for availability in availabilities:
            Availability.objects.create(tutor_card=tutor_card, **availability)
        return tutor_card