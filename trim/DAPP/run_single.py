from DProject import *
from BTemplate import *
from utils import *

def main():
	template_name = input(f"{get_folders()}\n\n\n ¿ \
	Que plantilla quieres usar para el proyecto ?\n")
	
	project = DProject(root=template_name.lower())
	project.prepare_app()
	
	print(template_name.title(), project.root)
	btemplate = BTemplate(template=f"{template_name.title()}", project=f"{project.root}")
	
	project.add_views()
	project.add_urls()
	project.add_static_to_settings()	
		
	project.replace_img_srcs()	
	project.replace_img_and_page_href()
	project.replace_img_backgrounds()
	project.replace_img_in_css()
	
	project.send_partials()
	project.clean_main_templates()
	project.move_unclean_to_original()


if __name__ == "__main__":
	main()

	