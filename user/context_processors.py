from .forms import LoginForm

#登录界面弹窗
def login_modal_form(request):
    return {'login_modal_form': LoginForm()}
    