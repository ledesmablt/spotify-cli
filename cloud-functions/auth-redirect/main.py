from flask import render_template


def main(request):
    """Web UI for displaying user authorization code.

    Generates the redirect page for spotify.auth.login"""
    authorization_code = request.args.get('code')
    return render_template(
        'index.html',
        authorization_code=authorization_code
    )
