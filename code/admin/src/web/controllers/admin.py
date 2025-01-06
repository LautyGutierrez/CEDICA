from functools import wraps
import random
import string
from core.auth.roles import get_roles
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from web.forms.auth import UserUpdatePreRegisterToUserForm
from web.forms.user import ProfileUpdateForm, UserCreateForm
from src.utils import status
from src.web.controllers import _helpers as h
from src.core.auth import AuthService as auth

bp = Blueprint("admin", __name__, url_prefix="/admin")


def validate_user_decorator(func):
    """
    Decorador que chequea que un miembro exista y no esté borrado.
    Args:
        func: función del controlador a ser decorada.
    Returns:
        function: si el miembro es válido, devuelve la función decorada. Si no, redirige a la página principal.
    """

    @wraps(func)
    def wrapper(user_id: int, *args, **kwargs):
       
        user = auth.get_user(user_id)
        if not user or user['deleted']:
            h.flash_error("Usuario no encontrado")
            return redirect("/admin/users")
        
        return func(user, *args, **kwargs)

    return wrapper

def validate_user_deleted_decorator(func):
    """
    Decorador que chequea que un miembro exista si importar si está borrado o no.
    Args:
        func: función del controlador a ser decorada.
    Returns:
        function: si el miembro es válido, devuelve la función decorada. Si no, redirige a la página principal.
    """

    @wraps(func)
    def wrapper(user_id: int, *args, **kwargs):
       
        user = auth.get_user(user_id)
        if not user:
            h.flash_error("Usuario no encontrado")
            return redirect("/admin/users")
        
        return func(user, *args, **kwargs)

    return wrapper


@bp.get("/")
@h.authenticated_route(module="usuarios", permissions=("show", "index"))
def index_get():
    """Renders the admin index page."""
    return render_template("/index.html")


@bp.get("/users")
@h.authenticated_route(module="usuarios", permissions=("index", "create", "update", "destroy"))
def usuarios_get():
    page, per_page = h.url_pagination_args(
        default_per_page=10
    )

    email = request.values.get("email")
    active = request.values.get("active")
    rol = request.values.get("rol")
    order = request.args.get('order', 'asc')
    order_by = request.values.get('order_by', 'email')

    if request.args.get('toggle_order'):
        order = 'desc' if order == 'asc' else 'asc'

    users, total = auth.filter_users(
        email, active, rol, order, order_by, page, per_page
    )

    return render_template(
        "usuarios/index.html",
        users=users,
        page=page,
        per_page=per_page,
        total=total,
        email=email,
        roles=rol,
        active=active,
        order=order,
        order_by=order_by
    )


@bp.get("/users/create")
@h.authenticated_route(module="usuarios", permissions=("create",))
def users_new_get():
    form = UserCreateForm()
    form.role.choices = [(role.id, role.name) for role in get_roles()]

    return render_template("usuarios/create.html", form=form)


@bp.post("/users/create")
@h.authenticated_route(module="usuarios", permissions=("create",))
def services_new_post():

    params = request.form

    if params.get("password") != params.get("password_confirmation"):
        h.flash_error("Las contraseñás no son iguales")
        return redirect(url_for("admin.users_new_get"))

    if auth.find_user_exist(params.get("alias"), params.get("email")):
        h.flash_error("El Usuario ya existe")
        return redirect(url_for("admin.users_new_get"))

    user_data = {
        "first_name": params.get("firstname"),
        "last_name": params.get("lastname"),
        "email": params.get("email"),
        "alias": params.get("alias"),
        "rol_id": params.get("role"),
        "password": params.get("password"),
    }

    user = auth.create_user(**user_data)
    if not user:
        h.flash_error("No se pudo crear el usuario")
        return redirect(url_for("admin.users_new_get"))

    h.flash_success("Usuario creado existosamente")
    return redirect("/admin/users")


@bp.get("/users/<int:user_id>")
@h.authenticated_route(module="usuarios", permissions=("show", "update"))
@validate_user_decorator
def users_id_get(user, *args, **kwargs):

    form = ProfileUpdateForm(
        firstname=user['firstname'],
        lastname=user['lastname'],
        email=user['email'],
        alias=user['alias']
    )



    roles = [(role.id, role.name) for role in get_roles()]
    return render_template(
        "usuarios/update.html", user=user, form=form, roles=roles
    )


@bp.post("/users/<int:user_id>")
@h.authenticated_route(module="usuarios", permissions=("update",))
@validate_user_decorator
def users_id_post(user, *args, **kwargs):

    if request.form.get("alias") != user["alias"] or request.form.get("email") != user["email"]:
        if auth.find_user_exist(request.form.get("alias"), request.form.get("email")):
            h.flash_error("Existe un usuario con ese email o alias.")
            return redirect(url_for("admin.users_id_get", user_id=user["id"]))



    form = ProfileUpdateForm(request.form)

    if not form.validate():
        
        h.flash_info("Por favor, complete todos los campos requeridos.")
        return redirect(url_for("admin.users_id_get", user_id=user["id"]))

    auth.update_user(user["id"], **form.values())
    flash("Usuario actualizado con éxito.", "success")
    return redirect("/admin/users")


