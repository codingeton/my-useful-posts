from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^posts/$', views.search, name='posts'),
    url(r'^$',views.PostListView.as_view(paginate_by=5),name='post_list'),
    url(r'^about/$',views.AboutView.as_view(),name='about'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/pdf/$', views.BlogListPdf.as_view(),name='pdf'),
    url(r'^post/content/(?P<pk>\d+)$', views.BlogDetailPDF.as_view(),name='content'),
    url(r'^leverage/$',views.leverage_calculate,name='leverage'),
    url(r'^api/posts/$',views.PostListRest.as_view()),
    path('api/posts/<int:pk>/$',views.PostDetailRest.as_view()),
]
