from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from oscar.core.application import Application


class StripeDashboardApplication(Application):
    name = None
    list_view = views.StripeTransactionListView
    detail_view = views.StripeTransactionDetailView

    def get_urls(self):
        urlpatterns = [url(r'^transactions/$', self.list_view.as_view(),
                                   name='stripe-transaction-list'),
                               url(r'^transactions/(?P<pk>\d+)/$', self.detail_view.as_view(),
                                   name='stripe-transaction-detail'),
                               ]
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, pattern):
        return staff_member_required


application = StripeDashboardApplication()
