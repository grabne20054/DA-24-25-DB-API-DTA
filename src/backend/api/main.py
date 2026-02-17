from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import metadata, engine

from api import employees, siteconfigs, addresses, customers, orders, products, routes, categories, invoices, carts, categoriesProducts, ordersProducts, cartsProducts, routesOrders, roles


metadata.create_all(engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(employees.router)
app.include_router(siteconfigs.router)
app.include_router(addresses.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(routes.router)
app.include_router(categories.router)
app.include_router(invoices.router)
app.include_router(carts.router)
app.include_router(categoriesProducts.router)
app.include_router(ordersProducts.router)
app.include_router(cartsProducts.router)
app.include_router(roles.router)
app.include_router(routesOrders.router)