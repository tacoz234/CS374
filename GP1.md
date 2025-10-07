---

# **SafeRide Connect: JMU Saferides Database Application**

Team Name: DukeDrive

Project Name: SafeRide Connect

## **Introduction**

The problem of drunk driving is a persistent and dangerous one, especially on college campuses. While many students are aware of the risks, they may not have safe, convenient, and reliable transportation options available. This often leads to poor decisions with potentially fatal consequences. The goal of this project, **SafeRide Connect**, is to create a comprehensive database application that **streamlines and improves the existing James Madison University (JMU) Saferides program**.

Our vision is to create a user-friendly system that facilitates communication between students who need a ride and the volunteer drivers who provide the service. By centralizing ride requests, driver availability, and historical data, our solution will make the Saferides program more **efficient, reliable, and accessible**. This will ultimately benefit all stakeholders: students will have a safer way to get home, volunteer drivers will have a more organized and manageable system, and the broader community will be safer due to reduced instances of impaired driving.

---

## **Primary System Entities and Data Structure**

The database schema is built around core entities that manage user profiles, ride logistics, and performance tracking. The structure uses a centralized users table with specialized tables (drivers, riders, admins) to define user roles.

### **Core Entities**

| Entity (Table) | Purpose | Key Attributes |
| :---- | :---- | :---- |
| **users** | Stores basic profile and contact information for all individuals. | userID (PK), name, email, phone\_number |
| **rides** | The core transaction table, recording details about every ride request from initiation to completion. | rideID (PK), riderID, driverID, request\_time, status, carID |
| **locations** | Stores precise location data for all pickup and dropoff points used in the system. | locationID (PK), address, latitude, longitude |

### **Supporting Entities**

| Entity (Table) | Purpose | Key Relationships |
| :---- | :---- | :---- |
| **drivers** | A subset of users for individuals approved to provide rides. | One-to-one relationship with users (userID) |
| **riders** | A subset of users for individuals who request rides. | One-to-one relationship with users (userID) |
| **admins** | A subset of users for system administrative users. | One-to-one relationship with users (userID) |
| **cars** | Stores details about vehicles registered and used by drivers. | Linked to drivers via ownerID |
| **ratings** | Stores feedback scores provided by users following a ride. | Linked to users via userID (the user being rated) |
| **messages** | Stores real-time communication logs between users (driver and rider) for a given ride. | Linked to rides via rideID and users via senderID |

---

## **Primary System Users**

Our application is designed for three distinct user types, with separate interaction requirements and, notably, distinct dashboards for drivers and riders.

### **Students (Riders)**

* **Role:** Current JMU students who need a safe ride.  
* **Interaction:** Primarily use the application to **request a ride**, view the status of their request, and see the details of their assigned driver. They input their pickup and drop-off locations, and their experience with the data is limited to their **personal ride history**.

### **Volunteer Drivers**

* **Role:** Vetted JMU students or faculty who provide rides.  
* **Interaction:** Use the application's **Driver Dashboard** to view a list of available ride requests, accept a request, and update the ride status (e.g., "en route," "arrived," "completed"). They can see their personal ride history and contribution statistics, enabling potential incentive programs.

### **Administrators** 

* **Role:** Responsible for managing and overseeing the Saferides program.  
* **Interaction:** Have full access to all data within the system to **monitor real-time activity**, generate reports on program usage, manage user accounts, and verify driver credentials. They use the data to identify peak hours, high-traffic areas, and potential system bottlenecks.

---

## **System Functionality**

### **1\. Ride Management and Dispatch**

This feature is the core of the application, focused on connecting students with drivers in an efficient and timely manner, supported by the **rides** and **locations** tables.

* A student user can request a ride by providing their current location and desired destination.  
* The system displays a list of available ride requests to all logged-in and available drivers.  
* A driver user can select and accept a pending ride request, updating the ride status in the database.  
* The **messages** table facilitates real-time communication between the assigned driver and rider.  
* The driver updates the ride status (e.g., "picked up," "completed") as they progress, finalizing the ride record.

### **2\. User and System Analytics**

Leveraging data from the **rides**, **users**, and **ratings** tables, this feature provides valuable insights into the program's usage and efficiency.

* Administrators view a dashboard displaying **real-time statistics**, such as the number of active rides, available drivers, and average wait times.  
* The system generates reports on **historical ride data** (e.g., total number of rides completed on a given night or week).  
* The application displays the most popular pickup and drop-off locations based on past ride data.  
* Driver users can view their personal ride history and contribution statistics via their Driver Dashboard.

---

## **About the Team**

**Cole Determan:** I am a senior Computer Science major minoring in Data Analytics. I currently work a part time job at ManTech as a Technical Intern. I plan to pursue an accelerated masters at Virginia Tech. I have knowledge in javascript, html, and CSS, as well as SQL which will be useful for this project.

**Ben Berry:** I am a senior Computer Science major. Some recent CS courses I have taken are computer systems 2, intro to autonomous robots, application development and applied algorithms. I have knowledge in javascript, html, and CSS which may be useful for visualizing data in this project.

**Sergio Vavra:** I am a senior Computer Science major minoring in Italian. I currently work part time at 2 jobs, one as a site manager at UREC, and another as an AI/ML developer at Ellucian. The skills I’ve learned as a developer will be useful in writing readable and quality code, as well as the work I’ve done with databases.

