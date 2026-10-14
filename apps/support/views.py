"""
Views for the Support app: Help Center FAQ, Support Tickets, and Customer Feedback Reviews.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.core.mixins import AjaxResponseMixin, OwnerRequiredMixin
from apps.support.forms import SupportTicketForm, TicketReviewForm
from apps.support.models import FAQ, SupportTicket


class FAQListView(ListView):
    """
    Frequently Asked Questions & Help Center (Screen 17).
    Uses native HTML5 <details> and <summary> disclosure elements.
    """

    model = FAQ
    template_name = "support/faq.html"
    context_object_name = "faqs"

    def get_queryset(self):
        qs = FAQ.objects.filter(is_published=True).order_by("category", "order")
        search = self.request.GET.get("q")
        if search:
            st = search.strip()
            qs = qs.filter(question__icontains=st) | qs.filter(answer__icontains=st)
        return qs


class SupportTicketListView(LoginRequiredMixin, ListView):
    """
    Client's Support Tickets List (Screen 16a).
    """

    model = SupportTicket
    template_name = "support/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 15

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by("-created_at")


class SupportTicketDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    """
    Support Ticket Detail View (Screen 16b).
    """

    model = SupportTicket
    template_name = "support/ticket_detail.html"
    context_object_name = "ticket"
    owner_field = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = TicketReviewForm()
        context["existing_reviews"] = self.object.reviews.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = self.object
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your rating and feedback!")
            return redirect("support:detail", pk=self.object.pk)
        context = self.get_context_data(review_form=form)
        return self.render_to_response(context)


class SupportTicketCreateView(LoginRequiredMixin, AjaxResponseMixin, CreateView):
    """
    Create a new Support Ticket (Screen 16c & Section 5).
    """

    model = SupportTicket
    form_class = SupportTicketForm
    template_name = "support/ticket_create.html"
    success_url = reverse_lazy("support:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = SupportTicket.TicketStatus.OPEN
        messages.success(
            self.request,
            "Your support ticket has been submitted! Our support team will respond shortly.",
        )
        return super().form_valid(form)
