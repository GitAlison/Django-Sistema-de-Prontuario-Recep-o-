from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin

SEXO_CHOICE = [
    ('M','Masculino'),
    ('F','Feminino')
]

STATUS_CHOICE = [
    ('Desativado', 'DESATIVADO'),
    ('Ativado', 'ATIVADO'),

]

class Funcionario(models.Model):

    nome_completo = models.CharField('Nome Completo',max_length=80)
    sexo = models.CharField('Sexo',choices=SEXO_CHOICE,max_length=2)
    cpf = models.IntegerField('CPF',blank=True,null=True)
    rg = models.IntegerField('RG',blank=True,null=True)
    data_nascimento = models.DateField('Data Nascimento',blank=True,null=True)

    status = models.CharField('Status',max_length=11,choices=STATUS_CHOICE,blank=True,default='Ativado')
    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    def desativar(self):
        self.status='Desativado'
        self.save()

    def ativar(self):
        self.status='Ativado'
        self.save()

    def __str__(self):
        return self.nome_completo

    class Meta:
        ordering = ['-id']

class PacienteManager(models.Manager):

    def pesquisa(self,query):
        return self.get_queryset().filter(
            nome_completo__icontains=query)

class Paciente(models.Model):

    nome_completo = models.CharField('Nome Completo', max_length=80)
    sus = models.IntegerField('Cartão SUS',blank=True,null=True)
    sexo = models.CharField('Sexo',choices=SEXO_CHOICE,max_length=2)

    cpf = models.IntegerField('CPF', blank=True, null=True)
    rg = models.IntegerField('RG', blank=True, null=True)
    data_nascimento = models.DateField('Data Nascimento',blank=True,null=True)

    status = models.CharField('Status',max_length=11,choices=STATUS_CHOICE,blank=True,default='Ativado')
    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    objects = PacienteManager()

    def desativar(self):
        self.status = 'Desativado'
        self.save()

    def ativar(self):
        self.status = 'Ativado'
        self.save()


    def __str__(self):
        return str(self.nome_completo)
    class Meta:
        ordering = ['-id']

class Familia(models.Model):
    titular = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    agente = models.ForeignKey(Funcionario,on_delete=models.CASCADE,
                               blank=True,null=True)
    #endereço
    logradouro = models.CharField('Logradouro',max_length=90,blank=True,null=True)
    numero = models.CharField('Numero',max_length=10,blank=True,null=True)
    bairro = models.CharField('Bairro',max_length=20,blank=True,null=True)
    cidade = models.CharField('Cidade',max_length=30,blank=True,null=True)
    uf = models.CharField('UF',max_length=6,blank=True,null=True)
    complemento = models.TextField('Complemento',blank=True,null=True)

    status = models.CharField('Status',max_length=11,choices=STATUS_CHOICE,blank=True,default='Ativado')
    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ['-id']

class IntegranteManager(models.Manager):
    def pesquisa(self,query):
        return self.get_queryset().filter(
            paciente__nome_completo__icontains=query
        )
class IntegranteFamilia(models.Model):
    familia = models.ForeignKey(Familia,on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    objects = IntegranteManager()


class User(PermissionsMixin,AbstractBaseUser):

    username = models.CharField('Usuario',max_length=20,unique=True)
    email = models.EmailField('E-mail',unique=True)
    is_staff = models.BooleanField('É da equipe',default=False)

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    object = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username
