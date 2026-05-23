**Feedo**

# **Product Overview**

Feedo is a web app that recommends personalized cat food for multi-cat households. Each cat gets individual recommendations based on age, weight, health conditions, and learned food preferences.

## **Problem**

Two cats in the same household have different nutritional needs. Most owners feed them the same food because there is no tool to help them decide otherwise.

## **Core Loop**

**Onboarding:**

1. User creates a profile for each cat (age, weight, health conditions) as part of the onboarding flow

2. During onboarding: user picks 3 foods each cat likes, 3 each cat dislikes

   * **Cyclical Loop:**

3. App recommends cat food matched to each cat's nutritional requirements

4. User gives feedback (cat liked/ignored/vomited), which helps recommendations improve over time

**Final Step:**

5. Purchase links go through the Chewy Affiliate Program (4% commission)

## **Tech Stack**

| Layer | Technology |
| :---- | :---- |
| Frontend | React \+ TypeScript, Apollo Client, Shadcn, React Router v6 |
| Backend | Python \+ Django \+ Strawberry（Python‘s GraphQL library） |
| Database | PostgreSQL |
| Cache | Redis — cache recommendation results per cat profile |
| AI | Claude Code \+ Codex |
| Food data (MVP) | Open Pet Food Facts (free, open API) |
| Pet Preference Data (MVP)  | Semantic Findings From Message Boards/Chilean dataset if possible |
| Food data (post-MVP) | Chewy Affiliate product feed (free after approval) |
| Commerce | Chewy Affiliate via Partnerize — 4% commission, 15-day cookie |
| Deployment | Docker |

## **Constraints**

* **Budget:** Zero spend until revenue. Free tiers and open source only.

* **No medical claims:** App cannot assess cat health or give medical advice.

* **No veterinary data:** No publicly accessible clinical datasets exist. Any feature requiring this is out of scope.

* **ML-ready schema:** Data collected in MVP must support ML later without schema changes.

## **Non-Goals**

* Health diagnosis or symptom triage is permanently out of scope

* Passive monitoring (audio, camera) — platform limitations make this unviable

* Dogs, birds, or any non-cat species

* Own e-commerce — Chewy handles fulfillment

* Mobile app, real-time features, social features, internationalization

* Multi-user households at MVP — schema hook exists (cats.household\_id), feature deferred

# **Frontend Architecture**

Input food preference, health record, and create a UI element that is most helpful for this

## **Structure**

