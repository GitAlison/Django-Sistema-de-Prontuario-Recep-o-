from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control',
                                                      'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control ', }),
        }


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control',
                                                      'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control ',}),
        }



class FamiliaForm(forms.ModelForm):

    class Meta:
        model = Familia
        fields = '__all__'
        widgets = {
            'titular': forms.Select(attrs={'class':'form-control select2'}),
            'agente': forms.Select(attrs={'class': 'form-control select2'}),
            'complemento': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class IntegranteFamiliaForm(forms.ModelForm):

    class Meta:
        model = IntegranteFamilia
        fields = '__all__'
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control select2'}),
            'familia': forms.Select(attrs={'class': 'form-control select2'}),
        }

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Senha',widget = forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha',widget = forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password1 and password1 != password2:
            raise forms.ValidationError('Senhas Não conferem')
        else:
            return password1

    def save(self, commit=True):
        user = super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username','email']