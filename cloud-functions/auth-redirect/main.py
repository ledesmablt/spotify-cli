from flask import render_template

def main(request):
    authorization_code = request.args.get('code')
    return render_template(
        'index.html',
        authorization_code=authorization_code
    )
