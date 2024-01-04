from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView

from accounts.models import *
from django.forms import ModelForm, ModelChoiceField, HiddenInput, CharField, EmailField, ImageField

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
    first_name = CharField(label='Jméno', max_length=64)
    last_name = CharField(label='Příjmení', max_length=64)
    email = EmailField()
    users_image = ImageField(required=False)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birth_date': SelectDateWidget(years=range(datetime.now().year, 1900, -1)),
            'user': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        users_image = self.cleaned_data.get('users_image')

        if users_image:
            user_image = UserImage(user=instance, image=users_image)
            user_image.save()

        if commit:
            instance.save()

        return instance


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileModelForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('profile')

    user_image = ImageField(required=False)

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

        user_image = self.request.FILES.get('users_image', None)
        if user_image:
            UserImage.objects.create(user=user.profile, image=user_image, description="Profilový obrázek")

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
    user_profile = Profile.objects.get(id=pk)
    images = UserImage.objects.filter(user=user_profile)
    context = {'profile': user_profile, 'images': images}
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        print(request.FILES)
        form = ProfileModelForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            print(request.POST)
            print(form.cleaned_data)
            user.save()
            print(request.POST)
            form.save()

            image_path = form.cleaned_data.get('users_image')
            print(image_path)
            user.refresh_from_db()
            user_pk = profile.pk
            print("Formulář je platný")
            return redirect(reverse('profile', kwargs={'pk': user_pk}))
        else:
            print(form.errors)
            print(request.POST)
            print(request.FILES)
            print("Chyby při ukládání do databáze:", form.non_field_errors())
    else:
        form = ProfileModelForm(instance=user.profile)

    context = {'form': form}
    return render(request, 'profile_edit.html', context)
