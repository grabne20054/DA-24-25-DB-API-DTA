from api.model import Employee, SiteConfig, Address, Customer, Order, Product, Route, Category, Invoice, Cart, Role, Sector
from db.session import session
from fastapi import HTTPException
from db.model import Employee, SiteConfig, Address, Customer, Order, Product, Route, Category, Invoice, Cart, Role, Sector, categoriesProducts, ordersProducts, routesOrders, cartsProducts
from sqlalchemy import select, delete
from uuid import UUID
from datetime import datetime

# GET PER ID
def get_employee(employee_id: UUID):
    employee = session.query(Employee).filter(Employee.employeeId == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def get_site_config(site_config_id: UUID):
    site_config = session.query(SiteConfig).filter(SiteConfig.siteConfigId == site_config_id).first()
    if not site_config:
        raise HTTPException(status_code=404, detail="Site config not found")
    return site_config

def get_address(address_id: UUID):
    address = session.query(Address).filter(Address.addressId == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

def get_customer(customer_id: UUID):
    customer = session.query(Customer).filter(Customer.customerId == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def get_order(order_id: UUID):
    order = session.query(Order).filter(Order.orderId == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_product(product_id: UUID):
    product = session.query(Product).filter(Product.productId == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_route(route_id: UUID):
    route = session.query(Route).filter(Route.routeId == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

def get_category(category_id: UUID):
    category = session.query(Category).filter(Category.categoryId == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_invoice(invoice_id: UUID):
    invoice = session.query(Invoice).filter(Invoice.invoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

def get_cart(cart_id: UUID):
    cart = session.query(Cart).filter(Cart.cartId == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def get_categoriesProducts(categoryId: UUID, productId: UUID):
    categories = (
        session.query(Category)
        .join(
            categoriesProducts,
            Category.categoryId == categoriesProducts.c.categoryId
        ).filter(
            categoriesProducts.c.productId == productId,
            categoriesProducts.c.categoryId == categoryId
        )
        .first()
    )
    if categories is not None:
        return categories
    else:
        raise HTTPException(status_code=404, detail="Category or Product not found")
    
def get_cartsProducts(cartId: UUID, productId: UUID):
    carts = (
        session.query(Cart)
        .join(
            cartsProducts,
            Cart.cartId == cartsProducts.c.cartId
        ).filter(
            cartsProducts.c.productId == productId,
            cartsProducts.c.cartId == cartId
        )
        .first()
    )
    if carts is not None:
        return carts
    else:
        raise HTTPException(status_code=404, detail="Cart or Product not found")

def get_ordersProducts(orderId: UUID, productId: UUID):
    orders = (
        session.query(Order)
        .join(
            ordersProducts,
            Order.orderId == ordersProducts.c.orderId
        ).filter(
            ordersProducts.c.productId == productId,
            ordersProducts.c.orderId == orderId
        )
        .first()
    )
    if orders is not None:
        return orders
    else:
        raise HTTPException(status_code=404, detail="Order or Product not found")
    
def get_routesOrders(routeId: UUID, orderId: UUID):
    routes = (
        session.query(Route)
        .join(
            routesOrders,
            Route.routeId == routesOrders.c.routeId
        ).filter(
            routesOrders.c.orderId == orderId,
            routesOrders.c.routeId == routeId
        )
        .first()
    )
    if routes is not None:
        return routes
    else:
        raise HTTPException(status_code=404, detail="Route or Order not found")    
    

def get_categoriesProducts_by_categoryId(categoryId: UUID):
    products = (
        session.query(Product)
        .filter(Product.productId.in_(
            session.query(categoriesProducts.c.productId)
            .filter(categoriesProducts.c.categoryId == categoryId)
        ))
        .all()
    )

    if session.query(Category).filter(Category.categoryId == categoryId).first() is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products
    
def get_categoriesProducts_by_productId(productId: UUID):
    categories = (
        session.query(Category)
        .filter(Category.categoryId.in_(
            session.query(categoriesProducts.c.categoryId)
            .filter(categoriesProducts.c.productId == productId)
        ))
        .all()
    )
    if session.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories

def get_cartsProducts_by_cartId(cartId: UUID):
    products = (
        session.query(Product)
        .filter(Product.productId.in_(
            session.query(cartsProducts.c.productId)
            .filter(cartsProducts.c.cartId == cartId)
        ))
        .all()
    )

    if session.query(Cart).filter(Cart.cartId == cartId).first() is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_cartsProducts_by_productId(productId: UUID):
    carts = (
        session.query(Cart)
        .filter(Cart.cartId.in_(
            session.query(cartsProducts.c.cartId)
            .filter(cartsProducts.c.productId == productId)
        ))
        .all()
    )
    if session.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts

def get_ordersProducts_by_orderId(orderId: UUID):
    products = (
        session.query(Product)
        .filter(Product.productId.in_(
            session.query(ordersProducts.c.productId)
            .filter(ordersProducts.c.orderId == orderId)
        ))
        .all()
    )

    if session.query(Order).filter(Order.orderId == orderId).first() is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_ordersProducts_by_productId(productId: UUID):
    orders = (
        session.query(Order)
        .filter(Order.orderId.in_(
            session.query(ordersProducts.c.orderId)
            .filter(ordersProducts.c.productId == productId)
        ))
        .all()
    )
    if session.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_routesOrders_by_routeId(routeId: UUID):
    orders = (
        session.query(Order)
        .filter(Order.orderId.in_(
            session.query(routesOrders.c.orderId)
            .filter(routesOrders.c.routeId == routeId)
        ))
        .all()
    )

    if session.query(Route).filter(Route.routeId == routeId).first() is None:
        raise HTTPException(status_code=404, detail="Route not found")
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_routesOrders_by_orderId(orderId: UUID):
    routes = (
        session.query(Route)
        .filter(Route.routeId.in_(
            session.query(routesOrders.c.routeId)
            .filter(routesOrders.c.orderId == orderId)
        ))
        .all()
    )
    if session.query(Order).filter(Order.orderId == orderId).first() is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if not routes:
        raise HTTPException(status_code=404, detail="Route not found")
    return routes




# GET ALL
def get_employees(email:str, password:str):
    if email is not None and password is not None:
        employees = session.query(Employee).filter(Employee.email == email, Employee.password == password).all()
    else: 
        employees = session.query(Employee).all()
    return employees

def get_site_configs():
    site_configs = session.query(SiteConfig).all()
    return site_configs

def get_addresses():
    addresses = session.query(Address).all()
    return addresses

def get_customers():
    customers = session.query(Customer).all()
    return customers

def get_orders():
    orders = session.query(Order).all()
    return orders

def get_products():
    products = session.query(Product).all()
    return products

def get_routes():
    routes = session.query(Route).all()
    return routes

def get_categories():
    categories = session.query(Category).all()
    return categories

def get_invoices():
    invoices = session.query(Invoice).all()
    return invoices

def get_carts():
    carts = session.query(Cart).all()
    return carts


def get_categoriesProductss():
    return session.execute(select(categoriesProducts)).mappings().all()

def get_cartsProductss():
    return session.execute(select(cartsProducts)).mappings().all()

def get_ordersProductss():
    return session.execute(select(ordersProducts)).mappings().all()




def get_routesOrderss():
    return session.execute(select(routesOrders)).mappings().all()


# POST (JUST FOR MOCKUP)
def create_employee(payload: Employee):
    employee = Employee(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )
    session.add(employee)
    session.commit()
    return employee.employeeId

def create_site_config(payload: SiteConfig):
    site_config = SiteConfig(
        companyName=payload.companyName,
        logoPath=payload.logoPath,
        email=payload.email,
        phoneNumber=payload.phoneNumber,
        companyNumber=payload.companyNumber,
        iban=payload.iban,
        addressId=payload.addressId
    )
    session.add(site_config)
    session.commit()
    return site_config.siteConfigId

def create_address(payload: Address):
    address = Address(
        streetName=payload.streetName,
        streetNumber=payload.streetNumber,
        city=payload.city,
        postCode=payload.postCode,
        country=payload.country,
        state=payload.state)
    session.add(address)
    session.commit()
    return address.addressId

def create_customer(payload: Customer):
    customer = Customer(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phoneNumber=payload.phoneNumber,
        companyNumber=payload.companyNumber,
        customerReference=payload.customerReference,
        signedUp=payload.signedUp,
        role=payload.role,
        businessSector=payload.businessSector,
        avatarPath=payload.avatarPath,
        addressId=payload.addressId)
    
    session.add(customer)
    session.commit()
    return customer.customerId

def create_order(payload: Order):
    order = Order(
        orderDate=payload.orderDate,
        deliveryDate=payload.deliveryDate,
        customerReference=payload.customerReference,
        orderState=payload.orderState,
        selfCollect=payload.selfCollect,)
    session.add(order)
    session.commit()
    return order.orderId

def create_product(payload: Product):
    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        imagePath=payload.imagePath,
        createdAt=payload.createdAt
        )
    session.add(product)
    session.commit()
    return product.productId

def create_route(payload: Route):
    route = Route(
        name=payload.name,
    )
    session.add(route)
    session.commit()
    return route.routeId

def create_category(payload: Category):
    category = Category(
        name=payload.name,
        imagePath=payload.imagePath
    )
    session.add(category)
    session.commit()
    return category.categoryId

def create_cart(payload: Cart):
    cart = Cart(
        customerReference=payload.customerReference,
    )
    session.add(cart)
    session.commit()
    return cart.cartId

def create_invoice(payload: Invoice):
    invoice = Invoice(
        orderId=payload.orderId,
        invoiceAmount=payload.invoiceAmount,
        paymentDate=payload.paymentDate,
        pdfUrl=payload.pdfUrl
    )
    session.add(invoice)
    session.commit()
    return invoice.invoiceId

def create_categoriesProducts(categoryId: UUID, productId: UUID):
    already_in_category = (
        session.query(categoriesProducts).filter_by(categoryId=categoryId, productId=productId).first()
    )

    if already_in_category:
        raise HTTPException(status_code=400, detail="Already in category")
    
    procuct_exists = session.query(Product).filter(Product.productId == productId).first()
    category_exists = session.query(Category).filter(Category.categoryId == categoryId).first()

    if procuct_exists and category_exists:
        session.execute(categoriesProducts.insert().values(categoryId=categoryId, productId=productId))
        session.commit()
        return productId, categoryId
    else:
        raise HTTPException(status_code=404, detail="Product or category not found")
    
def create_ordersProducts(productId: UUID, orderId: UUID, productAmount: int, orderDate: datetime): 
    product_exists = session.query(Product).filter(Product.productId == productId).first()
    order_exists = session.query(Order).filter(Order.orderId == orderId).first()

    if product_exists and order_exists:
        session.execute(ordersProducts.insert().values(productId=productId, orderId=orderId, productAmount=productAmount, orderDate=orderDate))
        session.commit()
        return productId, orderId, productAmount, orderDate
    else:
        raise HTTPException(status_code=404, detail="Product or order not found")

def create_routesOrders(routeId: UUID, orderId: UUID):
        
        route_exists = session.query(Route).filter(Route.routeId == routeId).first()
        order_exists = session.query(Order).filter(Order.orderId == orderId).first()
    
        if route_exists and order_exists:
            session.execute(routesOrders.insert().values(routeId=routeId, orderId=orderId))
            session.commit()
            return routeId, orderId
        else:
            raise HTTPException(status_code=404, detail="Route or order not found")

def create_cartsProducts(productId: UUID, cartId: UUID, productAmount: int):
            
        procuct_exists = session.query(Product).filter(Product.productId == productId).first()
        cart_exists = session.query(Cart).filter(Cart.cartId == cartId).first()
    
        if procuct_exists and cart_exists:
            session.execute(cartsProducts.insert().values(productId=productId, cartId=cartId, productAmount=productAmount))
            session.commit()
            return productId, cartId, productAmount
        else:
            raise HTTPException(status_code=404, detail="Product or cart not found")
        


# DELETE BY ID

def delete_employee(employee_id: UUID):
    employee = session.query(Employee).filter(Employee.employeeId == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return employee_id

def delete_site_config(config_id: UUID):
    site_config = session.query(SiteConfig).filter(SiteConfig.configId == config_id).first()
    if not site_config:
        raise HTTPException(status_code=404, detail="Site config not found")
    session.delete(site_config)
    session.commit()
    return config_id

def delete_address(address_id: UUID):
    address = session.query(Address).filter(Address.addressId == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    session.delete(address)
    session.commit()
    return address_id

def delete_customer(customer_id: UUID):
    customer = session.query(Customer).filter(Customer.customerId == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return customer_id

def delete_order(order_id: UUID):
    order = session.query(Order).filter(Order.orderId == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return order_id

def delete_product(product_id: UUID):
    product = session.query(Product).filter(Product.productId == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return product_id

def delete_route(route_id: UUID):
    route = session.query(Route).filter(Route.routeId == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    session.delete(route)
    session.commit()
    return route_id

def delete_category(category_id: UUID):
    category = session.query(Category).filter(Category.categoryId == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return category_id

def delete_invoice(invoice_id: UUID):
    invoice = session.query(Invoice).filter(Invoice.invoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    session.delete(invoice)
    session.commit()
    return invoice_id

def delete_cart(cart_id: UUID):
    cart = session.query(Cart).filter(Cart.cartId == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    session.delete(cart)
    session.commit()
    return cart_id

# DELETE ALL
def delete_employees():
    employees = session.query(Employee).all()
    for employee in employees:
        session.delete(employee)
    session.commit()
    return True

def delete_site_configs():
    site_configs = session.query(SiteConfig).all()
    for site_config in site_configs:
        session.delete(site_config)
    session.commit()
    return True

def delete_addresses():
    addresses = session.query(Address).all()
    for address in addresses:
        session.delete(address)
    session.commit()
    return True

def delete_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        session.delete(customer)
    session.commit()
    return True

def delete_orders():
    orders = session.query(Order).all()
    for order in orders:
        session.delete(order)
    session.commit()
    return True

def delete_products():
    products = session.query(Product).all()
    for product in products:
        session.delete(product)
    session.commit()
    return True

def delete_routes():
    routes = session.query(Route).all()
    for route in routes:
        session.delete(route)
    session.commit()
    return True

def delete_categories():
    categories = session.query(Category).all()
    for category in categories:
        session.delete(category)
    session.commit()
    return True

def delete_invoices():
    invoices = session.query(Invoice).all()
    for invoice in invoices:
        session.delete(invoice)
    session.commit()
    return True

def delete_carts():
    carts = session.query(Cart).all()
    for cart in carts:
        session.delete(cart)
    session.commit()
    return True


def delete_ordersProductss():
    session.execute(delete(ordersProducts))
    session.commit()
    return True

def delete_categoriesProductss():
    session.execute(delete(categoriesProducts))
    session.commit()
    return True

def delete_cartsProductss():
    session.execute(delete(cartsProducts))
    session.commit()
    return True
    