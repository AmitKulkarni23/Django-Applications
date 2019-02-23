from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course
from .forms import CourseForm

# base View Class = View


class CourseListView(View):
    template_name = "courses/course_list.html"
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)


class CourseView(View):
    # One advantage is you can the change the templates on teh fly
    template_name = "courses/course_detail.html"

    def get(self, request, id = None, *args, **kwargs):
        """
        Function based view
        :param request: The HTTP request object
        :return: The rendered template along with the context
        """
        context = {}
        if id:
            context["object"] = get_object_or_404(Course, id=id)
        return render(request, self.template_name, context)


class CourseCreateView(View):

    template_name = "courses/course_create.html"

    def get(self, request, *args, **kwargs):
        """
        Function based view
        :param request: The HTTP request object
        :return: The rendered template along with the context
        """
        form = CourseForm()
        context = {"form" : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Function based view
        :param request: The HTTP request object
        :return: The rendered template along with the context
        """
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            form = CourseForm()

        context = {"form": form}
        return render(request, self.template_name, context)