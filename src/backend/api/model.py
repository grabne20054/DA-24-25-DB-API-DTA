from datetime import datetime
from pydantic import BaseModel
from enum import Enum as pyenum
import uuid

class Role(str, pyenum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    SUPPLIER = "supplier"
    
class Sector(str, pyenum):
    AGRICULTURE = "agriculture"
    CONSTRUCTION = "construction"
    EDUCATION = "education"
    FINANCE = "finance"
    HEALTH = "health"
    IT = "it"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    TRANSPORTATION = "transportation"
    TOURISM = "tourism"
    HOSPITALITY = "hospitality"
    TECHONOLOGY = "technology"
    OTHER = "other"

class OrderState(str, pyenum):
    ORDER_PLACED = "order_placed"
    ORDER_COLLECTED = "order_collected"
    IN_PROGRESS = "in_progress"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"


class Employee(BaseModel):
    firstName: str
    lastName: str
    password: str
    email: str
    role: Role
    deleted: bool


class EmployeeDB(Employee):
    employeeId: uuid.UUID

class SiteConfig(BaseModel):
    companyName: str
    logoPath: str
    email: str
    phoneNumber: str
    companyNumber: str
    iban: str
    addressId: uuid.UUID
    modifiedAt: datetime | None
    deleted: bool

class SiteConfigDB(SiteConfig):
    siteConfigId: uuid.UUID

class Address(BaseModel):
    streetName: str
    streetNumber: str
    city: str
    postCode: str
    country: str
    state: str
    modifiedAt: datetime | None
    deleted: bool

class AddressDB(Address):
    addressId: uuid.UUID

class AddressGeocodes(AddressDB):
    latitude: float
    longitude: float

class Customer(BaseModel):
    customerReference: int
    firstName: str
    lastName: str
    email: str
    password: str
    phoneNumber: str
    companyNumber: str
    signedUp: datetime
    role: Role
    businessSector: Sector
    addressId: uuid.UUID
    modifiedAt: datetime | None
    deleted: bool
    avatarPath: str

class CustomerDB(Customer):
    customerId: uuid.UUID
    customerReference: int

class Order(BaseModel):
    orderDate: datetime
    deliveryDate: datetime | None
    customerReference: int
    deleted: bool
    orderState: OrderState
    selfCollect: bool

class OrderDB(Order):
    orderId: uuid.UUID

class Product(BaseModel):
    name: str
    description: str
    price: int
    stock: int
    imagePath: str
    modifiedAt: datetime | None
    deleted: bool
    createdAt: datetime

class ProductDB(Product):
    productId: uuid.UUID


class Route(BaseModel):
    name: str
    deleted: bool

class RouteDB(Route):
    routeId: uuid.UUID

class Category(BaseModel):
    name: str
    imagePath: str
    deleted: bool

class CategoryDB(Category):
    categoryId: uuid.UUID

class Cart(BaseModel):
    customerReference: int

class CartDB(Cart):
    cartId: uuid.UUID

class Invoice(BaseModel):
    orderId: uuid.UUID
    invoiceAmount: int
    paymentDate: datetime | None
    deleted: bool
    pdfUrl: str

class InvoiceDB(Invoice):
    invoiceId: uuid.UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
