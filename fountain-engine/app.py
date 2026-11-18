"""
Fountain Engine Marketplace - backend mínimo.

Aloja el catálogo, el detalle de recurso, un carrito de compras (memoria)
 y un checkout simulado. Proyecto base para añadir persistencia, autenticación
 y pago real en el futuro.
"""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
STATS_FILE = BASE_DIR / "temp" / "stats.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open(encoding="utf-8") as fh:
            return json.load(fh)
    return {
        "name": "Fountain Engine Marketplace",
        "tagline": "Recursos de programación web y desarrollo en un solo lugar",
        "version": "1.0.0",
        "resources": []
    }


def load_resources() -> list[dict]:
    return load_config().get("resources", [])


def load_stats() -> dict:
    if STATS_FILE.exists():
        try:
            with STATS_FILE.open(encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    return {"views": 0, "purchases": 0}


def save_stats(stats: dict) -> None:
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    @app.context_processor
    def inject_globals():
        return {
            "config": load_config(),
            "current_year": 2026,
            "brand_color": load_config().get("theme", {}).get("brand", "#f2c94c"),
        }

    def currency_filter(value):
        try:
            price = float(value)
        except (TypeError, ValueError):
            return str(value)
        return f"${price:,.2f}"

    app.jinja_env.filters["currency"] = currency_filter

    @app.route("/")
    def home():
        stats = load_stats()
        stats["views"] = stats.get("views", 0) + 1
        save_stats(stats)
        return render_template("home.html")

    @app.route("/catalog")
    def catalog():
        return render_template("catalog.html", resources=load_resources())

    @app.route("/resource/<resource_id>")
    def resource_detail(resource_id: str):
        resource = next((item for item in load_resources() if item.get("id") == resource_id), None)
        if resource is None:
            abort(404)
        stats = load_stats()
        stats["views"] = stats.get("views", 0) + 1
        save_stats(stats)
        return render_template("resource.html", resource=resource)

    cart = {}

    @app.route("/cart", methods=["GET", "POST"])
    def cart_route():
        if request.method == "POST":
            try:
                data = request.get_json(force=True)
            except Exception:
                abort(400)
            resource_id = data.get("resource_id")
            quantity = int(data.get("quantity", 1))
            if not resource_id or quantity < 1:
                abort(400)
            if quantity > 5:
                quantity = 5
            cart[resource_id] = cart.get(resource_id, 0) + quantity
            return jsonify({"status": "ok", "cart": cart})

        resources = load_resources()
        subtotal = sum(
            resource.get("price", 0) * qty
            for resource_id, qty in cart.items()
            if any(item["id"] == resource_id for item in resources)
        )
        total = subtotal
        return render_template("cart.html", cart=cart, resources=resources, subtotal=subtotal, total=total)

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        if request.method == "POST":
            try:
                data = request.get_json(force=True)
            except Exception:
                abort(400)
            email = data.get("email", "").strip()
            token = data.get("token", "")
            if not email or "@" not in email or not token:
                abort(400)
            stats = load_stats()
            stats["purchases"] = stats.get("purchases", 0) + 1
            save_stats(stats)
            return render_template("checkout.html", completed=True, email=email)

        return render_template("checkout.html", completed=False, email=None)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            name = request.form.get("name", "").strip()
            message = request.form.get("message", "").strip()
            if not email or "@" not in email or not message:
                abort(400)
            return render_template("contact.html", submitted=True, name=name)

        return render_template("contact.html", submitted=False, name=None)

    @app.route("/api/resources")
    def api_resources():
        return jsonify(load_resources())

    @app.route("/api/cart", methods=["GET", "POST"])
    def api_cart():
        if request.method == "POST":
            try:
                data = request.get_json(force=True)
            except Exception:
                abort(400)
            resource_id = data.get("resource_id")
            quantity = int(data.get("quantity", 1))
            if not resource_id or quantity < 1:
                abort(400)
            if quantity > 5:
                quantity = 5
            cart[resource_id] = cart.get(resource_id, 0) + quantity
            return jsonify({"status": "ok", "cart": cart})

        return jsonify(cart)

    @app.route("/api/stats")
    def api_stats():
        return jsonify(load_stats())

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