lib/

  apollo.ts      ← ApolloClient setup, replace axios

  queries/       ← .graphql files or gql\`\` tagged queries

    cats.ts

    foods.ts

    recommendations.ts

  mutations/

    cats.ts

    events.ts

    auth.ts

## **State Management**

**Server state:** Apollo Client 

**Client state:** React Context \+ useState/useReducer

## **Auth Token Storage**

* **access\_token:** memory only

* **refresh\_token:** httpOnly cookie — JS cannot access

* Apollo Client link handles silent token refresh on 401

## **TypeScript**

* Strict mode enabled — no types

* All API responses have defined interfaces

* Discriminated unions for loading/error/success states

## **Key Patterns**

Refer to the frontend skill 

# **Backend Architecture**

## **Structure**

feedo/

  apps/

    cats/

    foods/

    recommendations/

  core/

    auth/          

    schema.py

    settings.py

    urls.py

## **Auth**

* Self-implemented JWT — access token (15 min) \+ refresh token (30 days)

* Refresh tokens stored in DB with revoked\_at — supports explicit logout

* No third-party auth service — kept in-house for learning and cost

# **Data**

GraphQL via Strawberry (backend) and Apollo Client (frontend). Single /graphql/ endpoint.

Rationale: A single endpoint simplifies routing. Frontend queries exactly what it needs — no over-fetching. Strawberry integrates cleanly with Django ORM and Python type hints.  
Consequences:

- No REST routes — single /graphql/ endpoint only  
- Each app has schema.py with types, queries, mutations  
- core/schema.py merges all app schemas  
- Apollo Client replaces axios on the frontend

## **Matching Engine \-- Stage 1 (MVP)**

* Taking in the onboarding data, as well as the data from the preferences of the cat that people add I want a matching algorithm that takes their preferences, ie. Flavor, Texture, Meat, Health, Diseases, Age, etc. And suggests food based on the matching algorithm   
  * For example age filter the possible results by Kitty vs Adult cat food as metrics etc.  
  * For example Disease filter, match food benefiical for diseaes ie. renal, heart health based on their conditon  
* Determine the priority for each of the conditions and preferences that is adjustable, ie weightings or a ranking. Allow a human to modify them. 

### **Recommendation Scoring**

Recommendations use deterministic additive scoring.

Example scoring model:

Base score \= 0

\+40 life\_stage match  
\+30 condition support  
\+15 preferred protein  
\+10 preferred texture  
\+8 bowl\_finished history  
\-50 bowl\_ignored  
\-100 vomited\_after  
\-25 explicit\_negative

**Scoring Rules**

\- Hard exclusions remove foods before scoring  
\- Scores are additive, not multiplicative  
\- Maximum score capped at 100  
\- Negative scores allowed internally  
\- Tie-breaker: higher protein match count, then random shuffle  
\- Recommendation engine is deterministic except exploration logic

**Condition Mapping Rules**

Conditions never directly generate recommendations. They map to required and excluded nutritional tags.

Example mappings:

\`\`\`yaml  
renal:  
  required\_tags:  
    \- low\_phosphorus  
    \- kidney\_support  
  avoid\_tags:  
    \- high\_sodium

urinary:  
  required\_tags:  
    \- urinary\_support  
    \- hydration\_support

weight\_management:  
  required\_tags:  
    \- low\_calorie  
    \- high\_protein  
\`\`\`

Mappings are manually curated and versioned.  
LLMs never generate condition mappings dynamically.

## **Recommendation Engine — Stage 2 (MVP)**

Rules-based. No ML. Runs at request time.

* Hard filter: life\_stage match (computed from born\_at), conditions → required food\_tags  
* Exclusion: remove foods appearing in explicit\_negative cat\_events  
* Boost: score up foods appearing in explicit\_positive and bowl\_finished cat\_events  
* Sort by score, return top 10, pass to Claude for natural language explanation, or create a defined set of outputs to return per suggestion, pre-mapped   
* Add a random selection based on the score to suggest to users a random food to try for their kitty   
* Prioritize sort by health condition and preference of cat, recommendations that a user is inclined to pick based on their love for their cat   
* Potentially evaluate cost vs quantity as a metric to suggest cat food 

## **Recommendation Engine — Stage 2 (post-MVP)**

Collaborative filtering

* triggered when enough users have enough events,   
* find cats with similar event histories,   
* Recommend foods liked by similar cats not yet tried,   
* no new tables needed

## **SQL Policy**

* Django ORM for standard CRUD

* Use SqlAlchemy for sql methods, all available methods and django orm methodsData Pipeline

**Data Pipeline:** 

## **Food Catalog Seeding (pre-launch, one-time)**

6. Pull 300-500 cat food records from Open Pet Food Facts API

   GET https://world.openfoodfacts.org/cgi/search.pl

       ?tagtype\_0=categories\&tag\_0=cat-food\&json=1\&page\_size=500

7. Batch job: Claude will build a function based on the data shape to extract primary\_protein \+ texture from the ingredients list

8. GenerateFoodFeatureVectorJob: builds feature\_json from food\_attributes columns

9. Manual QA on the top 20 brands

10. Seed into foods \+ food\_attributes \+ food\_tags

\# Food Ingestion Pipeline

Open Pet Food Facts data is treated as untrusted raw input.

Pipeline stages:

\`\`\`txt

Raw API

→ normalize

→ validate

→ enrich

→ dedupe

→ persist

\`\`\`

\#\# Normalization

Normalize:

\- brand names

\- ingredient casing

\- units

\- texture labels

\- protein labels

Examples:

\`\`\`txt

"ROYAL CANIN"

"Royal Canin®"

→ Royal Canin

\`\`\`

\#\# Validation

Reject foods missing:

\- product name

\- ingredient list

\- life stage metadata

\#\# Enrichment

Background jobs extract:

\- primary protein

\- texture

\- wet/dry classification

\- nutritional tags

\#\# Deduplication

Foods are deduplicated by:

\- normalized brand

\- normalized product name

\- package size

## **feature\_json Format**

Auto-generated. Never written manually. Used by Stage 2 recommendation engine.

{

  "protein": 0.32,  "fat": 0.18,  "is\_wet": 1,

  "is\_chicken": 1,  "is\_pate": 0,  "is\_chunks": 1

}

## **Post-MVP: Chewy Affiliate Product Feed**

* Apply to Chewy Affiliate Program (Partnerize) after MVP ships — requires live app

* Feed replaces OPFF as primary data source — more complete, official data

* foods.external\_ids jsonb already stores source IDs — no schema change needed

  \-- no schema change needed

  UPDATE food\_attributes SET data\_source \= 'chewy\_feed', last\_synced\_at \= NOW()

    WHERE food\_id IN (SELECT id FROM foods WHERE external\_ids ? 'chewy');

## **Event Collection (ongoing)**

cat\_events is append-only. Every user interaction writes an event. This is the training data for future ML.

| Event Type | Trigger | ML Signal |
| :---- | :---- | :---- |
| explicit\_positive | Onboarding — user marks food as liked | Strong positive |
| explicit\_negative | Onboarding — user marks food as disliked | Strong negative |
| bowl\_finished | User logs cat finished the bowl | Positive |
| bowl\_ignored | User logs cat did not eat | Negative |
| vomited\_after | User logs cat vomited after eating | Strong negative |
| recommendation\_clicked | User clicks through to Chewy | Weak positive |
| recommendation\_dismissed | User dismisses recommendation | Weak negative |

# **Database Schema**

## **Design Principles**

* Separate tables by rate of change, not conceptual category

* Store raw events, not derived conclusions — events are immutable facts

* Nullable FKs and jsonb as forward-compat hooks — future migrations should be additive only

* born\_at not age\_months — age is derived and goes stale

* Time series for weight — need trend data, not just current value

## **Tables**

| Table | Purpose | Key Design Note |
| :---- | :---- | :---- |
| users | Auth and identity | password\_hash, is\_verified boolean |
| refresh\_tokens | JWT refresh token store | revoked\_at nullable — null means valid |
| cats | Cat identity | household\_id nullable (forward compat), born\_at not age |
| cat\_measurements | Weight time series | Separate table — need historical trend data |
| cat\_conditions | Health conditions | resolved\_at nullable — null means currently active |
| cat\_events | Append-only behavior log | NEVER update or delete. No updated\_at column. |
| foods | Product identity | external\_ids jsonb — supports OPFF \+ Chewy \+ others |
| food\_attributes | Nutritional \+ ML features | feature\_json jsonb auto-generated by background job |
| food\_tags | Searchable tags | Separate table — better indexing than array column |
| recommendations | Generated recommendations | metadata jsonb — stores model\_version, score, reasoning |
| recommendation\_feedbacks | Feedback on recommendations | Also writes to cat\_events on submit |

## **Domain Taxonomy**

All recommendation logic, ingestion, filtering, and ML features must use canonical enums and normalized tags.

No freeform strings are used internally for:

\- texture

\- protein

\- life stage

\- conditions

\- event types

\- nutritional tags

### **Texture Enum**

export enum Texture {

  Pate \= "pate",

  Shredded \= "shredded",

  ChunksInGravy \= "chunks\_in\_gravy",

  Minced \= "minced",

  Mousse \= "mousse",

  DryKibble \= "dry\_kibble",

}

export enum Protein {

  Chicken \= "chicken",

  Tuna \= "tuna",

  Salmon \= "salmon",

  Turkey \= "turkey",

  Beef \= "beef",

  Duck \= "duck",

  Rabbit \= "rabbit",

}

export enum LifeStage {

  Kitten \= "kitten",

  Adult \= "adult",

  Senior \= "senior",

}

Conditions map to canonical internal tags only.

Unsupported conditions are stored but ignored by recommendation logic until mapped.

## **Forward Compat Hooks**

| Future Feature | Hook in Schema Now |
| :---- | :---- |
| Multi-user households | cats.household\_id — nullable bigint |
| Multiple food data sources | foods.external\_ids — jsonb |
| ML model versioning | recommendations.metadata — jsonb |
| Content-based filtering | food\_attributes.feature\_json — jsonb |
| Collaborative filtering | cat\_events append-only log |
| Email verification | users.is\_verified — boolean |
| Token revocation | refresh\_tokens.revoked\_at — nullable |

# **Product Scope**

Three possible directions considered: (1) health/symptom triage, (2) passive behavior monitoring, (3) food recommendation. Food recommendation only. Health diagnosis and passive monitoring were rejected.

**Alternatives**

### **Health diagnosis/symptom triage**

* No real veterinary training data exists publicly — all open datasets are synthetic or contaminated

* SAVSNET (8M+ real records) is not publicly accessible

* Legal liability for wrong health guidance is not acceptable

### **Passive monitoring (Alexa, phone mic)**

* Alexa Sound Detection API supports 6 hardcoded sounds only — no custom sounds possible

* Alexa Routines Kit deprecated May 2026

* Always-on phone microphone requires foreground service — bad UX, battery drain

### **Food recommendation**

* WSAVA and AAFCO nutritional standards are public and authoritative

* Clear user pain with no existing solution

* Natural affiliate commercial model

**Rationale**

Food recommendation is the only direction that has available data, no legal risk, and a clear commercial model.

**Consequences**

* Health features are permanently out of scope

* Nutritional standards (WSAVA, AAFCO) are the core knowledge base

* Commercial model is affiliate, not subscription

# **Cat Food Data Source**

Need a food catalog with product name, brand, food type, macronutrients, and ingredients before the app can make recommendations. Chewy affiliate approval requires a live app — chicken-and-egg.

Open Pet Food Facts (OPFF) for MVP. Chewy Affiliate product feed post-MVP.

**Alternatives**

| Source | Cost | Quality | Available Now |
| :---- | :---- | :---- | :---- |
| OPFF | Free | Variable | Yes |
| Chewy Affiliate feed | Free (post-approval) | High | No — need live app first |
| Unwrangle Chewy API | Paid | High | Yes |
| Manual curation | Time | High | Yes — QA only |

**Rationale**

OPFF is the only free option available before launch. foods.external\_ids jsonb stores source IDs — switching to Chewy feed post-MVP requires no schema changes.

**Consequences**

* OPFF missing primary\_protein and texture — extract from ingredients via Claude batch job

* Some incomplete nutrition data at launch — acceptable

* Apply for Chewy Affiliate immediately after launch

# **Commerce Model**

Chewy Affiliate Program via Partnerize. 4% commission on all sales. 15-day cookie. Apply after MVP ships.

**Alternatives**

| Model | Gain | Give Up |
| :---- | :---- | :---- |
| Chewy Affiliate (chosen) | Revenue \+ free product data | Dependent on Chewy terms |
| Subscription | Higher LTV | Requires validated product first |
| Advertising | Easy | Bad UX, misaligned incentives |
| Amazon Affiliate | Broader catalog | Lower pet commission than Chewy |

**Rationale**

Affiliate adds minimal implementation complexity and gives us the product feed data as a side benefit. Revenue is tied to recommendation quality — incentives are aligned.

**Consequences**

* foods.chewy\_url stores affiliate link

* Apply immediately after MVP ships

# **AI Layer**

Recommendations need natural language explanations. Options: rules only, fine-tuned model, or general LLM with context.

**Decision**

Rules-based filtering first. Anthropic API (Claude) for natural language explanation only. System prompt contains WSAVA/AAFCO nutritional standards.

\#\#\# Explanation Contract

Claude never receives raw database rows directly.

Recommendation explanations use a structured payload:

\`\`\`json

{

  "food\_name": "Fancy Feast Chicken Pate",

  "matched\_conditions": \["renal\_support"\],

  "matched\_preferences": \["chicken", "pate"\],

  "excluded\_reasons": \[\],

  "confidence": 0.82

}

\`\`\`

Claude converts structured recommendation facts into natural language.

LLM output must never introduce:

\- medical claims

\- unsupported nutritional claims

\- unmapped health reasoning

# **Event Sourcing for User Behavior**

Need to track user behavior to improve recommendations. Two approaches: store derived state ('cat dislikes fish') or store raw events.

**Decision**

cat\_events as an append-only event log. No updated\_at. Never update or delete rows.

**Alternatives**

* Mutable preference table — can't recompute with different logic once data is overwritten. Rejected.

* Event table \+ materialized view — adds complexity not needed at MVP scale; add later if needed.

* Separate tables for implicit vs explicit — event\_type column achieves same result with less complexity.

**Rationale**

Raw events are immutable facts. Derived conclusions (liked/disliked) are interpretations that change as recommendation logic improves. Storing events means we can recompute any derived state at any time with any logic — this is the training dataset for Stage 2 and Stage 3 ML.

**Consequences**

* cat\_events is the single source of truth for all behavioral signals

* All feedback UI writes to cat\_events in addition to recommendation\_feedbacks

* Never add updated\_at to cat\_events

# **food\_attributes as Single Table**

Initial design had two tables: food\_nutrition (protein %, fat %, etc.) and food\_features (primary protein, texture, moisture level). Both are 1:1 with foods. Both come from the same sources and update on the same cadence.

**Decision**

Merge into single food\_attributes table. food\_tags remains separate (many-to-many).

**Rationale**

Two 1:1 tables with the same update cadence add join complexity with no architectural benefit. feature\_json is auto-generated by GenerateFoodFeatureVectorJob after every food\_attributes update — it is the ML feature vector and should never be written manually.

**Consequences**

* GenerateFoodFeatureVectorJob runs after every food\_attributes update

* food\_tags remains separate — many-to-many, different structure, better indexing than array column

# **Auth**

Need user authentication. Options range from third-party services to self-implemented. Self-implemented JWT in Django. Access token (15 min) \+ refresh token (30 days, stored in DB).

**Alternatives**

* Auth0 / Clerk — removes auth as a learning opportunity. Rejected.

* django+strawberry— good option, can refactor to this later once the pattern is understood.

* Django session auth — doesn't work well for React SPA \+ API architecture.

**Rationale**

Auth is one of the most educational backend topics. Implementing it from scratch covers password hashing, token lifecycle, security tradeoffs, and DB design. Third-party services skip all of that.

**Consequences**

* access\_token: memory only on frontend — never localStorage (XSS risk)

* refresh\_token: httpOnly cookie — JS cannot access

* refresh\_tokens table with revoked\_at — supports explicit logout

* Email verification and password reset deferred to post-MVP

# **Recommendation Engine**

Three recommendation stages planned: rules → content-based filtering → collaborative filtering. What to build for MVP.Rules-based engine for MVP. cat\_events collects training data from day one for future stages.

**Alternatives**

| Stage | Trigger | Method | New Tables |
| :---- | :---- | :---- | :---- |
| Stage 1 (MVP) | Day one | Rules-based | None |
| Stage 2 | \>=50 events per cat | Collaborative filtering on cat\_events | None |

**Rationale**

ML needs data. At zero events, ML has nothing to learn. Rules give good recommendations from day one using structured cat profile data. All three stages read the same tables — switching to ML requires no schema changes.

**Consequences**

* cat\_events collects (cat\_id, food\_id, event\_type) from day one — Stage 2 training data ready

* recommendations.metadata jsonb stores model\_version — rules\_v1 now

* Raw SQL required for recommendation queries — intentional, not ORM shortcut

# **Open Questions**

* Email verification at launch — or is\_verified stays false for all MVP users?

* Minimum food catalog size for useful recommendations? (Suggested: 100+)

* UI pattern for multi-cat feedback — how does user specify which cat they are giving feedback for?

* Handling foods mentioned by user that are not in the database

* Deployment target: Railway vs Render vs Fly.io — decide before Week 2