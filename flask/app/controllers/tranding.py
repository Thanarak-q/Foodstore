import json
from datetime import datetime, timedelta
from flask import request, jsonify
from app import app
from app.models.menu import Menu
from app.models.order import Order


def parse_menu_list(menu_list):
    """
    Convert the menu_list dictionary into a list of tuples [(menu_id, quantity), ...]
    """
    return [(int(menu_id), int(qty)) for menu_id, qty in menu_list.items()]


def get_trending_menu(start_date=None, end_date=None):
    """
    Main function to calculate trending menus within a specified time range.
    - start_date, end_date: Define the time range (None = no range).
    """
    all_menu = Menu.query.all()
    all_order = Order.query.all()

    menu_sales = {}

    for order in all_order:
        if (start_date and order.order_time < start_date) or (end_date and order.order_time > end_date):
            continue  # Skip orders outside the specified time range

        items = parse_menu_list(order.menu_list)
        for menu_id, qty in items:
            menu = next((m for m in all_menu if m.id == menu_id), None)
            if menu:
                if menu.name not in menu_sales:
                    menu_sales[menu.name] = {"total_sold": 0, "image_url": menu.image_url}
                menu_sales[menu.name]["total_sold"] += qty

    # Return the top 5 trending menus
    sorted_sales = sorted(menu_sales.items(), key=lambda x: x[1]["total_sold"], reverse=True)
    return [{"menu_name": name, "total_sold": data["total_sold"], "image_url": data["image_url"]} for name, data in sorted_sales[:5]]


@app.route('/daily_trending')
def get_daily_trending():
    """
    Trending menus for the current day.
    """
    now = datetime.now()
    start_date = datetime(now.year, now.month, now.day)
    end_date = now
    return jsonify(get_trending_menu(start_date, end_date))


@app.route('/weekly_trending')
def get_weekly_trending():
    """
    Trending menus for the last 7 days.
    """
    now = datetime.now()
    start_date = now - timedelta(days=7)
    end_date = now
    return jsonify(get_trending_menu(start_date, end_date))


@app.route('/monthly_trending')
def get_monthly_trending():
    """
    Trending menus for the current month.
    """
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1) 
    end_date = now  
    return jsonify(get_trending_menu(start_date, end_date))

@app.route('/yearly_trending')
def get_yearly_trending():
    """
    Trending menus for the current year.
    """
    now = datetime.now()
    start_date = datetime(now.year, 1, 1)
    end_date = now
    return jsonify(get_trending_menu(start_date, end_date))


@app.route('/all_time_trending')
def get_all_time_trending():
    """
    All-time trending menus.
    """
    return jsonify(get_trending_menu())


@app.route('/custom_trending')
def get_custom_trending():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    return jsonify(get_trending_menu(start_date, end_date))

#!-------------------------------------------------------------------------------------------------