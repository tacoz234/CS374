"""Example code from the ORM Quick Start.

https://docs.sqlalchemy.org/en/20/orm/quickstart.html
"""

from typing import List, Optional
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

# ------------------------------------------------------------------------------
# Declare Models
# ------------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# ------------------------------------------------------------------------------
# Create an Engine / Emit CREATE TABLE DDL
# ------------------------------------------------------------------------------

engine = create_engine("sqlite://", echo=True)

Base.metadata.create_all(engine)

# ------------------------------------------------------------------------------
# Create Objects and Persist
# ------------------------------------------------------------------------------

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

# ------------------------------------------------------------------------------
# Simple SELECT / SELECT with JOIN
# ------------------------------------------------------------------------------

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
for user in session.scalars(stmt):
    print(user)

stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(stmt).one()
print(sandy_address)

# ------------------------------------------------------------------------------
# Make Changes / Some Deletes
# ------------------------------------------------------------------------------

stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()

patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

session.commit()

sandy = session.get(User, 2)
assert sandy is not None
sandy.addresses.remove(sandy_address)

session.flush()
session.delete(patrick)
session.commit()
