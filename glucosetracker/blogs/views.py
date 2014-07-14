from django.views.generic.base import ContextMixin
from django.views.generic import DetailView, ListView

from .models import Blog


class BlogBaseView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BlogBaseView, self).get_context_data(**kwargs)
        context['recent_blog_list'] = Blog.objects.recent_posts()

        return context


class BlogDetailView(DetailView, BlogBaseView):
    model = Blog

    def get_queryset(self):
        """
        Only return the object if status is 'published', unless the user is
        a superuser.
        """
        if self.request.user.is_authenticated() and \
                self.request.user.is_superuser:
            return Blog.objects.all()
        else:
            return Blog.objects.publicly_viewable()


class BlogListView(ListView, BlogBaseView):
    model = Blog

    def get_queryset(self):
        """
        Only return the object if status is 'published', unless the user is
        a superuser.
        """
        if self.request.user.is_authenticated() and \
                self.request.user.is_superuser:
            return Blog.objects.all()
        else:
            return Blog.objects.publicly_viewable()

