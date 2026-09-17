# Day 02

## Goal

Extend ASM beyond application discovery and start identifying security-relevant attack surfaces.

## Completed

- Admin Endpoint Discovery
- Upload Endpoint Discovery
- Database Discovery
- Environment Variable Discovery
- Risk Classification Engine

## Example Findings

Admin Routes:
- GET /admin
- DELETE /admin/user/:id

Upload Routes:
- POST /upload/image
- POST /upload/document

Environment Variables:
- DATABASE_URL
- JWT_SECRET
- AWS_ACCESS_KEY
- STRIPE_SECRET_KEY

## Learnings

Application understanding requires more than route enumeration.

High-risk surfaces can be identified using contextual security signals.

## Next

Attack Surface Graph

Attack Path Generation

Reachability Analysis