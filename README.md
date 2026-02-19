
## Personalized Learning Progress & Recommendation System

##  Overview

 Personalized Learning Progress & Recommendation System is a full-stack web application that tracks student performance through quizzes and provides intelligent learning recommendations based on performance analysis.

The system evaluates quiz scores, calculates performance percentages, and categorizes students into learning levels (Beginner, Intermediate, Advanced). Based on this classification, it suggests appropriate topics to improve learning outcomes.

This project demonstrates the practical integration of frontend development, backend APIs, database design, and machine learning into an educational platform.

---

 ##  Key Features

* Student login and user creation
* Quiz-based performance evaluation
* Automated score calculation
* Progress tracking system
* Machine learning-based level classification
* Personalized topic recommendations
* Persistent data storage using SQLite

---

## Tech Stack:

## Frontend:

* HTML
* CSS
* JavaScript

## Backend:

* Python (Flask Framework)

## Machine Learning:

* Scikit-learn (KMeans clustering)

## Database:

* SQLite



##  How It Works

1. Student logs in using name and email.
2. Student attempts the quiz.
3. Quiz results are stored in the database.
4. System calculates performance percentage.
5. Based on performance:

   * Below 40% → Beginner
   * 40% to 75% → Intermediate
   * Above 75% → Advanced
6. Personalized learning recommendations are generated.
7. Student can view historical progress and improvement.

---

##  Database Structure

The system consists of three main tables:

## Users

* id (Primary Key)
* name
* email

## Quiz Attempts

* id (Primary Key)
* user_id (Foreign Key)
* topic
* score
* total
* date

## Recommendations

* id (Primary Key)
* user_id (Foreign Key)
* level
* recommended_topic
* difficulty
* created




##  Future Enhancements

* Secure authentication with password & JWT
* Admin analytics dashboard
* Cloud database integration
* Performance visualization graphs





