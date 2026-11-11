# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages

# from .models import Appliance
# from .forms import ApplianceForm


# @login_required
# def dashboard(request):

#     appliances = Appliance.objects.filter(
#         owner=request.user
#     ).order_by('-created_at')

#     total = appliances.count()

#     active = sum(
#         a.warranty_status == 'Active'
#         for a in appliances
#     )

#     expiring = sum(
#         a.warranty_status == 'Expiring Soon'
#         for a in appliances
#     )

#     expired = sum(
#         a.warranty_status == 'Expired'
#         for a in appliances
#     )

#     context = {
#         'appliances': appliances,
#         'total': total,
#         'active': active,
#         'expiring': expiring,
#         'expired': expired,
#     }

#     return render(
#         request,
#         'dashboard.html',
#         context
#     )


# @login_required
# def add_appliance(request):

#     if request.method == 'POST':

#         form = ApplianceForm(
#             request.POST,
#             request.FILES
#         )

#         if form.is_valid():

#             appliance = form.save(commit=False)
#             appliance.owner = request.user
#             appliance.save()

#             messages.success(
#                 request,
#                 'Appliance added successfully!'
#             )

#             return redirect('dashboard')

#     else:
#         form = ApplianceForm()

#     return render(
#         request,
#         'appliance_form.html',
#         {'form': form}
#     )


# @login_required
# def delete_appliance(request, pk):

#     appliance = get_object_or_404(
#         Appliance,
#         pk=pk,
#         owner=request.user
#     )

#     if request.method == 'POST':
#         appliance.delete()

#         messages.success(
#             request,
#             'Appliance deleted successfully!'
#         )

#     return redirect('dashboard')


# def register(request):

#     if request.method == 'POST':

#         form = UserCreationForm(request.POST)

#         if form.is_valid():

#             user = form.save()
#             login(request, user)

#             return redirect('dashboard')

#     else:
#         form = UserCreationForm()

#     return render(
#         request,
#         'registration/register.html',
#         {'form': form}
#     )



from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q

from .models import Appliance
from .forms import ApplianceForm


@login_required
def dashboard(request):

    all_appliances = Appliance.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "")
    selected_status = request.GET.get("status", "")

    total = all_appliances.count()
    active = 0
    expiring = 0
    expired = 0
    total_spend = 0

    category_expenses = defaultdict(float)

    for appliance in all_appliances:

        status = appliance.warranty_status

        if status == "Active":
            active += 1
        elif status == "Expiring Soon":
            expiring += 1
        else:
            expired += 1

        total_spend += appliance.price
        category_expenses[appliance.category] += float(appliance.price)

    appliances = all_appliances

    if search_query:
        appliances = appliances.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model_number__icontains=search_query)
        )

    if selected_category:
        appliances = appliances.filter(
            category=selected_category
        )

    if selected_status in ["Active", "Expiring Soon", "Expired"]:
        appliances = [
            appliance for appliance in appliances
            if appliance.warranty_status == selected_status
        ]

    context = {
        "appliances": appliances,
        "total": total,
        "active": active,
        "expiring": expiring,
        "expired": expired,
        "total_spend": total_spend,
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_status": selected_status,
        "categories": Appliance.CATEGORY_CHOICES,
        "chart_labels": list(category_expenses.keys()),
        "chart_values": list(category_expenses.values()),
    }

    return render(request, "dashboard.html", context)


@login_required
def add_appliance(request):

    if request.method == "POST":

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
                "Appliance added successfully!"
            )

            return redirect("dashboard")

    else:
        form = ApplianceForm()

    return render(
        request,
        "appliance_form.html",
        {"form": form}
    )


@login_required
def delete_appliance(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":

        appliance.delete()

        messages.success(
            request,
            "Appliance deleted successfully!"
        )

    return redirect("dashboard")


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Registration successful!"
            )

            return redirect("dashboard")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )
