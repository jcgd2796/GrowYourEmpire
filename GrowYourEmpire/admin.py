from django.contrib import admin
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.contrib.auth.models import User as User
from .models import Test, Subject, Option, Question, TestResolution, Village, Activity, Attack, TradeOffer,New, Upgrade, Training, Bonus,Student,God,Event,DonationEvent,Suggestion
# Register your models here.

admin.site.register(TestResolution)
admin.site.register(Village)
admin.site.register(Activity)
admin.site.register(Attack)
admin.site.register(TradeOffer)
admin.site.register(Upgrade)
admin.site.register(Training)
admin.site.register(Bonus)
admin.site.register(New)
admin.site.register(Subject)
admin.site.register(God)
admin.site.register(Suggestion)

class OptionInline(NestedTabularInline):
    model = Option

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        OptionInline
    ]

@admin.register(Test)
class TestAdmin(NestedModelAdmin):
    inlines = [
        QuestionInline,
    ]


class VillageInline(admin.StackedInline):
    model = Village

@admin.register(Student)
class TestAdmin(admin.ModelAdmin):
    inlines = [
        VillageInline,
    ]

class DonationEventInline(admin.StackedInline):
    model = DonationEvent

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [
        DonationEventInline,
    ]