from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView


from .models import Profile


class ProfileChangeView(UpdateView):
    model = Profile
    fields = [
        'bio',
        'date_of_birth',
        'phone',
    ]
    template_name = 'profile/profile-change.html'

    def get_success_url(self):
        return reverse_lazy('profile')


class ProfileData(ListView):
    template_name = 'profile.html'
    context_object_name = 'element'

    def get_queryset(self):

        user = self.request.user.pk

        current_item = Profile.objects.filter(
            user_id=user
        ).first()

        return current_item

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data()

        return context
