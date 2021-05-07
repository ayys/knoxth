class KnoxthLoginView(KnoxLoginView):
    '''
    The Login view has to be authenticated with the authorization code
    acquired via DRF.
    '''
    authentication_classes = [DRFTokenAuthentication]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    try:
        instance.token.delete()
    except: pass
    Token.objects.create(user=instance)
