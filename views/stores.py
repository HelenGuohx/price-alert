import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.store import Store
from common.decorators import require_login, require_admain


store_blueprint = Blueprint("store_blueprint", __name__)


@store_blueprint.route("/")
@require_login
def index():
    # print(session["email"])
    stores = Store.all()
    return render_template("stores/index.html", stores=stores)


@store_blueprint.route("/new", methods=["GET", "POST"])
@require_admain
def create_store():
    if request.method == "POST":
        name = request.form["name"]
        url_prefix = request.form["url_prefix"]
        tag_name = request.form["tag_name"]
        query = {request.form["attribute"]: request.form["value"]}

        Store(name, url_prefix, tag_name, query).save_to_mongo()
        flash("success", 'success')

    return render_template("stores/new_store.html")


@store_blueprint.route("/edit/<string:store_id>", methods=["GET","POST"])
@require_admain
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == "POST":
        store.url_prefix = request.form["url_prefix"]
        store.tag_name = request.form["tag_name"]
        store.query = {request.form["attribute"]: request.form["value"]}

        store.save_to_mongo()
        flash("success", 'success')
        # return redirect(url_for(".index"))

    return render_template("stores/edit_store.html", store=store)


@store_blueprint.route("delete/<string:store_id>")
@require_admain
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for(".index"))
