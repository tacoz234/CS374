from typing import Optional
import datetime

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, REAL, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_appbuilder import Model




class Affiliation(Model):
    __tablename__ = 'affiliation'
    __table_args__ = (
        PrimaryKeyConstraint('org_name', name='affiliation_pkey'),
    )

    org_name: Mapped[str] = mapped_column(Text, primary_key=True)
    website: Mapped[str] = mapped_column(Text, nullable=False)
    country: Mapped[str] = mapped_column(Text, nullable=False)

    person_affiliation: Mapped[list['PersonAffiliation']] = relationship('PersonAffiliation', back_populates='affiliation')


class Conference(Model):
    __tablename__ = 'conference'
    __table_args__ = (
        PrimaryKeyConstraint('year', name='conference_pkey'),
    )
    def __str__(self):
      return f"Conference {self.year} at {self.location}"

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    location: Mapped[str] = mapped_column(Text, nullable=False)

    papers: Mapped[list['Paper']] = relationship('Paper', back_populates='conference')


class Person(Model):
    __tablename__ = 'person'
    __table_args__ = (
        PrimaryKeyConstraint('email', name='person_pkey'),
    )

    email: Mapped[str] = mapped_column(Text, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)

    paper: Mapped[list['Paper']] = relationship('Paper', back_populates='person')
    person_affiliation: Mapped[list['PersonAffiliation']] = relationship('PersonAffiliation', back_populates='person')
    paper_author: Mapped[list['PaperAuthor']] = relationship('PaperAuthor', back_populates='person')


class Superheroes(Model):
    __tablename__ = 'superheroes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='superheroes_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hero_name: Mapped[str] = mapped_column(Text, nullable=False)
    secret_identity: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[float] = mapped_column(REAL, nullable=False)
    height: Mapped[float] = mapped_column(REAL, nullable=False)
    nick_name: Mapped[str] = mapped_column(Text, nullable=False)

    supervillains: Mapped[list['Supervillains']] = relationship('Supervillains', back_populates='main_hero')


class Topic(Model):
    __tablename__ = 'topic'
    __table_args__ = (
        PrimaryKeyConstraint('topic_id', name='topic_pkey'),
    )
    def __str__(self):
      return f"Topic #{self.topic_id}: {self.topic_name}"

    topic_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    topic_name: Mapped[str] = mapped_column(Text, nullable=False)

    papers: Mapped[list['Paper']] = relationship('Paper', secondary='paper_topic', back_populates='topics')
    reviewer: Mapped[list['Reviewer']] = relationship('Reviewer', secondary='expertise', back_populates='topic')


class Paper(Model):
    __tablename__ = 'paper'
    __table_args__ = (
        ForeignKeyConstraint(['contact_email'], ['person.email'], name='paper_contact_email_fkey'),
        ForeignKeyConstraint(['year'], ['conference.year'], name='paper_year_fkey'),
        PrimaryKeyConstraint('paper_id', name='paper_pkey')
    )
    def __str__(self):
      return f"Paper #{self.paper_id}: {self.title}"

    paper_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=False)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    contact_email: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    person: Mapped['Person'] = relationship('Person', back_populates='paper')
    conference: Mapped['Conference'] = relationship('Conference', back_populates='papers')
    topics: Mapped[list['Topic']] = relationship('Topic', secondary='paper_topic', back_populates='papers')
    history: Mapped[list['History']] = relationship('History', back_populates='paper')
    paper_author: Mapped[list['PaperAuthor']] = relationship('PaperAuthor', back_populates='paper')
    review: Mapped[list['Review']] = relationship('Review', back_populates='paper')
    


class PersonAffiliation(Model):
    __tablename__ = 'person_affiliation'
    __table_args__ = (
        ForeignKeyConstraint(['email'], ['person.email'], name='person_affiliation_email_fkey'),
        ForeignKeyConstraint(['org_name'], ['affiliation.org_name'], name='person_affiliation_org_name_fkey'),
        PrimaryKeyConstraint('email', 'org_name', name='person_affiliation_pkey')
    )

    email: Mapped[str] = mapped_column(Text, primary_key=True)
    org_name: Mapped[str] = mapped_column(Text, primary_key=True)
    from_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    to_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    person: Mapped['Person'] = relationship('Person', back_populates='person_affiliation')
    affiliation: Mapped['Affiliation'] = relationship('Affiliation', back_populates='person_affiliation')


