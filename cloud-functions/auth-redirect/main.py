from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def main(request):
    authorization_code = request.args.get('code')
    template = env.get_template('index.html')
    return template.render(
        authorization_code=authorization_code
    )
