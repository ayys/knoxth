
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    try:
        instance.token.delete()
    except: pass
    Token.objects.create(user=instance)
