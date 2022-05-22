


def about(requests):
	template= 'main/about.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def blog_single(requests):
	template= 'main/blog-singles.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def blog(requests):
	template= 'main/blog.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def contact(requests):
	template= 'main/contact.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def index(requests):
	template= 'main/index.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def portfolio_details(requests):
	template= 'main/portfolio-details.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def portfolio(requests):
	template= 'main/portfolio.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def pricing(requests):
	template= 'main/pricing.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def services(requests):
	template= 'main/services.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def team(requests):
	template= 'main/team.html'
	context= {'template': 'variable'}
	return render(requests, template, context)


def testimonials(requests):
	template= 'main/testimonials.html'
	context= {'template': 'variable'}
	return render(requests, template, context)