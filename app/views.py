from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
def home(request):
    return render(request,'home.html')


@login_required(login_url='/login/') 
def dashboard(request):
    user = request.user

    if user.userprofile.role == 'student':
        try:
            enrollments = Enrollment.objects.filter(user=user)
            updates = StudentUpdate.objects.filter(user=user)
            
            context = {
                "enrollments" : enrollments,
                'updates' : updates
            }
            return render(request, 'dashboard_student.html',context)
        except:
            return HttpResponse("profile not found")
        

    elif user.userprofile.role == 'teacher':
        
        courses = Course.objects.filter(user=request.user)
            
        context = {
            "courses": courses
        }
        return render(request, 'dashboard_teacher.html',context)
        
       

    else:
        
        return HttpResponse("profile not found")

@login_required(login_url='/login/')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('dashboard_teacher')
@login_required(login_url='/login/') 
def profile(request):
    user = request.user

    if user.userprofile.role == 'student':
        try:
            user = UserProfile.objects.get(user=user)
            context = {
                'user': user
            }
            return render(request, 'profile.html', context)
        except:
            return HttpResponse("profile not found")
        

    elif user.userprofile.role == 'teacher':
        try:
            user = UserProfile.objects.get(user=user)
            context = {
                'user': user
            }
            return render(request, 'profile.html',context)
        except:
            return HttpResponse("profile not found")
        

    else:
        
        return HttpResponse("profile not found")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            login(request, user)
            
            return redirect('/dashboard')  
        else:
            
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
      
        username = request.POST['email']
        first_name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']

        # Perform any additional validation or processing here
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password1,first_name=first_name)
        
        # Create a user profile
        profile = UserProfile(user=user, role=user_type)
        profile.save()
        
        return redirect('login') 

       

    return render(request, 'signup.html')
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required(login_url='/login/') 
def create_course(request):
    user = request.user

    
    if request.method == 'POST':
        if user.userprofile.role == 'teacher':
            title = request.POST.get('course-title')
            description = request.POST.get('course-description')
            category = request.POST.get('category')
            schedule = request.POST.get('course-schedule')
            
            course = Course.objects.create(
                user=user, 
                title=title,
                description=description,
                category=category,
                schedule=schedule
            )

            
            return redirect('dashboard')

    return render(request, 'Createcourse.html')
@login_required(login_url='/login/')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('dashboard')
def view_course(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    feedbacks = Feedback.objects.filter(course=course)
    context = {
        'course': course,
        'feedbacks': feedbacks,
    }
    return render(request, 'view_course.html', context)

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        courses = Course.objects.filter(title__icontains=query)
        context = {
            'courses': courses
        }
        return render(request, "search.html", context)
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request,"search.html",context)
@login_required(login_url='/login/')
def forum(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        user = request.user
        post = Forum_post.objects.create(user=user, description=description)
        post.save()
        return redirect('forum')
    context = {
        'posts': Forum_post.objects.all()
    }
    return render(request, "forum.html",context)
@login_required(login_url='/login/')
def feedback_support(request,course_id):
    if request.method == 'POST':
        name = request.POST.get('your-name')
        description = request.POST.get('your-feedback')
        course = get_object_or_404(Course, id=course_id)
        user = request.user
        feedback = Feedback.objects.create(course=course, user=user, name=name, description=description)
        feedback.save()
        return redirect(f'/view_course/{course_id}/')
    context = {
        'courses': Course.objects.all(),
        "course_id": course_id
    }
    return render(request, "feedback_support.html", context)
@login_required(login_url='/login/')
def enroll_now(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    enrollment = Enrollment.objects.create(user=user, course=course)
    enrollment.save()
    # Create a notification for the teacher
    teacher = course.user 
    Notification.objects.create(
        user=teacher,
        message=f'New student {user.first_name} enrolled in your course "{course.title}".'
    )
    return redirect('dashboard')

def upload_material(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        title = request.POST.get('material-title')
        content = request.POST.get('material-content')
        file = request.FILES.get('material-file')
        print(title, content, file)
        # if not (title and content and file):
        #     return HttpResponseBadRequest("Invalid data. Make sure all fields are filled.")

        material = Material.objects.create(
            course=course,
            title=title,
            content=content,
            file=file
        )
        # Create notification for each student enrolled in the course
        enrolled_students = Enrollment.objects.filter(course=course)
        for enrollment in enrolled_students:
            Notification.objects.create(
                user=enrollment.user,
                message=f'New material "{material.title}" added to the course "{course.title}".'
            )

        return redirect(f"/view_course/{course.id}/")  # Redirect to course detail page

    return render(request, 'Uploadmaterial.html', {'course_id': course_id})
def view_students(request, course_id):
    course = Course.objects.get(id=course_id)
    students = Enrollment.objects.filter(course=course)  # Assuming you have a 'students' field in your Enrollment model
      # Assuming you have a related name 'students' in your Course model
    return render(request, 'view_students.html', {'course': course, 'students': students})
def view_profile(request, id):
    user = UserProfile.objects.get(id=id)
    return render(request, 'profile.html', {'user': user})
def view_material(request, course_id):
    course = Course.objects.get(id=course_id)
    materials = Material.objects.filter(course=course)
    return render(request, 'view_material.html', {'course': course, 'materials': materials})
def removeenrollment(request,id):
    
    obj = Enrollment.objects.get(id=id)
    course_id = obj.course.id
    obj.delete()
    return redirect(f'/students/{course_id}/')
def usersearch(request):
    if request.method == 'POST':
        query = request.POST['query']
        users = User.objects.filter(first_name__icontains=query)
        
        context = {
            'users': users
        }
        return render(request, "usersearch.html", context)
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, "usersearch.html", context)
@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': user_notifications})
@login_required(login_url='/login/') 
def writeupdates(request):
    if request.method == 'POST':
        
        content = request.POST.get('update')
        user = request.user
        update = StudentUpdate.objects.create(user=user, content=content)
        update.save()
        return redirect('dashboard')
    return render(request, 'studentsupdates.html')

def deleteupdate(request,id):
    update = StudentUpdate.objects.get(id=id)
    update.delete()
    return redirect('dashboard')