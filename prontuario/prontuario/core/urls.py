from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth
from . import views

app_name='core'
urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('login',auth.LoginView.as_view(template_name='conta/login.html'),name='login'),
    path('logout',auth.LogoutView.as_view(next_page='core:index'),name='logout'),
    path('registro',views.Register.as_view(),name='registro'),
    path('senha',auth.PasswordChangeView.as_view(
        template_name='conta/mudar_senha.html',
        success_url=reverse_lazy('core:index')
    ),name='mudar-senha'),
    #Funcioanarios
    path('funcionarios/',views.Funcionarios.as_view(),name='funcionarios-list'),
    path('funcionario-create/', views.FuncionarioCreate.as_view(), name='funcionario-create'),
    path('funcionario-desativar/<int:pk>/', views.FuncionarioDesativar.as_view(), name='funcionario-desativar'),
    path('funcionario-ativar/<int:pk>/', views.FuncionarioAtivar.as_view(), name='funcionario-ativar'),
    path('funcionario-update/<int:pk>/', views.FuncionarioUpdate.as_view(), name='funcionario-update'),
    #Pacientes
    path('pacientes/', views.Pacientes.as_view(), name='pacientes-list'),
    path('paciente-create/', views.PacienteCreate.as_view(), name='paciente-create'),
    path('paciente-ativar/<int:pk>/', views.PacienteAtivar.as_view(), name='paciente-ativar'),
    path('paciente-desativar/<int:pk>/', views.PacienteDesativar.as_view(), name='paciente-desativar'),
    path('paciente-update/<int:pk>/', views.PacienteUpdate.as_view(), name='paciente-update'),
    #Familias
    path('familias/', views.Familias.as_view(), name='familias-list'),
    path('familia-create/', views.FamiliaCreate.as_view(), name='familia-create'),
    path('familia-update/<int:pk>/', views.FamiliaUpdate.as_view(), name='familia-update'),
    #path('familia-delete/<int:pk>/', views.FamiliaDelete.as_view(), name='familia-delete'),

    path('adicionar_integrante/',views.AdicionarIntegrante.as_view(),name='add-integrante'),
    path('delete_integrante/<int:pk>', views.DeleteIntegrante.as_view(), name='delete-integrante'),
    #Pesquisa
    path('busca-prontuario/',views.BuscaProntuario.as_view(),name="busca-prontuario"),
    path('busca-paciente/', views.BuscaPaciente.as_view(), name="busca-paciente"),

]
