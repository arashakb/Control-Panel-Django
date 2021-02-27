from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func
    return decorator
def teacher_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'student':
			return redirect('student_panel')

		if group == 'teacher':
			return view_func(request, *args, **kwargs)

	return wrapper_function