class Reviewer(Person):
    __tablename__ = 'reviewer'
    __table_args__ = (
        ForeignKeyConstraint(['email'], ['person.email'], name='reviewer_email_fkey'),
        PrimaryKeyConstraint('email', name='reviewer_pkey')
    )

    email: Mapped[str] = mapped_column(Text, primary_key=True)
    phone: Mapped[Optional[str]] = mapped_column(Text)

    topic: Mapped[list['Topic']] = relationship('Topic', secondary='expertise', back_populates='reviewer')
    review: Mapped[list['Review']] = relationship('Review', back_populates='reviewer')


class Supervillains(Model):
    __tablename__ = 'supervillains'
    __table_args__ = (
        ForeignKeyConstraint(['main_hero_id'], ['superheroes.id'], name='supervillains_main_hero_id_fkey'),
        PrimaryKeyConstraint('id', name='supervillains_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    villain_name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[float] = mapped_column(REAL, nullable=False)
    height: Mapped[float] = mapped_column(REAL, nullable=False)
    main_hero_id: Mapped[int] = mapped_column(Integer, nullable=False)

    main_hero: Mapped['Superheroes'] = relationship('Superheroes', back_populates='supervillains')


t_expertise = Table(
    'expertise', Model.metadata,
    Column('email', Text, primary_key=True),
    Column('topic_id', Integer, primary_key=True),
    ForeignKeyConstraint(['email'], ['reviewer.email'], name='expertise_email_fkey'),
    ForeignKeyConstraint(['topic_id'], ['topic.topic_id'], name='expertise_topic_id_fkey'),
    PrimaryKeyConstraint('email', 'topic_id', name='expertise_pkey')
)


class History(Model):
    __tablename__ = 'history'
    __table_args__ = (
        ForeignKeyConstraint(['paper_id'], ['paper.paper_id'], name='history_paper_id_fkey'),
        PrimaryKeyConstraint('paper_id', 'timestamp', name='history_pkey')
    )
    def __str__(self):
      return f"History for #{self.paper_id} at {self.timestamp}"

    paper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    paper_status: Mapped[str] = mapped_column(Enum('SUBMITTED', 'UNDER_REVIEW', 'REVISION', 'RESUBMITTED', 'REJECTED', 'ACCEPTED', 'PUBLISHED', name='status'), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    paper: Mapped['Paper'] = relationship('Paper', back_populates='history')


class PaperAuthor(Model):
    __tablename__ = 'paper_author'
    __table_args__ = (
        ForeignKeyConstraint(['email'], ['person.email'], name='paper_author_email_fkey'),
        ForeignKeyConstraint(['paper_id'], ['paper.paper_id'], name='paper_author_paper_id_fkey'),
        PrimaryKeyConstraint('paper_id', 'email', name='paper_author_pkey')
    )

    paper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(Text, primary_key=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False, comment='author order')

    person: Mapped['Person'] = relationship('Person', back_populates='paper_author')
    paper: Mapped['Paper'] = relationship('Paper', back_populates='paper_author')


t_paper_topic = Table(
    'paper_topic', Model.metadata,
    Column('paper_id', Integer, primary_key=True),
    Column('topic_id', Integer, primary_key=True),
    ForeignKeyConstraint(['paper_id'], ['paper.paper_id'], name='paper_topic_paper_id_fkey'),
    ForeignKeyConstraint(['topic_id'], ['topic.topic_id'], name='paper_topic_topic_id_fkey'),
    PrimaryKeyConstraint('paper_id', 'topic_id', name='paper_topic_pkey')
)


class Review(Model):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(['email'], ['reviewer.email'], name='review_email_fkey'),
        ForeignKeyConstraint(['paper_id'], ['paper.paper_id'], name='review_paper_id_fkey'),
        PrimaryKeyConstraint('paper_id', 'email', name='review_pkey'),
        {'comment': 'Scores range from 1 to 5'}
    )

    paper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(Text, primary_key=True)
    merit: Mapped[int] = mapped_column(Integer, nullable=False)
    relevance: Mapped[int] = mapped_column(Integer, nullable=False)
    readability: Mapped[int] = mapped_column(Integer, nullable=False)
    originality: Mapped[int] = mapped_column(Integer, nullable=False)
    author_comments: Mapped[str] = mapped_column(Text, nullable=False)
    committee_comments: Mapped[Optional[str]] = mapped_column(Text)

    reviewer: Mapped['Reviewer'] = relationship('Reviewer', back_populates='review')
    paper: Mapped['Paper'] = relationship('Paper', back_populates='review')
