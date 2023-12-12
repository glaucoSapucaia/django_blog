from site_setup import models

def context(request):
    setup = models.SiteSetup.objects.order_by('-id').first
    return {
        'setup': setup,
    }