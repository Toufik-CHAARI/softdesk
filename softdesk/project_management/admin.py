from django.contrib import admin


from project_management.models import Project, Contributor, Issue, Comment
# Register your models here.

class ProjectAdmin(admin.ModelAdmin): 
    list_display = ("name", "description", "project_type","author")

admin.site.register(Project, ProjectAdmin)

class ContributorAdmin(admin.ModelAdmin): 
    list_display = ("user", "project")

admin.site.register(Contributor, ContributorAdmin)

class IssueAdmin(admin.ModelAdmin): 
    list_display = ("name", "status","priority","author","project")

admin.site.register(Issue, IssueAdmin)


class CommentAdmin(admin.ModelAdmin): 
    list_display = ("issue", "author","uuid")

admin.site.register(Comment, CommentAdmin)
    
