from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        #here we write our code which we want to run before calling main function
        if request.user.is_authenticated:
            return redirect('store')
        else: 
            # this returning and runing the original function   
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

#Из-за того что нам надо передать параметр функции мы создаем функцию, 
# с именем, с каким будет вызыватся декоратор, и передаем аргумент, а сам 
# декоратор пишем внутри и называем простым именем
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = []
            
            if request.user.groups.exists():
                for i in request.user.groups.all():
                    group.append(i.name)
            
            for role in group:
                if role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            groups = []
            if request.user.groups.exists():
                for i in request.user.groups.all():
                    groups.append(i.name)
            
            if 'admin' in groups:
                return view_func(request, *args, **kwargs)
            
            else:
                return redirect('store')
        
        else:
            return redirect('store')
        
    return wrapper_func

