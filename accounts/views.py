from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView

from accounts.models import *
from django.forms import ModelForm, ModelChoiceField, HiddenInput, CharField, EmailField, ImageField, \
    ModelMultipleChoiceField, CheckboxSelectMultiple

from viewer.models import Purchase


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
    first_name = CharField(label='Jméno', max_length=64, required=False)
    last_name = CharField(label='Příjmení', max_length=64, required=False)
    email = EmailField(required=False)
    users_image = ImageField(required=False)
    description = CharField(label='Popis obrázku', max_length=64, required=False)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)
    delete_images = ModelMultipleChoiceField(
        queryset=UserImage.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
        label='Smazat obrázky'
    )

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

        images_to_delete = self.cleaned_data.get('delete_images')

        if images_to_delete:
            UserImage.objects.filter(id__in=images_to_delete).delete()

        if commit:
            instance.save()

        return instance


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileModelForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('index')

    user_image = ImageField(required=False)

    def get_success_url(self):
        return reverse('index')

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
            obj, created = queryset.get_or_create(user=user_profile.user)
            return obj
        else:
            return queryset.create(user=self.request.user)


@login_required
def profile(request, pk):
    user_profile = Profile.objects.get(id=pk)
    images = UserImage.objects.filter(user=user_profile)
    purchases = Purchase.objects.filter(customer=request.user)
    context = {'profile': user_profile, 'images': images, 'purchases': purchases}
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile
    images = UserImage.objects.filter(user=profile)

    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')

            user.save()
            form.save()
            user.refresh_from_db()
            user_pk = profile.pk
            return redirect(reverse('profile', kwargs={'pk': user_pk}))
    else:
        form = ProfileModelForm(instance=user.profile, initial={
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'email': user.email
        })

    context = {'form': form, 'images': images}
    return render(request, 'profile_edit.html', context)
