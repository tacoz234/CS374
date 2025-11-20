CREATE TABLE "users" (
  "userID" int PRIMARY KEY,
  "name" text,
  "email" text,
  "phone_number" text
);

CREATE TABLE "drivers" (
  "userID" int PRIMARY KEY
);

CREATE TABLE "riders" (
  "userID" int PRIMARY KEY
);

CREATE TABLE "admins" (
  "userID" int PRIMARY KEY
);

CREATE TABLE "cars" (
  "carID" int PRIMARY KEY,
  "ownerID" int,
  "capacity" int,
  "brand" name,
  "color" name
);

CREATE TABLE "ratings" (
  "ratingID" int PRIMARY KEY,
  "score" int,
  "userID" int
);

CREATE TABLE "messages" (
  "messageID" int PRIMARY KEY,
  "rideID" int,
  "senderID" int,
  "content" text,
  "timestamp" datetime
);

CREATE TABLE "rides" (
  "rideID" int PRIMARY KEY,
  "request_time" datetime,
  "pickup_locationID" int,
  "dropoff_locationID" int,
  "status" VARCHAR,
  "riderID" int,
  "driverID" int,
  "num_riders" int,
  "carID" int
);

CREATE TABLE "locations" (
  "locationID" int PRIMARY KEY,
  "address" text,
  "latitude" float,
  "longitude" float
);

COMMENT ON TABLE "users" IS 'Stores basic profile and contact information for all individuals in the system (riders, drivers, and admins).';

COMMENT ON TABLE "drivers" IS 'A subset of the users table, containing records for users who are approved to provide rides.';

COMMENT ON TABLE "riders" IS 'A subset of the users table, containing records for users who request rides.';

COMMENT ON TABLE "admins" IS 'A subset of the users table, containing records for system administrative users.';

COMMENT ON TABLE "cars" IS 'Stores details about vehicles registered and used by drivers in the system.';

COMMENT ON TABLE "ratings" IS 'Stores feedback scores provided by users following a ride.';

COMMENT ON COLUMN "ratings"."score" IS 'The numerical rating given (e.g., 1 to 5 stars).';

COMMENT ON COLUMN "ratings"."userID" IS 'The userID of the user who is being rated (could be a driver or a rider).';

COMMENT ON TABLE "messages" IS 'Stores the real-time communication logs between users (driver and rider) for a given ride.';

COMMENT ON TABLE "rides" IS 'The core transaction table, recording details about every ride request, from initiation to completion.';

COMMENT ON TABLE "locations" IS 'Stores precise location data for all pickup and dropoff points used in the system.';

ALTER TABLE "rides" ADD FOREIGN KEY ("riderID") REFERENCES "riders" ("userID");

ALTER TABLE "rides" ADD FOREIGN KEY ("driverID") REFERENCES "drivers" ("userID");

ALTER TABLE "rides" ADD FOREIGN KEY ("pickup_locationID") REFERENCES "locations" ("locationID");

ALTER TABLE "rides" ADD FOREIGN KEY ("dropoff_locationID") REFERENCES "locations" ("locationID");

ALTER TABLE "admins" ADD FOREIGN KEY ("userID") REFERENCES "users" ("userID");

ALTER TABLE "drivers" ADD FOREIGN KEY ("userID") REFERENCES "users" ("userID");

ALTER TABLE "riders" ADD FOREIGN KEY ("userID") REFERENCES "users" ("userID");

ALTER TABLE "drivers" ADD FOREIGN KEY ("userID") REFERENCES "cars" ("ownerID");

ALTER TABLE "cars" ADD FOREIGN KEY ("carID") REFERENCES "rides" ("carID");

ALTER TABLE "users" ADD FOREIGN KEY ("userID") REFERENCES "ratings" ("userID");

ALTER TABLE "rides" ADD FOREIGN KEY ("rideID") REFERENCES "messages" ("rideID");

ALTER TABLE "users" ADD FOREIGN KEY ("userID") REFERENCES "messages" ("senderID");
