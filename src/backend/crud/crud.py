from api.model import Employee, SiteConfig, Address, Customer, Order, Product, Route, Category, Invoice, Cart, Role, Sector
from fastapi import HTTPException
from db.model import Employee, SiteConfig, Address, Customer, Order, Product, Route, Category, Invoice, Cart, Role, Sector, categoriesProducts, ordersProducts, routesOrders, cartsProducts, Role
from sqlalchemy import select, delete
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

# GET PER ID
def get_employee(employee_id: UUID, db: Session):
    employee = db.query(Employee).filter(Employee.employeeId == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def get_site_config(site_config_id: UUID, db: Session):
    site_config = db.query(SiteConfig).filter(SiteConfig.siteConfigId == site_config_id).first()
    if not site_config:
        raise HTTPException(status_code=404, detail="Site config not found")
    return site_config

def get_address(address_id: UUID, db: Session):
    address = db.query(Address).filter(Address.addressId == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

def get_customer(customer_id: UUID, db: Session):
    customer = db.query(Customer).filter(Customer.customerId == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def get_order(order_id: UUID, db: Session):
    order = db.query(Order).filter(Order.orderId == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.productId == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_route(route_id: UUID, db: Session):
    route = db.query(Route).filter(Route.routeId == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

def get_category(category_id: UUID, db: Session):
    category = db.query(Category).filter(Category.categoryId == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_invoice(invoice_id: UUID, db: Session):
    invoice = db.query(Invoice).filter(Invoice.invoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

def get_cart(cart_id: UUID, db: Session):
    cart = db.query(Cart).filter(Cart.cartId == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def get_categoriesProducts(categoryId: UUID, productId: UUID, db: Session):
    categories = (
        db.query(Category)
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
    
def get_cartsProducts(cartId: UUID, productId: UUID, db: Session):
    carts = (
        db.query(Cart)
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

def get_ordersProducts(orderId: UUID, productId: UUID, db: Session):
    orders = (
        db.query(Order)
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
    
def get_routesOrders(routeId: UUID, orderId: UUID, db: Session):
    routes = (
        db.query(Route)
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
    

def get_categoriesProducts_by_categoryId(categoryId: UUID, db: Session):
    products = (
        db.query(Product)
        .filter(Product.productId.in_(
            db.query(categoriesProducts.c.productId)
            .filter(categoriesProducts.c.categoryId == categoryId)
        ))
        .all()
    )

    if db.query(Category).filter(Category.categoryId == categoryId).first() is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_categoriesProducts_by_productId(productId: UUID, db: Session):
    categories = (
        db.query(Category)
        .filter(Category.categoryId.in_(
            db.query(categoriesProducts.c.categoryId)
            .filter(categoriesProducts.c.productId == productId)
        ))
        .all()
    )
    if db.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories

def get_cartsProducts_by_cartId(cartId: UUID, db: Session):
    products = (
        db.query(Product)
        .filter(Product.productId.in_(
            db.query(cartsProducts.c.productId)
            .filter(cartsProducts.c.cartId == cartId)
        ))
        .all()
    )

    if db.query(Cart).filter(Cart.cartId == cartId).first() is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_cartsProducts_by_productId(productId: UUID, db: Session):
    carts = (
        db.query(Cart)
        .filter(Cart.cartId.in_(
            db.query(cartsProducts.c.cartId)
            .filter(cartsProducts.c.productId == productId)
        ))
        .all()
    )
    if db.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts

def get_ordersProducts_by_orderId(orderId: UUID, db: Session):
    products = (
        db.query(Product)
        .filter(Product.productId.in_(
            db.query(ordersProducts.c.productId)
            .filter(ordersProducts.c.orderId == orderId)
        ))
        .all()
    )

    if db.query(Order).filter(Order.orderId == orderId).first() is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_ordersProducts_by_productId(productId: UUID, db: Session):
    orders = (
        db.query(Order)
        .filter(Order.orderId.in_(
            db.query(ordersProducts.c.orderId)
            .filter(ordersProducts.c.productId == productId)
        ))
        .all()
    )
    if db.query(Product).filter(Product.productId == productId).first() is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_routesOrders_by_routeId(routeId: UUID, db: Session):
    orders = (
        db.query(Order)
        .filter(Order.orderId.in_(
            db.query(routesOrders.c.orderId)
            .filter(routesOrders.c.routeId == routeId)
        ))
        .all()
    )

    if db.query(Route).filter(Route.routeId == routeId).first() is None:
        raise HTTPException(status_code=404, detail="Route not found")
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_routesOrders_by_orderId(orderId: UUID, db: Session):
    routes = (
        db.query(Route)
        .filter(Route.routeId.in_(
            db.query(routesOrders.c.routeId)
            .filter(routesOrders.c.orderId == orderId)
        ))
        .all()
    )
    if db.query(Order).filter(Order.orderId == orderId).first() is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if not routes:
        raise HTTPException(status_code=404, detail="Route not found")
    return routes




# GET ALL
def get_employees(email:str, password:str, db: Session):
    if email is not None and password is not None:
        employees = db.query(Employee).filter(Employee.email == email, Employee.password == password).all()
    elif email is not None and password is None:
        employees = db.query(Employee).filter(Employee.email == email).first()
    else: 
        employees = db.query(Employee).all()
    return employees

def get_site_configs(db: Session):
    site_configs = db.query(SiteConfig).all()
    return site_configs

def get_addresses(db: Session):
    addresses = db.query(Address).all()
    return addresses

def get_customers(db: Session):
    customers = db.query(Customer).all()
    return customers

def get_orders(db: Session):
    orders = db.query(Order).all()
    return orders

def get_products(db: Session):
    products = db.query(Product).all()
    return products

def get_routes(db: Session):
    routes = db.query(Route).all()
    return routes

def get_categories(db: Session):
    categories = db.query(Category).all()
    return categories

def get_invoices(db: Session):
    invoices = db.query(Invoice).all()
    return invoices

def get_carts(db: Session):
    carts = db.query(Cart).all()
    return carts


def get_categoriesProductss(db: Session):
    return db.execute(select(categoriesProducts)).mappings().all()

def get_cartsProductss(db: Session):
    return db.execute(select(cartsProducts)).mappings().all()

def get_ordersProductss(db: Session):
    return db.execute(select(ordersProducts)).mappings().all()




def get_routesOrderss(db: Session):
    return db.execute(select(routesOrders)).mappings().all()


# POST (JUST FOR MOCKUP)
def create_employee(payload: Employee, db: Session):
    employee = Employee(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )
    db.add(employee)
    db.commit()
    return employee.employeeId

def create_site_config(payload: SiteConfig, db: Session):
    site_config = SiteConfig(
        companyName=payload.companyName,
        logoPath=payload.logoPath,
        email=payload.email,
        phoneNumber=payload.phoneNumber,
        companyNumber=payload.companyNumber,
        iban=payload.iban,
        addressId=payload.addressId
    )
    db.add(site_config)
    db.commit()
    return site_config.siteConfigId

def create_address(payload: Address, db: Session):
    address = Address(
        streetName=payload.streetName,
        streetNumber=payload.streetNumber,
        city=payload.city,
        postCode=payload.postCode,
        country=payload.country,
        state=payload.state)
    db.add(address)
    db.commit()
    return address.addressId

def create_customer(payload: Customer, db: Session):
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

    db.add(customer)
    db.commit()
    return customer.customerId

def create_order(payload: Order, db: Session):
    order = Order(
        orderDate=payload.orderDate,
        deliveryDate=payload.deliveryDate,
        customerReference=payload.customerReference,
        orderState=payload.orderState,
        selfCollect=payload.selfCollect,)
    db.add(order)
    db.commit()
    return order.orderId

def create_product(payload: Product, db: Session):
    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        imagePath=payload.imagePath,
        createdAt=payload.createdAt
        )
    db.add(product)
    db.commit()
    return product.productId

def create_route(payload: Route, db: Session):
    route = Route(
        name=payload.name,
    )
    db.add(route)
    db.commit()
    return route.routeId

def create_category(payload: Category, db: Session):
    category = Category(
        name=payload.name,
        imagePath=payload.imagePath
    )
    db.add(category)
    db.commit()
    return category.categoryId

def create_cart(payload: Cart, db: Session):
    cart = Cart(
        customerReference=payload.customerReference,
    )
    db.add(cart)
    db.commit()
    return cart.cartId

def create_invoice(payload: Invoice, db: Session):
    invoice = Invoice(
        orderId=payload.orderId,
        invoiceAmount=payload.invoiceAmount,
        paymentDate=payload.paymentDate,
        pdfUrl=payload.pdfUrl
    )
    db.add(invoice)
    db.commit()
    return invoice.invoiceId

def create_categoriesProducts(categoryId: UUID, productId: UUID, db: Session):
    already_in_category = (
        db.query(categoriesProducts).filter_by(categoryId=categoryId, productId=productId).first()
    )

    if already_in_category:
        raise HTTPException(status_code=400, detail="Already in category")

    product_exists = db.query(Product).filter(Product.productId == productId).first()
    category_exists = db.query(Category).filter(Category.categoryId == categoryId).first()

    if product_exists and category_exists:
        db.execute(categoriesProducts.insert().values(categoryId=categoryId, productId=productId))
        db.commit()
        return productId, categoryId
    else:
        raise HTTPException(status_code=404, detail="Product or category not found")

def create_ordersProducts(productId: UUID, orderId: UUID, productAmount: int, orderDate: datetime, db: Session): 
    product_exists = db.query(Product).filter(Product.productId == productId).first()
    order_exists = db.query(Order).filter(Order.orderId == orderId).first()

    if product_exists and order_exists:
        db.execute(ordersProducts.insert().values(productId=productId, orderId=orderId, productAmount=productAmount, orderDate=orderDate))
        db.commit()
        return productId, orderId, productAmount, orderDate
    else:
        raise HTTPException(status_code=404, detail="Product or order not found")

def create_routesOrders(routeId: UUID, orderId: UUID, db: Session):

        route_exists = db.query(Route).filter(Route.routeId == routeId).first()
        order_exists = db.query(Order).filter(Order.orderId == orderId).first()

        if route_exists and order_exists:
            db.execute(routesOrders.insert().values(routeId=routeId, orderId=orderId))
            db.commit()
            return routeId, orderId
        else:
            raise HTTPException(status_code=404, detail="Route or order not found")

def create_cartsProducts(productId: UUID, cartId: UUID, productAmount: int, db: Session):

        product_exists = db.query(Product).filter(Product.productId == productId).first()
        cart_exists = db.query(Cart).filter(Cart.cartId == cartId).first()

        if product_exists and cart_exists:
            db.execute(cartsProducts.insert().values(productId=productId, cartId=cartId, productAmount=productAmount))
            db.commit()
            return productId, cartId, productAmount
        else:
            raise HTTPException(status_code=404, detail="Product or cart not found")
        


# DELETE BY ID

def delete_employee(employee_id: UUID, db: Session):
    employee = db.query(Employee).filter(Employee.employeeId == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return employee_id

def delete_site_config(config_id: UUID, db: Session):
    site_config = db.query(SiteConfig).filter(SiteConfig.configId == config_id).first()
    if not site_config:
        raise HTTPException(status_code=404, detail="Site config not found")
    db.delete(site_config)
    db.commit()
    return config_id

def delete_address(address_id: UUID, db: Session):
    address = db.query(Address).filter(Address.addressId == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return address_id

def delete_customer(customer_id: UUID, db: Session):
    customer = db.query(Customer).filter(Customer.customerId == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return customer_id

def delete_order(order_id: UUID, db: Session):
    order = db.query(Order).filter(Order.orderId == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return order_id

def delete_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.productId == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product_id

def delete_route(route_id: UUID, db: Session):
    route = db.query(Route).filter(Route.routeId == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(route)
    db.commit()
    return route_id

def delete_category(category_id: UUID, db: Session):
    category = db.query(Category).filter(Category.categoryId == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return category_id

def delete_invoice(invoice_id: UUID, db: Session):
    invoice = db.query(Invoice).filter(Invoice.invoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return invoice_id

def delete_cart(cart_id: UUID, db: Session):
    cart = db.query(Cart).filter(Cart.cartId == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(cart)
    db.commit()
    return cart_id

# DELETE ALL
def delete_employees(db: Session):
    employees = db.query(Employee).all()
    for employee in employees:
        db.delete(employee)
    db.commit()
    return True

def delete_site_configs(db: Session):
    site_configs = db.query(SiteConfig).all()
    for site_config in site_configs:
        db.delete(site_config)
    db.commit()
    return True

def delete_addresses(db: Session):
    addresses = db.query(Address).all()
    for address in addresses:
        db.delete(address)
    db.commit()
    return True

def delete_customers(db: Session):
    customers = db.query(Customer).all()
    for customer in customers:
        db.delete(customer)
    db.commit()
    return True

def delete_orders(db: Session):
    orders = db.query(Order).all()
    for order in orders:
        db.delete(order)
    db.commit()
    return True

def delete_products(db: Session):
    products = db.query(Product).all()
    for product in products:
        db.delete(product)
    db.commit()
    return True

def delete_routes(db: Session):
    routes = db.query(Route).all()
    for route in routes:
        db.delete(route)
    db.commit()
    return True

def delete_categories(db: Session):
    categories = db.query(Category).all()
    for category in categories:
        db.delete(category)
    db.commit()
    return True

def delete_invoices(db: Session):
    invoices = db.query(Invoice).all()
    for invoice in invoices:
        db.delete(invoice)
    db.commit()
    return True

def delete_carts(db: Session):
    carts = db.query(Cart).all()
    for cart in carts:
        db.delete(cart)
    db.commit()
    return True


def delete_ordersProducts(db: Session):
    db.execute(delete(ordersProducts))
    db.commit()
    return True

def delete_categoriesProducts(db: Session):
    db.execute(delete(categoriesProducts))
    db.commit()
    return True

def delete_cartsProducts(db: Session):
    db.execute(delete(cartsProducts))
    db.commit()
    return True
    

## ROLE

def delete_roles(db: Session):
    roles = db.query(Role).all()
    for role in roles:
        db.delete(role)
    db.commit()
    return True

def get_roles(db: Session):
    roles = db.query(Role).all()
    return roles

def get_role(role_id: UUID, db: Session):
    role = db.query(Role).filter(Role.roleId == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

def create_role(payload: Role, db: Session):
    role = Role(
        name=payload.name,
        description=payload.description,
        deleted=payload.deleted
    )
    db.add(role)
    db.commit()
    return role.roleId

def get_role_by_name(name: str, db: Session):
    role = db.query(Role).filter(Role.name == name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role