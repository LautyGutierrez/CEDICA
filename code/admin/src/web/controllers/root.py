import typing as t
from core import  seed
from core.enums import RegisterTypes
from core.mail import MailService
from src.core.bcrypt import bcrypt
from flask import (
    Blueprint,
    app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import urllib
from utils import status
from src.core.auth import AuthService as auth
from web.forms.auth import ProfileUpdateForm, SeedForm, UserPreRegister, UserRegister, UserLogin, CompleteRegister
from src.web.controllers import _helpers as h
from src.core.google import oauth

bp = Blueprint("root", __name__)


@bp.get("/")
@h.authenticated_route()
def index_get():
    """Renders the index page."""

    if g.user_has_permissions(("usuarios_show",)):
        return redirect("/admin")

    return render_template("index.html")


@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        del session["user_id"]
        if session.get("is_admin"):
            del session["is_admin"]
        session.clear()
        h.flash_info("La sesion se cerró correctamente")
        return redirect(url_for("root.login"))

    session.clear()
    return redirect(url_for("root.login"))


@bp.get("/account_disabled")
@h.require_session()
def account_disable():
    return render_template("account_disabled.html")

# Login y Logout


@bp.get("/login")
@h.require_no_session()
def login():
    form = UserLogin()
    return render_template("login.html", form=form)


@bp.post("/login")
@h.require_no_session()
def authenticate():
    params = request.form
    user = auth.check_user(params["email"], params["password"])
    if not user:
        flash("Invalid email or password", "error")
        return redirect(url_for("root.login"))
    
    if user.deleted:
        flash("Invalid email or password", "error")
        return redirect(url_for("root.login"))

    session["user"] = user.email
    session["user_id"] = user.id
    session["complete_register"] = user.complete_register
    if auth.user_is_admin(user.id):
        session["is_admin"] = True
    flash("Iniciaste sesión correctamente", "success")
    return redirect(url_for("root.index_get"))


# Registro de usuario

@bp.get("/register")
@h.require_no_session()
def register():
    form = UserRegister()
    return render_template("register.html", form=form)


@bp.post("/register")
@h.require_no_session()
def register_post():
    params = request.form

    if params.get("password") != params.get("password_confirmation"):
        flash("Las contraseñás no son iguales", "error")
        return redirect(url_for("root.register"))

    if auth.find_user_exist(params.get("alias"), params.get("email")):
        flash("El Usuario ya existe", "error")
        return redirect(url_for("root.register"))

    user_data = {
        "first_name": params.get("firstname"),
        "last_name": params.get("lastname"),
        "email": params.get("email"),
        "alias": params.get("alias"),
        "password": params.get("password"),
    }

    # Crear el usuario
    user = auth.create_user(**user_data)
    if not user:
        flash("No se pudo crear el usuario", "error")
        return redirect(url_for("root.register"))

    flash("Usuario creado existosamente", "success")
    return redirect(url_for("root.register"))


@bp.get("/complete_register/<int:user_id>")
@h.require_session()
def complete_register(user_id: int):
   
    form = CompleteRegister()
    return render_template("usuarios/register_incomplete.html", form=form)

@bp.post("/complete_register/<int:user_id>")
@h.require_session()
def complete_register_post(user_id: int):
    params = request.form

    if params.get("password") != params.get("password_confirmation"):
        flash("Las contraseñás no son iguales", "error")
        return redirect(url_for("root.complete_register" , user_id=user_id))

    if auth.find_alias(params.get("alias")):
        flash("El alias ya existe", "error")
        return redirect(url_for("root.complete_register" , user_id=user_id))
    
    hashed_password = bcrypt.generate_password_hash(
            params.get("password").encode('utf-8')).decode('utf-8')
    
    user_data = {
        "alias": params.get("alias"),
        "password": hashed_password,
        "complete_register": True,
    }
    
    # Crear el usuario
    user = auth.update_user(user_id, **user_data)
    session["complete_register"] = True
    if not user:
        flash("No se pudo crear el usuario", "error")
        return redirect(url_for("root.complete_register" , user_id=user_id))

    flash("Registro completado", "success")
    return redirect(url_for("root.index_get"))

# Perfil de usuario

@bp.get("/profile")
@h.authenticated_route()
def user_setting_get():

    user = auth.find_user_by_email(t.cast(str, session["user"]))

    form = ProfileUpdateForm(
        firstname=user.first_name,
        lastname=user.last_name,
        email=user.email,
        alias=user.alias,
    )

    return render_template(
        "profile.html",
        user=user,
        form=form,
    )


@bp.post("/profile")
@h.authenticated_route()
def user_setting_post():

    form = ProfileUpdateForm(request.form)
    user_setting = auth.find_user_by_email(t.cast(str, session.get("user")))
    form.email.data = user_setting.email
    form.alias.data = user_setting.alias
    
    if form.validate():
        try:
            id_user = t.cast(int, session.get("user_id"))
            user_setting = auth.update_user(id_user, **form.values())
            if user_setting is None:
                return redirect("/login")

            h.flash_success("Configuración actualizada")
            status_code = status.HTTP_200_OK
        except auth.UserServiceError as e:
            h.flash_error(e.message)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return render_template("profile.html", user=user_setting, form=form), status_code



@bp.get("/login_callback")
def google_login_get():
    return oauth.google.authorize_redirect(  
        url_for("root.google_login_post", _external=True)
    )


@bp.get("/login_callback_get")
def google_login_post():
    token = oauth.google.authorize_access_token() 

    if token is None:
        h.flash_success("Parametros invalidos")
        return redirect("/login")

    user_info = token["userinfo"] 
    user = auth.find_user_by_email_google(user_info["email"]) 
    if user:

        if user.deleted:
            h.flash_info("Usuario inhabilitado")
            return redirect("/login")


        session["user"] = user.email
        session["user_id"] = user.id
        session["complete_register"] = user.complete_register
        if auth.user_is_admin(user.id):
            session["is_admin"] = True
        h.flash_success("Se inicio sesion correctamente")
        return redirect(url_for("root.index_get"))
    
    user = auth.find_user_by_email(user_info["email"])
    if user:
        h.flash_info(
            "Parece que ya tienes una cuenta registrada sin google, por favor inicia sesion con tu correo y contraseña"
        )
        return redirect("/login")

    user = auth.get_pre_user_by_email(user_info["email"])  
    if user:
        h.flash_info(
            "Aun el administrador no ha aprobado su registro, por favor espere"
        )
        return redirect("/login")

    
    name = user_info["given_name"]
    lastname = user_info["family_name"]
    user = auth.create_user_pre_register(
        first_name=name,
        last_name=lastname,
        email=user_info["email"],  
    )

    h.flash_info(
        "Hemos registrado sus datos, por favor espere a que el administrador apruebe su registro con google"
    )
    return redirect(
        url_for("root.login")
    )








@bp.get("/register_callback")
def google_register_get():
    return oauth.google.authorize_redirect(  
        url_for("root.google_register_post", _external=True)
    )


@bp.get("/register_callback_get")
def google_register_post():
    token = oauth.google.authorize_access_token() 

    if token is None:
        h.flash_success("Parametros invalidos")
        return redirect("/login")

    user_info = token["userinfo"] 
   
    user = auth.find_user_by_email(user_info["email"])
    if user:
        if user.type_register == 'MANUAL':
            h.flash_info(
                "Parece que ya tienes una cuenta registrada sin google, por favor inicia sesion con tu correo y contraseña"
            )
            return redirect("/login")
        else:
            h.flash_info(
                "Parece que ya tienes una cuenta registrada con google, por favor inicia sesion con google"
            )
            return redirect("/login")

    user = auth.get_pre_user_by_email(user_info["email"])  
    if user:
        h.flash_info(
            "Parece que ya tienes una cuenta pre registrada con google, por favor espere a que el administrador apruebe su registro"
        )
        return redirect("/login")

    
    name = user_info["given_name"]
    lastname = user_info["family_name"]
    user = auth.create_user_pre_register(
        first_name=name,
        last_name=lastname,
        email=user_info["email"],  
    )

    h.flash_info(
        "Hemos registrado sus datos, por favor espere a que el administrador apruebe su registro con google"
    )
    return redirect(
        url_for("root.login")
    )





















@bp.get("/seed")
def seed_get():
    form = SeedForm()
    return render_template(
        "seed.html",
        form=form,
    )


@bp.post("/seed")
def seed_post():
    form = SeedForm(request.form)
    data = form.data
    if data["username"] == "KAKSFJDLDKAS123123" and data["password"] == "AJKWDAADKJALKDSJ123-9011":
        seed.seed_db()
        h.flash_info("Seed data has been created")
        return render_template("seed.html", form=form)
    h.flash_error("Invalid username or password")
    return render_template("seed.html", form=form)
