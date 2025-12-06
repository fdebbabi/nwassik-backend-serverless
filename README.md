# Nwassik Store - Serverless Backend

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [AWS Services Architecture](#️-aws-services-architecture)
- [API Endpoints](#-api-endpoints)

---

## 🎯 Project Overview

**Nwassik Store** is a reverse marketplace platform that connects people who need products or services (Requesters) with people who can fulfill those needs (Providers). The platform focuses on enabling cross-border transactions, particularly between Tunisia and France, where users can request items for purchase and delivery from abroad, items to be picked from one place and delivered to another, or purchasing online services that are not available locally.

### The Main Problem We Solve

- **High import costs**: Tunisian residents face expensive tariffs on imported goods
- **Travelers with spare capacity**: People traveling between countries have unused luggage space
- **Unavailable goods**: Get products or services that are not available locally
- **Peer-to-peer trust**: Connecting verified individuals for mutual benefit
- **Flexible services**: From physical goods (medecines, documents, perfumes,..) to online services (subscriptions, tickets, etc.)

### How It Works (Main Workflow)

1. Registration and login using:
    - Email/password
    - Social sites: Facebook + Google  
2. **Requesters** post what they need:
    - 3 Request types:
      - Buy & Deliver service
        - Users specify what items they want bought and to where should be delivered
      - Pickup & Deliver service
        - Users specify from where items should be picked, and to where should be delivered
      - Online service
        - Users specify what online service they need (Netflix, plane ticket,..) and meetup location for transaction
    - A due date can also be specified indicating the final deadline for completing the request (Possible for all kind of requests)
3. **Providers** browse public requests and offer to fulfill them
    - Support request type, location and due date filtering
4. **Negotiation** happens via private chat messaging
    - This reduces platform liability
5. **Transaction** occurs offline with cash on delivery (future: monetization via online payments)

---

## Backend Stack

| Dev Component        | Purpose                                      |
|----------------------|----------------------------------------------|
| **Language**         | Python 3.11                                  |
| **Deployment**       | Serverless Framework v4                      |
| **ORM**              | SQLAlchemy 2.0.44                            |
| **Model validation** | Pydantic 2.11+                               |
| **Linter**           | Ruff (strict rules)                          |
| **Testing**          | unittest, pytest, moto (AWS service mocking) |

## 🏗️ AWS services Architecture

### Current Usage

| AWS Service              | Purpose                                                             | Configuration   | Notes |
|--------------------------|---------------------------------------------------------------------|-----------------|-------|
| **AWS Lambda**           | Backend API handlers                                                | Python 3.11     | -     |
| **API Gateway**          | REST API endpoints                                                  | -               | -     |
| **RDS (PostgreSQL)**     | Application database                                                | PostgreSQL 15.x | -     |
| **AWS Secrets Manager**  | Credentials storage                                                 | -               | -     |
| **AWS Cognito**          | User authentication (JWT tokens)                                    | -               | -     |
| **CloudWatch Logs**      | All application components Logs, Metrics, Alarms (Lambdas, RDS, ..) | -               | -     |
| **Serverless Framework** | deployment tool                                                     | Framework v4    | -     |
| **Step Functions**       | Orchestrate multi-step workflows                                    | -               | -     |
| **S3**                   | Image storage (profiles, requests)                                  | -               | -     |
| **EventBridge**          | Schedule tasks, route events                                        | -               | -     |
| **SQS**                  | Message queuing, async processing                                   | -               | -     |
| **SNS**                  | Notifications (email, SMS, push)                                    | -               | -     |
| **DynamoDB**             | Chat messages, connections, sessions                                | -               | -     |
| **Rekognition**          | Image moderation, face detection                                    | -               | -     |
| **Comprehend**           | Text moderation, sentiment analysis                                 | -               | -     |
| **X-Ray**                | Tracing all Lambda invocations                                      | -               | -     |
| **CloudWatch**           | Metrics, dashboards, alarms                                         | -               | -     |
| **CloudTrail**           | Audit all API calls: logging, compliance                            | -               | -     |
| **Config**               | Track resources configurations                                      | -               | -     |
| **Batch**                | Scheduled analytics jobs                                            | -               | -     |
| **Lambda@Edge**          | Edge-level rate limiting                                            | -               | -     |
| **ElastiCache (Redis)**  | Distributed rate limit counters                                     | -               | -     |
| **RDS Proxy**            | Connection pooling, failover                                        | -               | -     |
| **CloudFront**           | CDN for images, static assets                                       | -               | -     |
| **WAF**                  | Web application firewall  + DDoS protection and rate limiting       | -               | -     |
| **GuardDuty**            | Threat detection                                                    | -               | -     |
| **KMS**                  | Encryption key management                                           | -               | -     |

---

## 📡 API Endpoints

| Method | Endpoint                               | Auth | Description                                   | Status |
|--------|----------------------------------------|------|-----------------------------------------------|--------|
| GET    | `/health`                              | ❌    | Health check                                  | ✅      |
| GET    | `/requests`                            | ❌    | List all requests (public)                    | ✅      |
| POST   | `/requests`                            | ✅    | Create new request                            | ✅      |
| GET    | `/requests/{id}`                       | ❌    | Get single request                            | ✅      |
| GET    | `/users/{user_id}/requests`            | ❌    | List user's requests                          | ✅      |
| PATCH  | `/requests/{id}`                       | ✅    | Update request (owner only)                   | ✅      |
| DELETE | `/requests/{id}`                       | ✅    | Delete request (owner only)                   | ✅      |
| POST   | `/favorites`                           | ✅    | Add favorite                                  | ✅      |
| GET    | `/favorites`                           | ✅    | List user's favorites                         | ✅      |
| DELETE | `/favorites/{id}`                      | ✅    | Remove favorite (owner only)                  | ✅      |
| POST   | `/users/profile/picture`               | ✅    | Get pre-signed URL for profile picture upload | ❌      |
| GET    | `/users/{user_id}/profile`             | ❌    | Get user profile with ratings                 | ❌      |
| POST   | `/requests/{id}/images`                | ✅    | Get pre-signed URLs for request image upload  | ❌      |
| GET    | `/conversations`                       | ✅    | List user's conversations                     | ❌      |
| GET    | `/conversations/{request_id}`          | ✅    | Get conversation messages                     | ❌      |
| POST   | `/conversations/{request_id}/messages` | ✅    | Send message (REST fallback)                  | ❌      |
| POST   | `/reports`                             | ✅    | Report user/request/message                   | ❌      |
| POST   | `/ratings`                             | ✅    | Rate user after transaction                   | ❌      |
| GET    | `/notifications/settings`              | ✅    | Get notification preferences                  | ❌      |
| PUT    | `/notifications/settings`              | ✅    | Update notification preferences               | ❌      |
| GET    | `/offers`                              | ❌    | List provider offers                          | ❌      |
| POST   | `/offers`                              | ✅    | Create provider offer                         | ❌      |

---

## 🎯 Implementation Status

| Feature                                | Status | Notes                                                                                                                                                       |
|----------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Request CRUD operations**            | ⏳      | Handlers needs review, unit tests needed. Allow users to upload a maximum of two images per request                                                         |
| **Favorites/bookmarks system**         | ⏳      | Handlers needs review, unit tests needed                                                                                                                    |
| **Database schema**                    | ⏳      | Models needs review, need validation tests                                                                                                                  |
| **Testing infrastructure**             | ⏳      | Setup pytest, write unit tests for repos/handlers                                                                                                           |
| **Monitoring and alerting**            | ⏳      | CloudWatch dashboards, alarms, X-Ray tracing                                                                                                                |
| **Content moderation**                 | ⏳      | Text and image moderation with Comprehend/Rekognition           (Users can report inappropriate or fraudulent requests/offers.  )                           |
| **Profile image uploads**              | ⏳      | Support profile images, with moderation                                                                                                                     |
| **API rate limiting**                  | ⏳      | Throttling and quota management                                                                                                                             |
| **Multi-Channel Notifications system** | ⏳      | Email, SMS, push notifications via SNS   (Notify users when a new request is posted and allow subscription to filters (service type, location, date, etc.)) |
| **Chat/messaging system**              | ⏳      | Real-time WebSocket chat with DynamoDB                                                                                                                      |
| **User profile management**            | ⏳      | View/edit profiles, verification badges (Users can verify their phone, email, or ID to increase trust, with a blue mark for verified users.)                |
| **Trust and safety features**          | ⏳      | Reporting, verification, trust scores                                                                                                                       |
| **E2E tests**                          | ⏳      | Full system integration tests (after all features)                                                                                                          |
| **CI/CD pipeline**                     | ⏳      | Automated testing and deployment                                                                                                                            |
| **JWT authentication**                 | ⏳      | Cognito with email/password, Facebook, Google OAuth                                                                                                         |
| **Platform Feedback**                  | ⏳      | Users can provide feedback with text and image for me                                                                                                       |
| **Current Offers/Commong things page** | ⏳      | Separate page displaying all current offers.                                                                                                                |
| **Money Exchange Officer**             | ⏳      | Add a trusted fund handler for secure money exchange and transactions                                                                                       |
| **Requester Money Reservation**        | ⏳      | Add users payment via edinar or something to garantee payment                                                                                               |
