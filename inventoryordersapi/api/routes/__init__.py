from api.routes import item_routes, order_routes

def include_routers(app):
    app.include_router(item_routes.router)
    app.include_router(order_routes.router)
