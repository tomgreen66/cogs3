from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from project.models import Project, ProjectUserMembership


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.has_perm('project.change_projectusermembership'):
            num_requests = ProjectUserMembership.objects.awaiting_authorisation(user).count()
            context['project_user_requests_count'] = num_requests

        if user.has_perm('project.add_project'):
            num_requests = Project.objects.awaiting_approval(user).count()
            context['project_application_count'] = num_requests

        # Which projects does the user have a valid project user membership record?
        context['project_codes'] = ProjectUserMembership.objects.filter(
            user=user,
            status=ProjectUserMembership.AUTHORISED,
        ).values_list('project__code', flat=True)

        # If the user is a tech lead, what is their latest project?
        try:
            context['latest_project_code'] = Project.objects.filter(
                tech_lead=user,
                status=Project.APPROVED,
            ).latest().code
        except Project.DoesNotExist:
            pass

        return context
