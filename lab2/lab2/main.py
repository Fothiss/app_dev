user_product_association = Table(
    'user_product_association', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
    Column('purchased_at', DateTime, default=datetime.now)
)

class User(Base):
    products: Mapped[List["Product"]] = relationship(
        "Product", 
        secondary=user_product_association,
        back_populates="users"
    )