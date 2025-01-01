from django.contrib import admin
from .models import Category, Competition, CompetitionMedia, Round, Tournament
from .forms import TournamentAdminForm


admin.site.register(Category)
admin.site.register(CompetitionMedia)
admin.site.register(Round)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    readonly_fields = ('file_uri',)

# @admin.register(Tournament)
# class TournamentAdmin(admin.ModelAdmin):
#     readonly_fields = ('file_uri',)

class TournamentAdmin(admin.ModelAdmin):
    form = TournamentAdminForm

admin.site.register(Tournament, TournamentAdmin)
