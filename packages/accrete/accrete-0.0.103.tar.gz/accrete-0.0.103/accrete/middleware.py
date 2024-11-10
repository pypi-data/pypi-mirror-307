from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponsePermanentRedirect
from accrete.tenant import set_tenant, set_member

from .models import Tenant


class TenantMiddleware(MiddlewareMixin):
    @staticmethod
    def get_tenant_id_from_request(request):
        if tenant := request.META.get('X-TENANT_ID'):
            tenant_id = tenant
        elif tenant_id := request.GET.get('tenant_id'):
            tenant_id = tenant_id
        elif tenant := request.COOKIES.get('tenant_id'):
            tenant_id = tenant
        else:
            tenant_id = None

        try:
            tenant_id = int(tenant_id)
        except (ValueError, TypeError):
            tenant_id = None

        return tenant_id

    def process_request(self, request):
        request.tenant = None
        request.member = None
        if request.path.startswith('/admin'):
            set_member(None)
            return

        if request.user.is_authenticated:
            memberships = request.user.memberships.filter(
                is_active=True,
                tenant__is_active=True
            )

            if request.user.is_staff:
                tenant_id = self.get_tenant_id_from_request(request)
                if not tenant_id:
                    tenant_id = memberships and memberships.first().tenant.pk
                request.tenant = tenant_id and Tenant.objects.filter(pk=tenant_id).first()
                request.member = request.tenant.members.filter(user=request.user).first()

            elif memberships and len(memberships) == 1:
                request.member = memberships.first()
                request.tenant = request.member.tenant
            elif memberships and len(memberships) > 1:
                tenant_id = self.get_tenant_id_from_request(request)
                if not tenant_id:
                    tenant_id = memberships.first().tenant.pk
                request.member = memberships.filter(tenant_id=tenant_id).first()
                request.tenant = request.member.tenant

        set_member(request.member)
        if request.user.is_staff:
            set_tenant(request.tenant)

        if request.POST and not request.POST.get('tenant') and request.tenant:
            request.POST = request.POST.copy()
            request.POST['tenant'] = request.tenant.pk

    @staticmethod
    def process_response(request, response):
        if request.tenant:
            response['X-TENANT_ID'] = request.tenant.id
            response.set_cookie(
                'tenant_id',
                request.tenant.pk,
                samesite=settings.SESSION_COOKIE_SAMESITE,
                max_age=31536000
            )
        return response


class HtmxRedirectMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        is_htmx = request.headers.get('HX-Request', 'false') == 'true'
        if not is_htmx:
            return response
        is_redirect = isinstance(response, HttpResponseRedirect)
        is_permanent_redirect = isinstance(response, HttpResponsePermanentRedirect)
        if is_redirect or is_permanent_redirect:
            response.status_code = 200
            header = 'HX-Location' if is_redirect else 'HX-Redirect'
            response[header] = response['Location']
        return response
