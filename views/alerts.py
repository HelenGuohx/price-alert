from flask import Blueprint, request, render_template, url_for, redirect, session, flash
from models.alert import Alert
from models.item import Item
from models.store import Store
from common.decorators import require_login

from common.errors import Error

alert_blueprint = Blueprint("alert_blueprint", __name__)


@alert_blueprint.route("/", methods=['GET'])
@require_login
def index():
    alerts = Alert.find_many_by("user_email", session['email'])
    return render_template("alerts/index.html", alerts=alerts)


@alert_blueprint.route("/new", methods=["GET", 'POST'])
@require_login
def create_alert():
    if request.method == "POST":
        alert_name = request.form["alert_name"]
        item_url = request.form["item_url"]
        price_limit = float(request.form["price_limit"])

        try:
            store = Store.find_by_url(item_url)
            item = Item(item_url, store.tag_name, store.query)
            item.load_price()
            item.save_to_mongo()
            Alert(alert_name, item._id, price_limit, session["email"]).save_to_mongo()
            flash("success", 'success')
        except Error as e:
            flash(e, 'danger')

    stores = Store.all()
    return render_template("alerts/new_alert.html", stores=stores)


@alert_blueprint.route("/edit/<string:alert_id>", methods=["GET", "POST"])
@require_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == "POST":
        price_limit = float(request.form["price_limit"])

        alert.price_limit = price_limit
        alert.save_to_mongo()
        flash("success", 'success')
        # return redirect(url_for('.index'))

    return render_template("alerts/edit_alert.html", alert=alert)


@alert_blueprint.route("/delete/<string:alert_id>")
@require_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session["email"]:
        alert.remove_from_mongo()
    return redirect(url_for(".index"))
