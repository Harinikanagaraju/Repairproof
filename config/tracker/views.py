from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Appliance
from .forms import ApplianceForm


@login_required
def dashboard(request):

    appliances = Appliance.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    total = appliances.count()

    active = sum(
        a.warranty_status == 'Active'
        for a in appliances
    )

    expiring = sum(
        a.warranty_status == 'Expiring Soon'
        for a in appliances
    )

    expired = sum(
        a.warranty_status == 'Expired'
        for a in appliances
    )

    context = {
        'appliances': appliances,
        'total': total,
        'active': active,
        'expiring': expiring,
        'expired': expired,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


@login_required
def add_appliance(request):

    if request.method == 'POST':

        form = ApplianceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            appliance = form.save(commit=False)
            appliance.owner = request.user
            appliance.save()

            messages.success(
                request,
                'Appliance added successfully!'
            )

            return redirect('dashboard')

    else:
        form = ApplianceForm()

    return render(
        request,
        'appliance_form.html',
        {'form': form}
    )


@login_required
def delete_appliance(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        appliance.delete()

        messages.success(
            request,
            'Appliance deleted successfully!'
        )

    return redirect('dashboard')


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )