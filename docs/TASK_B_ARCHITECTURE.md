**# Page Pulse - Scalable Architecture Design**



**## Overview**



**Page Pulse is a URL auditing platform that checks website availability,**

**response time, HTML metadata, and performance metrics.**



**The system is designed to handle:**



**- 10,000 audits per day**

**- 500 concurrent requests**

**- Customer-facing SLA requirements**

**- High availability and fault tolerance**





**# 1. Architecture Design**





**## High Level Architecture**





&#x20;                    **Users / Clients**

&#x20;                          **|**

&#x20;                          **|**

&#x20;                          **v**



&#x20;                    **API Gateway**

&#x20;                          **|**

&#x20;                          **|**

&#x20;                          **v**



&#x20;               **FastAPI Audit Service**

&#x20;                          **|**

&#x20;         **+----------------+----------------+**

&#x20;         **|                                 |**

&#x20;         **v                                 v**



&#x20;   **Redis Cache                     Rate Limiter**

&#x20;         **|**

&#x20;         **|**

&#x20;         **v**



&#x20;   **Audit Queue (Redis/RabbitMQ)**

&#x20;         **|**

&#x20;         **|**

&#x20;         **v**



&#x20;  **Background Workers**

&#x20;         **|**

&#x20;         **|**

&#x20;         **v**



&#x20;   **External Websites**





&#x20;         **|**

&#x20;         **v**



&#x20;   **PostgreSQL Database**





&#x20;         **|**

&#x20;         **v**



&#x20; **Monitoring + Logging Stack**



**---**



**# Components**





**## 1. API Gateway**



**Responsibilities:**



**- Request routing**

**- Authentication**

**- SSL termination**

**- Traffic management**





**Technology:**



**- Nginx**

**- AWS Application Load Balancer**





**---**



**## 2. FastAPI Audit Service**



**Responsibilities:**



**- Accept audit requests**

**- Validate URLs**

**- Generate request IDs**

**- Return audit results**





**Technology:**



**- Python FastAPI**

**- Uvicorn workers**





**---**



**## 3. Cache Layer**



**Purpose:**



**Avoid repeated website requests.**



**Example:**



**User audits:**





**https://google.com**





**First request:**





**API -> Website -> Cache Store**





**Second request:**





**API -> Cache -> Response**







**Technology:**



**- Redis**





**Cache configuration:**





**TTL = configurable**

**Default = 300 seconds**







**---**



**## 4. Queue System**





**Problem:**



**500 concurrent users can overload external websites.**





**Solution:**



**Use asynchronous queue processing.**





**Flow:**





**Request**

**|**

**v**

**Queue**

**|**

**v**

**Worker**

**|**

**v**

**Website Audit**







**Technology:**



**- RabbitMQ / Redis Queue**





**---**



**## 5. Worker Service**





**Responsibilities:**



**- Execute website audits**

**- Handle retries**

**- Manage failures**





**Technology:**



**- Celery workers**

**- Python async workers**





**---**



**## 6. Database**





**Stores:**



**- Audit history**

**- User information**

**- API usage**

**- Performance metrics**





**Technology:**



**- PostgreSQL**





**---**



**# Data Flow**





**1. User sends URL audit request.**



**2. API Gateway receives request.**



**3. FastAPI validates URL.**



**4. System checks Redis cache.**



**5. If cached:**





**Return cached result**







**6. If not cached:**





**Send job to queue**





**7. Worker performs website audit.**



**8. Result stored:**





**Redis Cache**

**+**

**PostgreSQL**





**9. API returns response.**





**---**



**# 2. Technology Decision Record**





**## FastAPI**



**Chosen:**



**FastAPI**





**Reason:**



**- High performance**

**- Async support**

**- Automatic Swagger documentation**

**- Python ecosystem**





**Rejected:**



**Django**





**Reason:**



**- More overhead**

**- Less suitable for lightweight APIs**





**---**





**## Redis Cache**



**Chosen:**



**Redis**





**Reason:**



**- Extremely fast**

**- TTL support**

**- Handles high traffic**





**Rejected:**



**Local memory cache**





**Reason:**



**- Not shared between multiple servers**





**---**





**## RabbitMQ Queue**



**Chosen:**



**RabbitMQ**





**Reason:**



**- Reliable message delivery**

**- Supports retries**





**Rejected:**



**Direct background tasks**





**Reason:**



**- Cannot handle large workloads**





**---**





**## PostgreSQL**



**Chosen:**



**PostgreSQL**





**Reason:**



**- Reliable relational database**

**- Strong consistency**





**Rejected:**



**MongoDB**





**Reason:**



**- Audit data has structured relationships**





**---**





**# 3. Failure Mode Analysis**





**## Failure 1: External Website Timeout**





**Problem:**



**Target website does not respond.**





**Impact:**



**Audit request fails.**





**Mitigation:**



**- HTTP timeout**

**- Retry mechanism**

**- Circuit breaker**





**---**





**## Failure 2: High Traffic Burst**





**Problem:**



**500 concurrent requests overload service.**





**Impact:**



**Slow responses.**





**Mitigation:**



**- Queue based processing**

**- Rate limiting**

**- Horizontal scaling**





**---**





**## Failure 3: Cache Failure**





**Problem:**



**Redis unavailable.**





**Impact:**



**More requests reach external websites.**





**Mitigation:**



**- Cache fallback**

**- Redis replication**

**- Monitoring alerts**





**---**





**# 4. Observability Plan**





**## Metrics**





**Monitor:**



**- API response time**

**- Request count**

**- Error percentage**

**- Queue length**

**- Cache hit ratio**

**- Worker failures**





**Tools:**



**- Prometheus**

**- Grafana**





**---**





**## Logging**





**Structured logs include:**







**request\_id**

**timestamp**

**endpoint**

**status\_code**

**response\_time**

**error\_message**







**Tool:**



**- ELK Stack**





**---**





**# Alerting**





**Alerts:**





**## High Error Rate**



**Trigger:**





**5xx errors > 5%**







**## High Latency**



**Trigger:**





**Response time > SLA limit**







**## Queue Delay**



**Trigger:**





**Queue length increasing continuously**







**---**





**# Rollback Strategy**





**Deployment Process:**







**Developer**

**|**

**v**

**GitHub**

**|**

**v**

**CI Tests**

**|**

**v**

**Docker Build**

**|**

**v**

**Production Deployment**







**Rollback:**





**1. Detect unhealthy deployment.**



**2. Stop new traffic.**



**3. Restore previous stable version.**



**4. Verify health checks.**



**5. Resume traffic.**





**Deployment tools:**



**- Docker**

**- Kubernetes**

**- Blue-Green Deployment**





**---**



**# Conclusion**





**This architecture allows Page Pulse to scale from a single FastAPI service**

**to a production distributed auditing platform capable of handling**

**10,000+ audits per day with reliability and observability.**

