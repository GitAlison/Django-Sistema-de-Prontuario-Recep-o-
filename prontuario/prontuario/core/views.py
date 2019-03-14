from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,View,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

class Index(LoginRequiredMixin,View):

    def get(self,request):
        template_name = 'index.html'
        familias = Familia.objects.all().count()
        funcionarios = Funcionario.objects.all().count()
        pacientes = Paciente.objects.all().count()
        contexto ={
            'pacientes':pacientes,
            'funcionarios': funcionarios,
            'familias':familias
        }
        return render(request,template_name,contexto)


class Funcionarios(LoginRequiredMixin,ListView):
    template_name = 'funcionario/funcionario_list.html'
    model = Funcionario

class FuncionarioCreate(CreateView):
    template_name = 'funcionario/funcionario_form.html'
    form_class = FuncionarioForm

    def get_success_url(self):
        messages.success(self.request, 'Registrado com sucesso')
        return reverse_lazy('core:funcionarios-list')


class FuncionarioUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'funcionario/funcionario_form.html'
    model = Funcionario
    form_class = FuncionarioForm

    def get_success_url(self):
        messages.success(self.request, 'Atualizado com sucesso')
        return reverse_lazy('core:funcionarios-list')

class FuncionarioDesativar(LoginRequiredMixin,View):
    def get(self,request,pk):
        messages.success(request, 'Desativado com sucesso')
        funcionario = Funcionario.objects.get(id=pk)
        funcionario.desativar()
        return redirect('core:funcionarios-list')


class FuncionarioAtivar(LoginRequiredMixin,View):
    def get(self,request,pk):
        messages.success(self.request, 'Ativado com sucesso')
        funcionario = Funcionario.objects.get(id=pk)
        funcionario.ativar()
        return redirect('core:funcionarios-list')

class PacienteDesativar(LoginRequiredMixin,View):
    def get(self,request,pk):
        messages.success(request, 'Desativado com sucesso')
        funcionario = Paciente.objects.get(id=pk)
        funcionario.desativar()
        return redirect('core:pacientes-list')


class PacienteAtivar(LoginRequiredMixin,View):
    def get(self,request,pk):
        messages.success(self.request, 'Ativado com sucesso')
        paciente = Paciente.objects.get(id=pk)
        paciente.ativar()
        return redirect('core:pacientes-list')

class BuscaPaciente(LoginRequiredMixin,View):

    def get(self,request):
        template_name='buscas/busca_paciente.html'
        return render(request,template_name)
    def post(self,request):
        template_name='buscas/busca_paciente.html'
        paciente = Paciente.objects.pesquisa(request.POST['pesquisa'])
        contexto = {'resultado':paciente,}
        return render(request,template_name,contexto)

class Pacientes(LoginRequiredMixin,ListView):
    template_name = 'paciente/paciente_list.html'
    model = Paciente

class PacienteCreate(LoginRequiredMixin,CreateView):
    template_name = 'paciente/paciente_form.html'
    form_class = PacienteForm

    def get_success_url(self):
        messages.success(self.request, 'Registrado com sucesso')
        return reverse_lazy('core:pacientes-list')


class PacienteUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'paciente/paciente_form.html'
    model = Paciente
    form_class = PacienteForm

    def get_success_url(self):
        messages.success(self.request, 'Atualizado com sucesso')
        return reverse_lazy('core:pacientes-list')


class Familias(LoginRequiredMixin,ListView):
    template_name = 'familia/familia_list.html'
    model = Familia

class FamiliaCreate(LoginRequiredMixin,View):
    def get(self,request):
        familia_form = FamiliaForm(request.POST or None)
        integrante_form = IntegranteFamiliaForm(request.POST or None)
        template_name = 'familia/familia_form.html'
        contexto = {'form':familia_form}
        return render(request,template_name,contexto)
    def post(self,request):
        familia_form = FamiliaForm(request.POST)
        if familia_form.is_valid():
            familia_form.save()
            messages.success(request,'Criado insira as Proximas informações')
            return redirect('core:familia-update',familia_form.instance.pk)

        template_name='familia/familia_form.html'
        contexto = {'form':familia_form}
        return render(request,template_name,contexto)
####
class FormulariosCreate(View):
    def get(self,request):
        placa_form = PlacaForm(request.POST or None)
        registro_form = RegistroForm(request.POST or None)
        template_name = 'formulario.html'
        contexto = {'placa_form':placa_form,
                    'registro_form': registro_form}
        return render(request,template_name,contexto)
    def post(self,request):
        placa_form = PlacaForm(request.POST)
        registro_form = RegistroForm(request.POST )
        if placa_form.is_valid():
            placa_form.save()
            messages.success(request,'Criado ')
            return redirect('core:placa-list')

        if registro_form.is_valid():
            registro_form.save()
            messages.success(request,'Criado')
            return redirect('core:placa-list')

        template_name='familia/familia_form.html'
        contexto = {'form':familia_form}
        return render(request,template_name,contexto)

###

class FamiliaUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'familia/familia_form.html'
    model = Familia
    form_class = FamiliaForm

    def get_context_data(self, **kwargs):
        context = super(FamiliaUpdate, self).get_context_data(**kwargs)
        context['form_integ'] = IntegranteFamiliaForm()
        return context

    def get_success_url(self):
        messages.success(self.request, 'Atualizado com sucesso')
        return reverse_lazy('core:familias-list')

class AdicionarIntegrante(LoginRequiredMixin,CreateView):
    model = IntegranteFamilia
    form_class = IntegranteFamiliaForm
    template_name = 'familia/familia_form.html'

    def get_success_url(self):
        return reverse_lazy('core:familia-update', kwargs={'pk': self.object.familia.id})

class DeleteIntegrante(LoginRequiredMixin,View):
    def get(self,request,pk):
        integrante = IntegranteFamilia.objects.get(id=pk)
        integrante.delete()
        messages.success(request,'Deletado com sucesso')
        
        return redirect('core:familia-update',integrante.familia.pk)

        

class BuscaProntuario(LoginRequiredMixin,View):

    def get(self,request):
        template_name='buscas/busca_prontuario.html'
        return render(request,template_name)
    def post(self,request):
        template_name='buscas/busca_prontuario.html'

        integrante = IntegranteFamilia.objects.pesquisa(request.POST['pesquisa'])

        familia_list = []
        for inte in integrante:
            #resultado =  Familia.objects.get(id=int(familia))
            if not inte.familia in familia_list:
                familia_list.append(inte.familia)
            print(familia_list)
        contexto = {'resultado':integrante,
                    'familia_list':familia_list}

        return render(request,template_name,contexto)


class Register(View):

    def get(self,request):
        template_name = 'conta/novo-usuario.html'
        form = RegisterForm(request.POST or None)
        contexto = {
            'form':form
        }
        return render(request,template_name,contexto)


    def post(self, request):
        template_name = 'conta/novo-usuario.html'
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'Novo Usuario registrado')
        contexto = {
            'form': form
        }
        return render(request, template_name, contexto)