"""Generate fake data for the Conference Review System."""
__author__ = "Cole Determan"

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from faker import Faker

from models import Base, Affiliation, Conference, Person, Topic, Paper, PersonAffiliation, Reviewer, History, PaperAuthor, Review

import datetime
import random


def main():
    engine = create_engine("postgresql+psycopg://determsc:113893504@data.cs.jmu.edu/sec1", echo=False, future=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    random.seed(42)
    faker = Faker("en_US")
    Faker.seed(42)

    with Session(engine) as session:
        session.execute(text("""
            TRUNCATE TABLE
                paper_topic,
                expertise,
                review,
                history,
                paper_author,
                person_affiliation,
                paper,
                reviewer,
                topic,
                person,
                affiliation,
                conference
            RESTART IDENTITY CASCADE
        """))
        session.commit()
        persons: list[Person] = []
        reviewers: list[Reviewer] = []
        base_persons: list[Person] = []
        used_emails: set[str] = set()

        def unique_person_email(first: str, last: str) -> str:
            while True:
                domain = random.choice(["example.com", "university.edu", "research.org", "mail.com"])
                email = f"{first.lower()}.{last.lower()}@{domain}"
                if email in used_emails:
                    email = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@{domain}"
                if email not in used_emails:
                    used_emails.add(email)
                    return email

        for _ in range(5):
            first = faker.first_name()
            last = faker.last_name()
            email = unique_person_email(first, last)
            p = Person(email=email, first_name=first, last_name=last)
            persons.append(p)
            base_persons.append(p)

        for _ in range(5):
            first = faker.first_name()
            last = faker.last_name()
            email = unique_person_email(first, last)
            phone = faker.phone_number()
            r = Reviewer(email=email, first_name=first, last_name=last, phone=phone)
            reviewers.append(r)
            persons.append(r)

        session.add_all(persons)
        session.commit()

        affiliations = []
        for _ in range(4):
            org = faker.unique.company()
            website = f"https://{faker.domain_name()}"
            country = faker.country()
            affiliations.append(Affiliation(org_name=org, website=website, country=country))
        session.add_all(affiliations)
        session.commit()

        pa_rows: list[PersonAffiliation] = []
        pa_pairs: set[tuple[str, str]] = set()
        while len(pa_rows) < 8:
            p = random.choice(persons)
            a = random.choice(affiliations)
            key = (p.email, a.org_name)
            if key in pa_pairs:
                continue
            pa_pairs.add(key)
            start_date = faker.date_between(datetime.date(2015, 1, 1), datetime.date(2023, 12, 31))
            to_date = None
            if random.random() < 0.7:
                to_date = faker.date_between(start_date, datetime.date(2024, 12, 31))
            pa_rows.append(PersonAffiliation(email=p.email, org_name=a.org_name, from_date=start_date, to_date=to_date))
        session.add_all(pa_rows)
        session.commit()

        conf = Conference(year=2024, location=f"{faker.city()}, {faker.state_abbr()}")
        session.add(conf)
        session.commit()

        topics = []
        seen_names = set()
        while len(topics) < 20:
            base = faker.word().title()
            suffix = random.choice(["Computing", "Systems", "Engineering", "Analytics", "Security", "Robotics", "Vision", "Learning", "Mining", "Privacy"])
            name = f"{base} {suffix}"
            if name not in seen_names:
                seen_names.add(name)
                topics.append(Topic(topic_name=name))
        session.add_all(topics)
        session.commit()

        papers: list[Paper] = []
        for i in range(3):
            contact = random.choice(base_persons)
            title = faker.sentence(nb_words=random.randint(3, 6)).rstrip(".")
            abstract = "\n".join(faker.paragraphs(nb=random.randint(2, 4)))
            filename = f"paper_{i + 1}.pdf"
            ppr = Paper(
                title=title,
                abstract=abstract,
                filename=filename,
                contact_email=contact.email,
                year=conf.year,
            )
            papers.append(ppr)
        session.add_all(papers)
        session.commit()

        pauth_rows: list[PaperAuthor] = []
        ranks_per_paper = {0: [1, 2, 3], 1: [1, 2, 3], 2: [1, 2]}
        for idx, ranks in ranks_per_paper.items():
            selected_authors = random.sample(base_persons, k=len(ranks))
            for rank, person in zip(ranks, selected_authors):
                pauth_rows.append(PaperAuthor(paper=papers[idx], person=person, rank=rank))
        session.add_all(pauth_rows)
        session.commit()

        reviews: list[Review] = []
        chosen_reviewers = random.sample(reviewers, k=3)
        for i, reviewer in enumerate(chosen_reviewers):
            reviews.append(
                Review(
                    paper=papers[i],
                    reviewer=reviewer,
                    merit=random.randint(3, 5),
                    relevance=random.randint(3, 5),
                    readability=random.randint(3, 5),
                    originality=random.randint(3, 5),
                    author_comments=faker.sentence(nb_words=6),
                    committee_comments=random.choice([None, faker.sentence(nb_words=8)]),
                )
            )
        session.add_all(reviews)
        session.commit()

        histories: list[History] = []
        base_time = datetime.datetime(2024, 6, 1, 10, 0, 0)
        staged_statuses = [
            ["SUBMITTED", "UNDER_REVIEW"],
            ["SUBMITTED", "REJECTED"],
            ["SUBMITTED"],
        ]
        for idx, status_seq in enumerate(staged_statuses):
            t = base_time
            for status in status_seq:
                histories.append(History(paper=papers[idx], timestamp=t, paper_status=status, notes=None))
                t = t + datetime.timedelta(days=7)
        while len(histories) < 5:
            histories.append(
                History(
                    paper=papers[2],
                    timestamp=base_time + datetime.timedelta(days=14),
                    paper_status="UNDER_REVIEW",
                    notes="External review scheduled.",
                )
            )
        session.add_all(histories)
        session.commit()

        for reviewer in reviewers:
            assigned_ids = set()
            while len(assigned_ids) < 2:
                tpc = random.choice(topics)
                if tpc.topic_id not in assigned_ids:
                    assigned_ids.add(tpc.topic_id)
                    reviewer.topic.append(tpc)
        session.commit()

        for paper in papers:
            assigned_ids = set()
            while len(assigned_ids) < 3:
                tpc = random.choice(topics)
                if tpc.topic_id not in assigned_ids:
                    assigned_ids.add(tpc.topic_id)
                    paper.topic.append(tpc)
        session.commit()

        print("Data generation complete.")
        print("Database URL:", engine.url)


if __name__ == "__main__":
    main()