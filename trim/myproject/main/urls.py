from django.urls import path
import views


#add your url patters here :)


urlpatterns = [ 

	path('about/', views.about, name='about'),
	path('blog-single/', views.blog_single, name='blog_single'),
	path('blog/', views.blog, name='blog'),
	path('contact/', views.contact, name='contact'),
	path('index/', views.index, name='index'),
	path('portfolio-details/', views.portfolio_details, name='portfolio_details'),
	path('portfolio/', views.portfolio, name='portfolio'),
	path('pricing/', views.pricing, name='pricing'),
	path('services/', views.services, name='services'),
	path('team/', views.team, name='team'),
	path('testimonials/', views.testimonials, name='testimonials'),
