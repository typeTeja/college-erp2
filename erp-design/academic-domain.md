You are a senior frontend engineer working on a College ERP system.

TASK CONTEXT

- The project has legacy frontend code with outdated “Master Data / Master Tabs”.
- Many fields are renamed, removed, or no longer available.
- Backend APIs are already refactored and MUST be treated as locked and final.
- Only the Academic domain is in scope.
- Backend endpoints, request/response contracts, and validations MUST NOT be changed.

OBJECTIVE
Refactor the frontend Academic Master modules to fully align with the new backend APIs by:

1. Removing all legacy endpoints from the frontend.
2. Updating frontend URLs to use ONLY the new backend academic endpoints.
3. Mapping renamed fields correctly based on backend responses.
4. Removing UI fields that are no longer supported by backend.
5. Ensuring all CRUD operations work end-to-end from frontend.

IN-SCOPE MODULES (Academic Domain)

- Program / Course Master
- Academic Batch Master
- Year & Semester Structure
- Section Master
- Practical Batch / Lab Group Master
- Subject Master (Theory / Practical / Audit)
- Regulation-linked academic masters (read-only where applicable)

STRICT RULES

- DO NOT modify backend code, schemas, or endpoints.
- DO NOT create mock fields or fake payloads.
- DO NOT keep backward compatibility for legacy frontend APIs.
- Frontend must fail fast if backend rejects a request.
- Use backend response shape as the single source of truth.

REFRACTORING STEPS

1. Scan the frontend Academic Master codebase and list:
   - Legacy API endpoints in use
   - Legacy field names
   - Unused or deprecated UI fields
2. Replace all legacy endpoints with new academic endpoints provided by backend.
3. Update API service layer:
   - Base URLs
   - HTTP methods
   - Request payloads
   - Response typings
4. Update forms and tables:
   - Rename fields to match backend contract
   - Remove unsupported fields
   - Mark backend-required fields as mandatory in UI
5. Ensure full CRUD support:
   - Create → success toast + refresh list
   - Read → paginated or hierarchical display
   - Update → patch/put with correct IDs
   - Delete → soft/hard delete as per backend support
6. Validate error handling:
   - Show backend validation errors clearly
   - No silent failures
7. Remove:
   - Dead code
   - Legacy API utilities
   - Old enums/constants not used by backend

OUTPUT EXPECTATIONS

- Clean, backend-aligned frontend Academic Master modules
- No references to legacy endpoints
- Type-safe API integration
- Stable CRUD flows
- Ready for QA testing without backend changes

ASSUME

- Backend follows REST conventions
- API responses are authoritative
- Academic hierarchy is Program → Batch → Year → Semester → Section → Practical Batch → Subject

Deliver refactored frontend code and explain key changes briefly.
