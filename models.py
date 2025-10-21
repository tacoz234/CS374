from typing import Optional
import datetime
import decimal

from sqlalchemy import CHAR, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Part(Base):
    __tablename__ = 'part'
    __table_args__ = (
        PrimaryKeyConstraint('p_partkey', name='part_pkey'),
    )

    p_partkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    p_name: Mapped[str] = mapped_column(String(55), nullable=False)
    p_mfgr: Mapped[str] = mapped_column(CHAR(25), nullable=False)
    p_brand: Mapped[str] = mapped_column(CHAR(10), nullable=False)
    p_type: Mapped[str] = mapped_column(String(25), nullable=False)
    p_size: Mapped[int] = mapped_column(Integer, nullable=False)
    p_container: Mapped[str] = mapped_column(CHAR(10), nullable=False)
    p_retailprice: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    p_comment: Mapped[str] = mapped_column(String(23), nullable=False)

    partsupp: Mapped[list['Partsupp']] = relationship('Partsupp', back_populates='part')


class Region(Base):
    __tablename__ = 'region'
    __table_args__ = (
        PrimaryKeyConstraint('r_regionkey', name='region_pkey'),
    )

    r_regionkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    r_name: Mapped[str] = mapped_column(CHAR(25), nullable=False)
    r_comment: Mapped[Optional[str]] = mapped_column(String(152))

    nation: Mapped[list['Nation']] = relationship('Nation', back_populates='region')


class Nation(Base):
    __tablename__ = 'nation'
    __table_args__ = (
        ForeignKeyConstraint(['n_regionkey'], ['region.r_regionkey'], name='nation_fk1'),
        PrimaryKeyConstraint('n_nationkey', name='nation_pkey')
    )

    n_nationkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    n_name: Mapped[str] = mapped_column(CHAR(25), nullable=False)
    n_regionkey: Mapped[int] = mapped_column(Integer, nullable=False)
    n_comment: Mapped[Optional[str]] = mapped_column(String(152))

    region: Mapped['Region'] = relationship('Region', back_populates='nation')
    customer: Mapped[list['Customer']] = relationship('Customer', back_populates='nation')
    supplier: Mapped[list['Supplier']] = relationship('Supplier', back_populates='nation')


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        ForeignKeyConstraint(['c_nationkey'], ['nation.n_nationkey'], name='customer_fk1'),
        PrimaryKeyConstraint('c_custkey', name='customer_pkey')
    )

    c_custkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    c_name: Mapped[str] = mapped_column(String(25), nullable=False)
    c_address: Mapped[str] = mapped_column(String(40), nullable=False)
    c_nationkey: Mapped[int] = mapped_column(Integer, nullable=False)
    c_phone: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    c_acctbal: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    c_mktsegment: Mapped[str] = mapped_column(CHAR(10), nullable=False)
    c_comment: Mapped[str] = mapped_column(String(117), nullable=False)

    nation: Mapped['Nation'] = relationship('Nation', back_populates='customer')
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='customer')


class Supplier(Base):
    __tablename__ = 'supplier'
    __table_args__ = (
        ForeignKeyConstraint(['s_nationkey'], ['nation.n_nationkey'], name='supplier_fk1'),
        PrimaryKeyConstraint('s_suppkey', name='supplier_pkey')
    )

    s_suppkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    s_name: Mapped[str] = mapped_column(CHAR(25), nullable=False)
    s_address: Mapped[str] = mapped_column(String(40), nullable=False)
    s_nationkey: Mapped[int] = mapped_column(Integer, nullable=False)
    s_phone: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    s_acctbal: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    s_comment: Mapped[str] = mapped_column(String(101), nullable=False)

    nation: Mapped['Nation'] = relationship('Nation', back_populates='supplier')
    partsupp: Mapped[list['Partsupp']] = relationship('Partsupp', back_populates='supplier')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['o_custkey'], ['customer.c_custkey'], name='orders_fk1'),
        PrimaryKeyConstraint('o_orderkey', name='orders_pkey')
    )

    o_orderkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    o_custkey: Mapped[int] = mapped_column(Integer, nullable=False)
    o_orderstatus: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    o_totalprice: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    o_orderdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    o_orderpriority: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    o_clerk: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    o_shippriority: Mapped[int] = mapped_column(Integer, nullable=False)
    o_comment: Mapped[str] = mapped_column(String(79), nullable=False)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='orders')
    lineitem: Mapped[list['LineItem']] = relationship('Lineitem', back_populates='orders')


class Partsupp(Base):
    __tablename__ = 'partsupp'
    __table_args__ = (
        ForeignKeyConstraint(['ps_partkey'], ['part.p_partkey'], name='partsupp_fk2'),
        ForeignKeyConstraint(['ps_suppkey'], ['supplier.s_suppkey'], name='partsupp_fk1'),
        PrimaryKeyConstraint('ps_partkey', 'ps_suppkey', name='partsupp_pkey')
    )

    ps_partkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    ps_suppkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    ps_availqty: Mapped[int] = mapped_column(Integer, nullable=False)
    ps_supplycost: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    ps_comment: Mapped[str] = mapped_column(String(199), nullable=False)

    part: Mapped['Part'] = relationship('Part', back_populates='partsupp')
    supplier: Mapped['Supplier'] = relationship('Supplier', back_populates='partsupp')
    lineitem: Mapped[list['LineItem']] = relationship('Lineitem', back_populates='partsupp')


class LineItem(Base):
    __tablename__ = 'lineitem'
    __table_args__ = (
        ForeignKeyConstraint(['l_orderkey'], ['orders.o_orderkey'], name='lineitem_fk1'),
        ForeignKeyConstraint(['l_partkey', 'l_suppkey'], ['partsupp.ps_partkey', 'partsupp.ps_suppkey'], name='lineitem_fk2'),
        PrimaryKeyConstraint('l_orderkey', 'l_linenumber', name='lineitem_pkey')
    )

    l_orderkey: Mapped[int] = mapped_column(Integer, primary_key=True)
    l_partkey: Mapped[int] = mapped_column(Integer, nullable=False)
    l_suppkey: Mapped[int] = mapped_column(Integer, nullable=False)
    l_linenumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    l_quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    l_extendedprice: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    l_discount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    l_tax: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    l_returnflag: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    l_linestatus: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    l_shipdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    l_commitdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    l_receiptdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    l_shipinstruct: Mapped[str] = mapped_column(CHAR(25), nullable=False)
    l_shipmode: Mapped[str] = mapped_column(CHAR(10), nullable=False)
    l_comment: Mapped[str] = mapped_column(String(44), nullable=False)

    orders: Mapped['Orders'] = relationship('Orders', back_populates='lineitem')
    partsupp: Mapped['Partsupp'] = relationship('Partsupp', back_populates='lineitem')
