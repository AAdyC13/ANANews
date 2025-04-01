from django.shortcuts import render

def base(request):
    return render(request,
                  'app_advanced_search/adv_base.html')
    
def user_interest(request):
    return render(request,
                  'app_advanced_search/user_interest.html')