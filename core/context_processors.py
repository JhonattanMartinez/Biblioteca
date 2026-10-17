def session_user(request):
    return {'current_user': request.session.get('user')}
