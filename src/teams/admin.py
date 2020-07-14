from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

from .models import Team, Availability
from import_export import resources

class TeamResource(resources.ModelResource):

    class Meta:
        model = Team
        fields = ('id','team_name', 'classification','organization', 'scores')


class TeamCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Team
        fields = ('team_name','classification','organization',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        team = super().save(commit=False)
        team.set_password(self.cleaned_data['password1'])
        if commit:
            team.save()
        return team


class TeamChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))
    
    class Meta:
        model = Team
        exclude = ('password',)
    
    def save(self, commit=True):
        team = super(TeamChangeForm, self).save(commit=False)
        tasks_solved = self.cleaned_data['tasks_solved'].all()
        scores = sum([task.cost for task in tasks_solved])
        team.scores = scores
        if commit:
            team.save()
        return team


class TeamAdmin(BaseUserAdmin, ImportExportModelAdmin):
    form = TeamChangeForm
    add_form = TeamCreationForm

    list_display = ('team_name', 'classification', 'organization', 'is_admin', 'scores')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('team_name', 'password')}),
        ('Team info', {'fields': ('classification','organization', 'tasks_solved', 'scores', 'last_complete_date')}),
        ('Permissions', {'fields': ('is_admin',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('team_name', 'password1', 'password2', 'classification', 'organization'),
        }),
    )
    search_fields = ('team_name', 'organization')
    ordering = ('scores',)
    filter_horizontal = ('tasks_solved',)
    resource_class = TeamResource

admin.site.register(Team, TeamAdmin)
admin.site.register(Availability)
admin.site.unregister(Group)
