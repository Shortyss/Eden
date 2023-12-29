from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView

from accounts.models import *


# Create your views here.


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': ('Uživatelské jméno'),
            'first_name': ('Jméno'),
            'last_name': ('Příjmení'),
            'email': ('E-mail'),
            'password1': ('Heslo'),
            'password2': ('Potvrzení hesla'),
        }


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'


class ProfileModelForm(ModelForm):
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birth_date': SelectDateWidget(years=range(datetime.now().year, 1900, -1)),
            'user': HiddenInput(),
        }

    ProfileImage = ImageField(upload_to='users_image/')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileModelForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.user.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        result = super().form_valid(form)
        return result

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        user_profile = getattr(self.request.user, 'profile', None)
        if user_profile:
            obj = get_object_or_404(queryset, user=user_profile.user)
            return obj
        else:
            raise Http404("Profil neexistuje")


@login_required
def profile(request, pk):

    user_profile = request.user.profile
    images = UserImage.objects.filter(user=user_profile)
    context = {'profile': user_profile, 'images': images}
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileModelForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.refresh_from_db()
            user_pk = user.pk
            return redirect(reverse('profile', kwargs={'pk': user_pk}))
    else:
        form = ProfileModelForm(instance=user.profile)

    context = {'form': form}
    return render(request, 'profile_edit.html', context)
