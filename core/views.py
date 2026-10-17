from django.shortcuts import redirect
def home(request):
    user = request.session.get('user')
    if user and user['role'] == 'librarian':
        return redirect('dashboard:index')
    return redirect('books:list')
