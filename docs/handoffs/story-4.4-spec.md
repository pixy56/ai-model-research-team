# Dev Team Handoff: Story 4.4 - Distribution System

**Story:** Create system for distributing research briefs via email/Slack  
**Points:** 5  
**Priority:** Medium  
**Dependencies:** Story 4.3 (Complete - first brief generated)

---

## Overview

Create automated distribution system for weekly research briefs. The system should send briefs via email and Slack, manage subscriptions, and track delivery.

---

## Data Sources

### Input
- **Briefs Location:** `briefs/research-brief-YYYY-MM-DD.md`
- **Format:** Markdown with frontmatter metadata
- **Sample:** `briefs/research-brief-2025-04-20.md`

### Brief Structure
```markdown
---
title: AI Model Research Brief - Week of April 20, 2025
week: "2025-W16"
date: "2025-04-20"
version: "1.0"
total_models: 179
new_models: 59
innovation_patterns: 14
paper_findings: 196
---

# Executive Summary
...
```

---

## Requirements

### Functional Requirements

1. **Email Distribution**
   - Send briefs as HTML email
   - Support multiple recipients
   - CC/BCC support
   - Email templates with branding
   - Attachment support (PDF export)

2. **Slack Integration**
   - Post briefs to Slack channels
   - Support for multiple channels
   - Thread-based discussions
   - File upload to Slack
   - @mention support for urgent updates

3. **Subscription Management**
   - Subscribe/unsubscribe via web UI or commands
   - Preference settings (email only, Slack only, both)
   - Frequency options (weekly, monthly)
   - Topic filters (specific labs, architectures)
   - Subscriber database

4. **Archive & Tracking**
   - Archive of all distributed briefs
   - Delivery tracking (sent, opened, clicked)
   - Bounce handling
   - Unsubscribe tracking
   - Analytics dashboard

5. **Automation**
   - Weekly scheduled distribution (Mondays 9am)
   - Manual trigger option
   - Preview before send
   - Draft mode

### Non-Functional Requirements

- **Reliability:** 99.9% delivery rate
- **Security:** Secure credential storage
- **Scalability:** Support 1000+ subscribers
- **Compliance:** GDPR unsubscribe support

---

## Technical Stack

**Backend:**
- Extend existing FastAPI (`src/api/main.py`)
- SQLite for subscriber database
- Celery or APScheduler for scheduling

**Email:**
- SMTP integration (SendGrid, AWS SES, or Mailgun)
- HTML email templates (Jinja2)
- Markdown to HTML conversion

**Slack:**
- Slack Bolt SDK or webhooks
- OAuth for workspace integration

**Frontend (Optional):**
- Subscription management UI
- Admin dashboard

---

## API Endpoints Needed

```
# Distribution
POST /api/distribute/email - Send email distribution
POST /api/distribute/slack - Post to Slack
POST /api/distribute/preview - Preview before sending

# Subscriptions
POST /api/subscribe - Subscribe to briefs
DELETE /api/subscribe/{id} - Unsubscribe
GET /api/subscriptions - List subscriptions
PUT /api/subscriptions/{id} - Update preferences

# Archive
GET /api/briefs - List all briefs
GET /api/briefs/{id} - Get specific brief
GET /api/briefs/{id}/analytics - Delivery analytics

# Automation
POST /api/schedule/weekly - Schedule weekly distribution
DELETE /api/schedule/weekly - Cancel schedule
GET /api/schedule/status - Check schedule status
```

---

## Database Schema

```sql
-- Subscribers table
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    slack_user_id TEXT,
    preferences JSON,  -- {"email": true, "slack": false, "frequency": "weekly"}
    topics JSON,       -- ["openai", "anthropic", "reasoning"]
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    active BOOLEAN DEFAULT true
);

-- Distribution log
CREATE TABLE distributions (
    id INTEGER PRIMARY KEY,
    brief_id TEXT,
    channel TEXT,      -- "email" or "slack"
    recipient TEXT,
    status TEXT,       -- "sent", "delivered", "opened", "bounced"
    sent_at TIMESTAMP,
    opened_at TIMESTAMP,
    error_message TEXT
);

-- Briefs archive
CREATE TABLE briefs_archive (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    week TEXT,
    date TEXT,
    title TEXT,
    sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP
);
```

---

## Configuration

**Environment Variables:**
```bash
# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=xxx
FROM_EMAIL=briefs@ai-research-team.com

# Slack
SLACK_BOT_TOKEN=xoxb-xxx
SLACK_SIGNING_SECRET=xxx
DEFAULT_SLACK_CHANNEL=#ai-research

# App
BASE_URL=https://research-team.example.com
SECRET_KEY=xxx
```

---

## Acceptance Criteria

- [ ] Email distribution system
- [ ] Slack webhook integration
- [ ] Subscription management
- [ ] Archive of distributed briefs
- [ ] Delivery tracking
- [ ] Weekly automation
- [ ] Documentation

---

## Files to Reference

- `briefs/research-brief-2025-04-20.md` - Sample brief format
- `templates/research-brief.md` - Brief template structure
- `src/api/main.py` - Existing API to extend

---

## Notes

- Briefs are markdown files - convert to HTML for email
- Consider PDF generation for email attachments
- Slack messages should be concise with link to full brief
- Use markdown-to-html library (like Python-Markdown or markdown2)
- Test with small group before full distribution

---

**Created:** April 20, 2025  
**Handoff By:** AI Research Team