@bp.post("/users/<int:user_id>/toggle_active")
@h.authenticated_route(module="usuarios", permissions=("update",))
@validate_user_decorator
def users_id_toggle_active_post(user, *args, **kwargs):

    auth.toggle_active(user['id'])
    if user["is_active"]:
        h.flash_success("Usuario activado con éxito.")
    else:
        h.flash_success("Usuario desactivado con éxito.")

    return redirect("/admin/users")


@bp.post("/users/<int:user_id>/delete")
@h.authenticated_route(module="usuarios", permissions=("destroy",))
@validate_user_decorator
def users_id_delete_post(user, *args, **kwargs):

    if user['role'] == "SYSTEM_ADMIN":
        h.flash_error("No se puede eliminar usuarios system admins.")
        return redirect("/admin/users")

    result = auth.delete_user(user['id'])

    if result:
        h.flash_success("Usuario eliminado con éxito.")
        return redirect("/admin/users")

    h.flash_error("No se pudo eliminar el usuario.")
    return redirect(f"/admin/users/{user.id}")



@bp.get("/users/deleteds")
@h.authenticated_route(module="usuarios", permissions=("index", "create", "update", "destroy"))
def usuarios_deleteds_get():
    """"
    Renderiza la página de usuarios eliminados.
    """
    page, per_page = h.url_pagination_args(
        default_per_page=10
    )

    users, total = auth.filter_users_deleteds(
        page, per_page
    )

    return render_template(
        "usuarios/deleteds.html",
        users=users,
        page=page,
        per_page=per_page,
        total=total,
        
    )

@bp.post("/users/<int:user_id>/toggle_deleted")
@h.authenticated_route(module="usuarios", permissions=("update",))
@validate_user_deleted_decorator
def users_id_toggle_deleted_post(user, *args, **kwargs):

    a = auth.toggle_deleted(user['id'])
    h.flash_success("Usuario restaurado con éxito.")
    return redirect("/admin/users")



@bp.get("/users/preRegisters")
@h.authenticated_route(module="usuarios", permissions=("accept",))
def usuarios_preregisters_get():
    """"
    Renderiza la página de usuarios eliminados.
    """
    page, per_page = h.url_pagination_args(
        default_per_page=10
    )

    preusers, total = auth.filter_pre_users(
        page, per_page
    )

    return render_template(
        "usuarios/pre-register.html",
        preusers=preusers,
        page=page,
        per_page=per_page,
        total=total,
        
    )


@bp.get("/users/<int:user_id>/approve_registration")
@h.authenticated_route(module="usuarios", permissions=("accept",))
def pre_users_id_get(user_id: int):
    pre_user = auth.get_pre_user_by_id(user_id)
    
    if pre_user is None:
        h.flash_error("Usuario no encontrado.")
        return redirect("/admin/users/preRegisters")
    

    form = UserUpdatePreRegisterToUserForm(
        firstname=pre_user.first_name,
        lastname=pre_user.last_name,
        email=pre_user.email
    )

    roles = [(role.id, role.name) for role in get_roles()]
    return render_template(
        "usuarios/update_preuser.html", user=pre_user, form=form, roles=roles
    )

@bp.post("/users/<int:user_id>/approve_registration")
@h.authenticated_route(module="usuarios", permissions=("accept",))
def users_id_approve_registration_post(user_id: int):
    
    params = request.form
    password_provisional = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    alias_provisional = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    if auth.find_user_exist(alias_provisional, params.get("email")):
        h.flash_error("El Usuario ya existe")
        return redirect(url_for("admin.pre_users_id_get", user_id=user_id))

    user_data = {
        "first_name": params.get("firstname"),
        "last_name": params.get("lastname"),
        "email": params.get("email"),
        "alias": alias_provisional,
        "rol_id": params.get("role"),
        "password": password_provisional,
        "complete_register": False,
        "type_register": "GOOGLE"
    }

    user = auth.create_user(**user_data)
    
    if user is None:
        h.flash_error("No se pudo crear el usuario")
        return redirect(url_for("admin.pre_users_id_get", user_id=user_id))

    pre_user = auth.delete_preuser(user_id)
    if not pre_user:
        h.flash_error("No se pudo crear el usuario")
        return redirect(url_for("admin.pre_users_id_get", user_id=user_id))

    h.flash_success("Usuario creado existosamente")
    return redirect("/admin/users")

