from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, RedirectView


from .models import Group, GroupMember

# Create your views here.
class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description')
    model = Group
    
class SingleGroup(DetailView):
    model = Group
    
class ListGroup(ListView):
    model = Group
    
class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
        
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request, ('Warning! Already a member'))
        else:
            messages.success(self.request, ('You are now a member of {}'.format(group.name)))
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:list_group')
        
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            GroupMember.objects.filter(
                group__pk__iexact = group.pk
            ).get().delete()
        except:
            messages.warning(self.request, ('You are not a member of {}'.format(group.name)))
        else:
            messages.success(self.request, ('You are no longer a member of {}'.format(group.name)))
            
        return super().get(request, *args, **kwargs)
    
    
    
    
    
    
    
    
    