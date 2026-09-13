import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.units import inch

def draw_header(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(HexColor("#7c3aed"))
    canvas_obj.rect(0, 11.4 * inch, 8.5 * inch, 0.6 * inch, fill=True, stroke=False)
    canvas_obj.setFillColor(white)
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawString(0.5 * inch, 11.58 * inch, "TeamForge - SDE 1 Interview Preparation Guide")
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(8.0 * inch, 11.58 * inch, "Project-Grounded Technical Q&A")
    canvas_obj.restoreState()

def draw_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(HexColor("#6b7280"))
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawCentredString(4.25 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas_obj.restoreState()

output_path = os.path.join(os.path.dirname(__file__), "TeamForge_SDE1_Interview_Prep_2026.pdf")
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    topMargin=0.85 * inch,
    bottomMargin=0.6 * inch,
    leftMargin=0.6 * inch,
    rightMargin=0.6 * inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=22, leading=26, textColor=HexColor("#6d28d9"), alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle("CustomSubtitle", parent=styles["Normal"], fontSize=10.5, leading=14, textColor=HexColor("#4b5563"), alignment=TA_CENTER, spaceAfter=12)
section_style = ParagraphStyle("Section", parent=styles["Heading1"], fontSize=13, leading=16, textColor=HexColor("#5b21b6"), spaceBefore=14, spaceAfter=8, fontName="Helvetica-Bold")
q_style = ParagraphStyle("Question", parent=styles["Heading2"], fontSize=10.5, leading=14, textColor=HexColor("#111827"), spaceBefore=10, spaceAfter=3, fontName="Helvetica-Bold")
meta_style = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8.5, leading=11, textColor=HexColor("#6d28d9"), fontName="Helvetica-Bold", spaceAfter=4)

a_style = ParagraphStyle("Answer", parent=styles["Normal"], fontSize=9, leading=13, textColor=HexColor("#1f2937"), spaceAfter=6)
star_box = ParagraphStyle("StarBox", parent=styles["Normal"], fontSize=9, leading=13, textColor=HexColor("#3b0764"), backColor=HexColor("#f3e8ff"), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=6)
prep_box = ParagraphStyle("PrepBox", parent=styles["Normal"], fontSize=9, leading=13, textColor=HexColor("#064e3b"), backColor=HexColor("#ecfdf5"), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=6)

fu_style = ParagraphStyle("FollowUp", parent=styles["Normal"], fontSize=8.5, leading=12, textColor=HexColor("#374151"), leftIndent=10, spaceAfter=4)
concept_style = ParagraphStyle("KeyConcept", parent=styles["Normal"], fontSize=8.5, leading=11, textColor=HexColor("#6d28d9"), fontName="Helvetica-Bold", spaceBefore=2, spaceAfter=4)
code_style = ParagraphStyle("Code", parent=styles["Normal"], fontSize=7.5, leading=9.5, fontName="Courier", textColor=HexColor("#111827"), backColor=HexColor("#f3f4f6"), leftIndent=6, rightIndent=6, spaceBefore=3, spaceAfter=5)
note_style = ParagraphStyle("Note", parent=styles["Normal"], fontSize=8.5, leading=11.5, textColor=HexColor("#374151"), backColor=HexColor("#f5f3ff"), leftIndent=8, rightIndent=8, spaceBefore=6, spaceAfter=8)

questions = [
    {
        "num": 1,
        "freq": "HIGH (~95%)",
        "category": "Project Architecture & Scope",
        "question": "Tell me about your project - what problem does TeamForge solve?",
        "method": "STAR",
        "star": {
            "S": "Small-to-medium teams often struggle with bloated project management tools like Jira or unstructured channels like chat and spreadsheets, leading to lost tasks and unclear ownership.",
            "T": "I designed and built TeamForge, a multi-tenant B2B project management SaaS that delivers structured organization without operational bloat.",
            "A": "I implemented a 3-tier hierarchy (Workspaces -> Projects -> Tasks) with strict data isolation per workspace. Built the full backend using Node.js, Express, TypeScript, and MongoDB, paired with a React 18 + Vite frontend using TanStack Query for data fetching and Zustand for state persistence.",
            "R": "Delivered a production-ready application supporting secure multi-tenancy, instant team onboarding via invite codes, and workspace-scoped Role-Based Access Control (RBAC)."
        },
        "followups": [
            ("Why choose multi-tenancy at the workspace level rather than database isolation?",
             "Workspace-level isolation using a shared database with workspaceId tenant scoping offers the best trade-off between cost efficiency and complexity for an MVP. Database-per-tenant adds significant infrastructure overhead and connection pool exhaustion at small scale, whereas indexing workspaceId across collections ensures fast queries and logical isolation."),
            ("How do invite codes simplify onboarding without compromising security?",
             "Workspace owners generate secure UUID invite codes. When a user registers or logs in with an invite code, our backend transaction bypasses public workspace creation and atomically joins the user directly to the target workspace with a default MEMBER role.")
        ],
        "key_concept": "3-tier multi-tenant architecture (Workspace -> Project -> Task) with tenant-scoped MongoDB queries."
    },
    {
        "num": 2,
        "freq": "HIGH (~90%)",
        "category": "Authentication & Security",
        "question": "How does authentication work in TeamForge? Walk me through the request lifecycle.",
        "method": "PREP",
        "prep": {
            "P": "TeamForge implements Passport.js with three authentication strategies: JWT (cookie-based), Google OAuth 2.0, and Local email/password.",
            "R": "This multi-strategy approach accommodates different login workflows while ensuring session security. Storing JWTs in httpOnly cookies eliminates XSS token theft compared to localStorage.",
            "E": "On login, signJwtToken creates an HS256-signed token (audience: ['user'], 24h expiry) attached to an httpOnly, SameSite=Strict cookie. On requests, passportAuthenticationJWT extracts the token, verifies the user in MongoDB, and populates req.user. For Google OAuth, loginOrCreateAccountService runs inside a MongoDB transaction to link OAuth provider IDs to User documents.",
            "P2": "This provides a seamless, secure authentication pipeline across both social and credentials-based logins."
        },
        "followups": [
            ("Why store JWT in httpOnly cookies instead of localStorage?",
             "Tokens stored in localStorage are vulnerable to Cross-Site Scripting (XSS) because any injected client script can read localStorage. HttpOnly cookies are inaccessible to client JS, meaning XSS attacks cannot extract session tokens."),
            ("How does account linking work if a user registers with email/password and later uses Google OAuth?",
             "When a Google OAuth login occurs, loginOrCreateAccountService checks if a User exists with that email. If found, it creates an Account document linking provider: 'GOOGLE' and providerId to the existing User ID inside a transaction, enabling unified login.")
        ],
        "key_concept": "Passport.js + JWT in httpOnly cookies + MongoDB transactional account linking.",
        "code": "// backend/src/middlewares/isAuthenticated.middleware.ts\nconst isAuthenticated = async (req: Request, res: Response, next: NextFunction) => {\n  if (!req.user || !req.user._id) throw new UnauthorizedException('Unauthorized. Please log in.');\n  next();\n};"
    },
    {
        "num": 3,
        "freq": "HIGH (~85%)",
        "category": "Authorization & RBAC",
        "question": "Explain your Role-Based Access Control (RBAC) system. How are permissions enforced?",
        "method": "STAR",
        "star": {
            "S": "In a multi-tenant platform, a user's permissions must vary by context - a user can be an OWNER in Workspace A but only a MEMBER in Workspace B.",
            "T": "I needed a granular authorization system that evaluates permissions per request without coupling roles globally to the User model.",
            "A": "I created a 3-part RBAC model: Role collection (OWNER, ADMIN, MEMBER), Member join table (associating userId, workspaceId, role), and RolePermissions mapping 14 granular permissions (e.g., CREATE_TASK, DELETE_WORKSPACE). I wrote a reusable roleGuard middleware to enforce permissions at the route layer.",
            "R": "Achieved zero-trust request authorization. Permissions are dynamically evaluated based on the user's active workspace membership."
        },
        "followups": [
            ("How does roleGuard enforce required permissions at the endpoint level?",
             "roleGuard receives the user's member role and an array of required PermissionType enums. It looks up RolePermissions[role] and executes .every(perm => userPermissions.includes(perm)). If permission is lacking, it immediately throws UnauthorizedException before the controller runs."),
            ("How does the frontend stay synchronized with backend RBAC rules?",
             "The AuthProvider fetches the current workspace and user membership, utilizing the usePermissions hook to derive active permissions. The <PermissionsGuard> HOC wraps UI elements (like 'Delete Workspace' buttons) to conditionally render them based on hasPermission().")
        ],
        "key_concept": "Workspace-scoped RBAC via Member join table and roleGuard middleware.",
        "code": "// backend/src/utils/roleGuard.ts\nexport const roleGuard = (role: keyof typeof RolePermissions, requiredPermission: PermissionType[]) => {\n  const permission = RolePermissions[role];\n  const hasPermission = requiredPermission.every((p) => permission.includes(p));\n  if (!hasPermission) throw new UnauthorizedException('Permission denied');\n};"
    },
    {
        "num": 4,
        "freq": "HIGH (~80%)",
        "category": "Database Schema & Modeling",
        "question": "Describe your database schema - what are the core collections and relationships?",
        "method": "PREP",
        "prep": {
            "P": "TeamForge's database consists of 7 collections: Users, Accounts, Workspaces, Members, Roles, Projects, and Tasks.",
            "R": "This normalized collection structure cleanly separates user identities, workspace boundaries, and project management entities while maintaining fast retrieval paths.",
            "E": "1) Users holds identity & currentWorkspace reference.<br/>2) Accounts links OAuth providers (userId, provider, providerId).<br/>3) Workspaces represents tenants (name, owner, inviteCode).<br/>4) Members is the join collection (userId, workspaceId, role).<br/>5) Projects belongs to workspace and createdBy.<br/>6) Tasks links project, workspace, createdBy, and assignedTo.<br/>7) Roles defines permission arrays.",
            "P2": "By keeping relationships explicit and referencing IDs, we preserve referential integrity and simplify tenant isolation."
        },
        "followups": [
            ("Why does the Task model store a direct workspace reference when it already belongs to a project?",
             "This is intentional denormalization. Storing workspace directly on Task allows task filtering, pagination, and analytics queries to filter by workspace without performing costly $lookup joins through the Project collection first."),
            ("How do you prevent a user from assigning a task to someone outside the workspace?",
             "In createTaskService, before saving, we query MemberModel.exists({ userId: assignedTo, workspaceId }). If the assigned user is not an active workspace member, the service throws NotFoundException('Assigned user is not a member of the workspace').")
        ],
        "key_concept": "7 collections connected via relational ObjectIds with denormalized tenant keys."
    },
    {
        "num": 5,
        "freq": "HIGH (~75%)",
        "category": "Data Consistency & Transactions",
        "question": "When and why do you use MongoDB transactions in TeamForge?",
        "method": "STAR",
        "star": {
            "S": "Multi-document mutations - such as deleting a workspace or registering a user via invite code - risk leaving orphan records or partial state if the server crashes mid-execution.",
            "T": "I needed guarantees that multi-step operations complete atomically (all-or-nothing).",
            "A": "I utilized MongoDB Sessions (mongoose.startSession()) and ACID transactions across critical services. In deleteWorkspaceByIdService, the transaction deletes all associated Projects, Tasks, Members, resets user workspace state, and deletes the Workspace document within a single session.",
            "R": "Guaranteed 100% data consistency. Failed transactions auto-rollback via session.abortTransaction(), preventing dangling data."
        },
        "followups": [
            ("What happens if a database session times out or encounters a write conflict during a transaction?",
             "MongoDB throws an error, triggering our catch block which calls session.abortTransaction() and passes the error to errorHandler.middleware.ts. The transaction guarantees that no partial changes persist."),
            ("Why are transactions not used for every database write in TeamForge?",
             "Transactions introduce lock overhead and latency because MongoDB must maintain write-intent logs across replica nodes. We reserve transactions strictly for multi-document operations where partial failure damages data integrity (e.g., workspace teardown, registration).")
        ],
        "key_concept": "ACID compliance for multi-document mutations using Mongoose sessions."
    },
    {
        "num": 6,
        "freq": "MEDIUM (~70%)",
        "category": "Backend API Architecture",
        "question": "How is your backend structured, and how do you handle asynchronous errors?",
        "method": "PREP",
        "prep": {
            "P": "TeamForge uses an Express + TypeScript MVC pattern (Routes -> Controllers -> Services) with Zod validation and a custom asyncHandler wrapper.",
            "R": "Separating HTTP handling from business logic keeps code modular and testable, while asyncHandler eliminates repetitive try-catch blocks across controllers.",
            "E": "asyncHandler wraps controller functions: (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next). Controllers parse request bodies via Zod schemas, then delegate to services (task.service.ts, workspace.service.ts). Thrown custom exceptions (BadRequestException, NotFoundException) inherit from AppError and are caught by errorHandler.middleware.ts.",
            "P2": "This creates a predictable, clean request lifecycle with centralized error handling."
        },
        "followups": [
            ("How does errorHandler.middleware.ts format error responses for the client?",
             "The error middleware inspects the error object. If it is an instance of AppError, it extracts statusCode (e.g., 400, 404, 401) and errorCode enum, returning { message, errorCode, statusCode }. Uncaught runtime errors default to 500 INTERNAL_SERVER_ERROR."),
            ("What role does Zod play in controller request handling?",
             "Zod schemas enforce strict runtime validation on req.body, req.params, and req.query. If validation fails, Zod throws a formatted validation error before service logic runs, preventing invalid data from entering the database.")
        ],
        "key_concept": "Async error propagation via asyncHandler and centralized AppError formatting."
    },
    {
        "num": 7,
        "freq": "MEDIUM (~65%)",
        "category": "Frontend State & Data Fetching",
        "question": "How do you handle client state vs. server state on the frontend?",
        "method": "PREP",
        "prep": {
            "P": "We separate server state using TanStack React Query v5 from client state using Zustand and React Context.",
            "R": "Mixing server cache with UI state leads to sync bugs and stale data. React Query manages async caching, background revalidation, and loading states, while Zustand holds persistent client state.",
            "E": "Server data (workspaces, projects, tasks, member lists) is managed by custom React Query hooks (useGetWorkspaceQuery, useGetAllTasksQuery). On mutations (e.g., createTaskMutationFn), queryClient.invalidateQueries triggers targeted refetches. Client state (active workspace selection, modal visibility) is managed by Zustand with sessionStorage persistence.",
            "P2": "This separation eliminates manual state syncing and ensures optimal UI rendering speed."
        },
        "followups": [
            ("How does React Query handle query invalidation when a task is created or edited?",
             "Upon successful mutation in useMutation, the onSuccess callback calls queryClient.invalidateQueries({ queryKey: ['all-tasks', workspaceId] }). This marks cached task lists as stale and triggers a silent background refetch."),
            ("Why use sessionStorage persistence for Zustand instead of localStorage?",
             "Workspace selection and temporary session states are session-bound. sessionStorage automatically resets when a tab closes, preventing cross-session workspace leaks if multiple users use the same browser.")
        ],
        "key_concept": "TanStack React Query for async server cache + Zustand for local UI state."
    },
    {
        "num": 8,
        "freq": "MEDIUM (~60%)",
        "category": "Type Safety & Interfaces",
        "question": "How do you enforce end-to-end type safety between backend and frontend?",
        "method": "STAR",
        "star": {
            "S": "In full-stack JavaScript/TypeScript projects, API contract mismatches between backend JSON responses and frontend component props cause subtle runtime bugs.",
            "T": "I established an end-to-end typing strategy across Mongoose models, API response payloads, and React components.",
            "A": "On the backend, I authored strict Mongoose Document interfaces (UserDocument, TaskDocument). On the frontend, I centralized all contract interfaces in frontend/src/types/api.type.ts (e.g., AllTaskResponseType, WorkspaceByIdResponseType). Axios call functions in api.ts strictly return typed Promises (Promise<AllTaskResponseType>).",
            "R": "Achieved full compile-time autocomplete and safety. Renaming or modifying an API field immediately surface TypeScript errors during build."
        },
        "followups": [
            ("How do you handle date serialization across the network barrier?",
             "MongoDB stores dates as ISO Date objects, but JSON responses serialize them as strings. Frontend types define dates as string, and components parse them using helper functions like format(new Date(dueDate), 'MMM dd')."),
            ("What strategy prevents 'any' types when handling dynamic query parameters?",
             "In getAllTasksQueryFn, we use structured payload interfaces (AllTaskPayloadType) with optional keys (keyword?: string, priority?: TaskPriorityEnumType). URLSearchParams appends parameters conditionally, preserving strict types.")
        ],
        "key_concept": "Centralized interface contracts in api.type.ts matching backend JSON structures."
    },
    {
        "num": 9,
        "freq": "MEDIUM (~55%)",
        "category": "Performance & Pagination",
        "question": "How do you optimize task listing queries for large workspaces?",
        "method": "PREP",
        "prep": {
            "P": "We combine compound MongoDB indexes with server-side pagination, selective projection, and debounced client-side filtering.",
            "R": "Fetching all tasks without limit causes query slowdowns and memory spikes as workspaces scale to thousands of items.",
            "E": "In getAllTasksService: <br/>1) We construct dynamic filter queries over workspaceId, projectId, status, priority, assignedTo.<br/>2) Execution uses .skip((pageNumber - 1) * pageSize).limit(pageSize).<br/>3) Promise.all executes TaskModel.find() and TaskModel.countDocuments() concurrently.<br/>4) .populate('assignedTo', '_id name profilePicture -password') excludes sensitive fields.<br/>5) Compound index { workspaceId: 1, createdAt: -1 } accelerates sorting.",
            "P2": "This query design maintains sub-50ms API response times regardless of total collection size."
        },
        "followups": [
            ("Why execute find() and countDocuments() in Promise.all?",
             "Promise.all runs both database queries in parallel on the MongoDB driver thread pool rather than sequentially, cutting total query latency nearly in half."),
            ("How does the frontend search bar avoid sending an API request on every keystroke?",
             "The search bar uses a custom useDebounce hook (300ms delay) on the search input state. Query parameters update only after typing pauses, preventing search endpoint flooding.")
        ],
        "key_concept": "Concurrent query execution (Promise.all), compound indexing, and debounced filters."
    },
    {
        "num": 10,
        "freq": "MEDIUM (~50%)",
        "category": "Security & Vulnerability Mitigation",
        "question": "What measures prevent common web vulnerabilities like XSS, CSRF, and IDOR in TeamForge?",
        "method": "STAR",
        "star": {
            "S": "SaaS applications handling multi-tenant data are prime targets for cross-tenant data leaks (IDOR), token theft (XSS), and unauthorized mutations (CSRF).",
            "T": "I implemented systemic defenses across authentication, input sanitization, and data access layers.",
            "A": "1) XSS: Auth JWTs stored in httpOnly cookies; React auto-escapes rendered JSX.<br/>2) CSRF: Auth cookies set SameSite=Strict and Secure in production.<br/>3) IDOR: Every service query explicitly includes workspaceId along with resource ID (e.g., TaskModel.findOne({ _id: taskId, workspace: workspaceId })).<br/>4) Injection: Zod validates all inputs; Mongoose parameterizes queries.",
            "R": "Eliminated IDOR vectors across all endpoints. Users cannot view or modify resources outside their authorized workspace even if they guess valid ObjectIDs."
        },
        "followups": [
            ("How does specifying workspaceId on every resource query prevent IDOR?",
             "If an endpoint queried TaskModel.findById(taskId), an attacker in Workspace A could guess a taskId from Workspace B and access it. Including workspace: workspaceId in the query ensures MongoDB returns null if the task doesn't belong to the active workspace."),
            ("How does SameSite=Strict protect against CSRF attacks?",
             "SameSite=Strict instructs the browser never to attach the authentication cookie to requests originating from third-party sites, making forged cross-site POST/PUT requests unauthenticated.")
        ],
        "key_concept": "Tenant-scoped database queries for IDOR prevention + httpOnly SameSite=Strict cookies."
    },
    {
        "num": 11,
        "freq": "MEDIUM (~45%)",
        "category": "DevOps & Infrastructure",
        "question": "How is TeamForge containerized and deployed across environments?",
        "method": "PREP",
        "prep": {
            "P": "TeamForge uses Docker Compose for reproducible local development and a decoupled cloud deployment model for production.",
            "R": "Containerizing local development ensures parity between developer machines and production, while decoupled deployment allows frontend and backend to scale independently.",
            "E": "Local: docker-compose.yml provisions Node.js API, MongoDB replica set (required for transactions), and Redis.<br/>Production Frontend: Deployed on Vercel with automatic edge CDN caching.<br/>Production Backend: Containerized Node.js API hosted on Railway/AWS EC2.<br/>Production DB: Managed MongoDB Atlas multi-node replica set with automated backups.",
            "P2": "This architecture keeps dev environment setup to one command (docker-compose up) while utilizing cloud-native platforms for production."
        },
        "followups": [
            ("Why is a MongoDB replica set required in the local docker-compose.yml environment?",
             "MongoDB requires write-ahead logging (oplog) across a replica set to execute multi-document transactions. Single standalone MongoDB instances reject startSession() transaction calls."),
            ("How are environment configurations managed across stages?",
             "Environment variables are loaded via get-env.ts with fallback defaults. Local dev uses .env (gitignored), while production variables are injected securely via Railway and Vercel configuration panels.")
        ],
        "key_concept": "Docker Compose local replica set + Vercel frontend + Railway/EC2 backend."
    },
    {
        "num": 12,
        "freq": "HIGH (~85%)",
        "category": "Complex Debugging & Engineering Challenges",
        "question": "Walk me through the most challenging bug or technical hurdle you solved in TeamForge.",
        "method": "STAR",
        "star": {
            "S": "When testing workspace deletion in staging, we discovered that deleting a workspace occasionally left orphaned Task and Project documents in MongoDB if a network glitch occurred mid-operation.",
            "T": "I needed to make workspace deletion completely atomic across four separate collections (Workspace, Project, Task, Member).",
            "A": "I refactored deleteWorkspaceByIdService to initialize a Mongoose session transaction (startSession()). I ordered mutations carefully: verify owner rights -> delete projects (ProjectModel.deleteMany({ workspace }).session(session)) -> delete tasks -> delete members -> update user's currentWorkspace -> delete workspace document -> session.commitTransaction(). Wrapped everything in a try/catch block with session.abortTransaction().",
            "R": "Eliminated data corruption risks. Simulated failure injections proved that partial deletions successfully roll back 100% of mutations."
        },
        "followups": [
            ("How did you handle the edge case where the user's currentWorkspace was the workspace being deleted?",
             "Inside the session, we check if (user.currentWorkspace.equals(workspaceId)). We query MemberModel.findOne({ userId }) to find another workspace the user belongs to and reassign user.currentWorkspace to that ID before committing."),
            ("What trade-off did you evaluate when deciding to run cascading deletes on the server vs using database hooks?",
             "Mongoose middleware hooks like post('remove') don't trigger reliably on bulk operations like deleteMany(). Executing explicit sequential deleteMany() calls within an explicit transaction guarantees execution control and atomicity.")
        ],
        "key_concept": "Multi-collection cascade teardown with user context re-pointing within a Mongoose session."
    },
    {
        "num": 13,
        "freq": "HIGH (~80%)",
        "category": "Technical Trade-offs",
        "question": "Why choose a Document database (MongoDB) over a Relational database (PostgreSQL) for TeamForge?",
        "method": "PREP",
        "prep": {
            "P": "MongoDB was chosen for document schema flexibility, seamless JSON/TypeScript integration, and fast nested reads.",
            "R": "TeamForge features evolving domain entities (dynamic task priorities, custom statuses, emoji metadata) where rigid relational migrations add development friction.",
            "E": "Pros gained:<br/>- Schema flexibility for tasks and project metadata.<br/>- BSON/JSON mapping directly aligns with TypeScript interfaces without complex ORM translation layers.<br/>- High-performance read operations on primary collections.<br/><br/>Trade-offs mitigated:<br/>- Relational integrity: Enforced in application service layer using explicit validation and Mongoose schema constraints.<br/>- Joins: $lookup used sparingly; strategic denormalization (workspace ID on Task) avoids deep joins.",
            "P2": "For an agile SaaS product, MongoDB delivered the best balance of speed and structure."
        },
        "followups": [
            ("If TeamForge required complex financial reporting across tenants, would MongoDB still be suitable?",
             "If cross-tenant analytical reporting and complex relational aggregations became core features, PostgreSQL with SQL joins and window functions would be superior. MongoDB aggregations become cumbersome for deep relational joins."),
            ("How do you guarantee unique constraints in MongoDB without relational foreign keys?",
             "We use Mongoose unique compound indexes (e.g., memberSchema.index({ userId: 1, workspaceId: 1 }, { unique: true })), which are enforced directly by MongoDB's B-tree index engine.")
        ],
        "key_concept": "Document flexibility vs relational integrity trade-off; application-enforced constraints."
    },
    {
        "num": 14,
        "freq": "MEDIUM (~50%)",
        "category": "Scalability & Future Architecture",
        "question": "How would you re-architect TeamForge to support 100,000 active workspaces?",
        "method": "STAR",
        "star": {
            "S": "At 100,000 active workspaces, a single database instance and monolithic Node.js process would suffer from CPU bottlenecks, database connection saturation, and slow query execution.",
            "T": "Design a scaling roadmap to transition TeamForge from a single-node setup to a high-availability distributed architecture.",
            "A": "I planned a 4-step scaling strategy:<br/>1) Database Sharding: Shard MongoDB cluster by workspaceId as the shard key, ensuring all data for a workspace resides on the same shard.<br/>2) Caching Layer: Redis cluster for session caching and caching getWorkspaceById responses.<br/>3) Asynchronous Queues: BullMQ + Redis for background tasks (sending invite emails, generating analytics reports).<br/>4) Stateless API Scale: Horizontal scaling of Express containers behind an AWS Application Load Balancer.",
            "R": "The architecture isolates tenant workloads, ensuring a high-traffic workspace doesn't impact other tenants ('noisy neighbor' isolation)."
        },
        "followups": [
            ("Why is workspaceId an ideal MongoDB shard key for TeamForge?",
             "Because 99% of database queries filter by workspaceId. Sharding by workspaceId ensures queries are routed to a single shard (targeted queries) rather than broadcasting across all shards (scatter-gather)."),
            ("How would real-time task updates be handled across multiple backend containers?",
             "By implementing Socket.IO with a Redis Pub/Sub adapter. When a user updates a task on Server A, the event publishes to Redis, which broadcasts it to Server B where other workspace members are connected.")
        ],
        "key_concept": "Tenant-based database sharding (workspaceId), Redis caching, and async job queues."
    },
    {
        "num": 15,
        "freq": "MEDIUM (~45%)",
        "category": "Testing Strategy",
        "question": "What is your testing philosophy and setup for TeamForge?",
        "method": "PREP",
        "prep": {
            "P": "We use a multi-tiered testing strategy: Jest for backend service/unit testing and Playwright for end-to-end user flow testing.",
            "R": "Unit tests verify core business logic fast, while E2E tests guarantee critical user journeys (registration, workspace creation, task management) function in real browser environments.",
            "E": "Backend Testing:<br/>- mongodb-memory-server spins up an ephemeral, in-memory MongoDB instance for fast test execution without database mocking.<br/>- Tests cover service methods (createWorkSpaceService, changeMemberRoleService) and error paths.<br/>Frontend Testing:<br/>- Playwright executes automated browser sessions testing login, modal forms, and permission guards.",
            "P2": "This dual approach ensures both API correctness and reliable client-side user experiences."
        },
        "followups": [
            ("Why use mongodb-memory-server instead of mocking Mongoose models with jest.mock()?",
             "Mocking Mongoose models tests your mocks, not your queries. mongodb-memory-server runs real MongoDB engine binaries in memory, validating actual queries, indexes, and transactions fast without network latency."),
            ("How do you test routes that require authenticated users in Jest?",
             "We create a helper function that generates valid JWT tokens signed with the test JWT_SECRET. Test HTTP requests include the token header Authorization: Bearer <test_jwt>, executing real middleware logic.")
        ],
        "key_concept": "In-memory database integration testing (mongodb-memory-server) + Playwright E2E."
    },
    {
        "num": 16,
        "freq": "MEDIUM (~40%)",
        "category": "Code Hygiene & Standards",
        "question": "How do you enforce code quality and prevent technical debt in TeamForge?",
        "method": "PREP",
        "prep": {
            "P": "We enforce quality programmatically using ESLint, Prettier, TypeScript strict mode, and Husky pre-commit hooks.",
            "R": "Manual code reviews should focus on architectural design and logic, not formatting style or missing type checks. Programmatic enforcement automates style consistency.",
            "E": "1) Husky + lint-staged: Intercepts git commit and runs ESLint + Prettier on staged files.<br/>2) TypeScript strict mode: Rejects implicit any, unsafe index accesses, and unhandled nulls.<br/>3) Zod runtime guards: Prevents malformed API requests from entering application logic.<br/>4) Clean Git workflow: Feature branches merged via PRs with automated GitHub Actions CI builds.",
            "P2": "Automating these checks keeps the codebase maintainable and prevents lint regression over time."
        },
        "followups": [
            ("What ESLint rules do you consider non-negotiable for TypeScript projects?",
             "@typescript-eslint/no-explicit-any set to error, @typescript-eslint/explicit-module-boundary-types for public services, and no-floating-promises to catch unhandled async promises."),
            ("How does lint-staged improve developer experience compared to running linter on the whole project?",
             "lint-staged runs checks only on modified, staged files, completing in under 2 seconds. Running linters over the full project on every commit creates friction and slows developer velocity.")
        ],
        "key_concept": "Automated pre-commit static analysis via Husky, lint-staged, and strict TypeScript."
    },
    {
        "num": 17,
        "freq": "MEDIUM (~35%)",
        "category": "Operational Resilience",
        "question": "How are runtime errors captured, logged, and surfaced to users?",
        "method": "STAR",
        "star": {
            "S": "Unhandled server exceptions can leak stack traces to clients (security risk) or crash Node.js processes, leaving users stranded with generic browser errors.",
            "T": "Build a robust error handling pipeline that sanitizes client responses while capturing detailed diagnostic logs.",
            "A": "I implemented a hierarchy of custom operational error classes extending AppError (BadRequestException, UnauthorizedException, NotFoundException). Controllers throw these directly or catch runtime errors via asyncHandler. The global errorHandler logs full stack traces and returns structured JSON: { message, errorCode, statusCode }. On the client, Axios response interceptors catch error codes and display toast notifications.",
            "R": "Clean client UX with 100% sanitized public error messages, while server logs retain detailed stack traces for debugging."
        },
        "followups": [
            ("What is the difference between an operational error and a programmer error?",
             "Operational errors are expected failure conditions (e.g., invalid password, user not found, 404). Programmer errors are unexpected bugs (e.g., TypeError: cannot read property of undefined). Operational errors return formatted 400-level JSON; programmer errors trigger 500 responses and process logging."),
            ("How does the frontend handle a 401 Unauthorized error globally?",
             "An Axios response interceptor intercepts 401 statuses globally. If a request fails with ACCESS_UNAUTHORIZED, the interceptor clears client auth state and redirects the browser to /login.")
        ],
        "key_concept": "Custom AppError hierarchy, global error middleware, and Axios interceptor redirects."
    },
    {
        "num": 18,
        "freq": "LOW (~30%)",
        "category": "Configuration Management",
        "question": "How do you handle environment configurations and secret management across environments?",
        "method": "PREP",
        "prep": {
            "P": "Environment variables are loaded via centralized configuration files with strict startup validation.",
            "R": "Hardcoding secrets or relying on unvalidated process.env calls scattered across files leads to silent runtime failures when an environment variable is missing.",
            "E": "1) Centralized backend/src/config/app.config.ts reads process.env variables.<br/>2) A custom get-env.ts utility function asserts that required environment variables (e.g., JWT_SECRET, MONGO_URI, GOOGLE_CLIENT_ID) exist at startup. If missing, the process fails fast with an explicit error message.<br/>3) .env files are strictly gitignored, with .env.example committed as a documentation template.",
            "P2": "Fail-fast configuration validation prevents silent failures in production deployments."
        },
        "followups": [
            ("Why is 'failing fast' at startup better than lazy-loading environment variables when needed?",
             "Lazy-loading means a missing JWT_SECRET is not discovered until a user tries to log in hours after deployment. Failing fast during container boot halts bad deployments instantly during CI/CD checks."),
            ("How are frontend environment variables handled differently from backend secrets?",
             "Vite bundles frontend variables prefixed with VITE_ into the static JavaScript client build. Backend variables (JWT_SECRET, MongoDB passwords) remain strictly server-side and are never exposed to the client bundle.")
        ],
        "key_concept": "Centralized config modules with startup fail-fast validation."
    },
    {
        "num": 19,
        "freq": "LOW (~25%)",
        "category": "Product Strategy & Feature Prioritization",
        "question": "What are the most critical architectural improvements you would make next to TeamForge?",
        "method": "STAR",
        "star": {
            "S": "As team usage grows, asynchronous collaboration (email-only) becomes a bottleneck, and user activity requires real-time presence.",
            "T": "Identify high-value technical additions to transform TeamForge into a real-time collaborative workspace.",
            "A": "I mapped out three high-priority enhancements:<br/>1) WebSockets (Socket.IO): For real-time task board updates, presence indicators, and live typing feedback.<br/>2) S3/Cloudinary File Attachments: Presigned URL upload pipeline for task attachments.<br/>3) Audit Logging: A dedicated AuditLog collection capturing workspace configuration changes and permission updates for security reporting.",
            "R": "These additions would elevate TeamForge from a basic task tracker to an enterprise-ready collaborative platform."
        },
        "followups": [
            ("How would you securely handle S3 file uploads for task attachments?",
             "Using AWS S3 Presigned URLs. The client requests an upload URL from the backend -> backend verifies user workspace permissions -> backend generates a temporary presigned PUT URL -> client uploads directly to S3. S3 credentials never touch the client."),
            ("How would you structure the Audit Log collection?",
             "AuditLog: { workspaceId, actorId, action (e.g. 'MEMBER_ROLE_CHANGED'), targetId, metadata, timestamp }. Indexed by workspaceId and timestamp for fast compliance querying.")
        ],
        "key_concept": "Real-time WebSocket event layer, presigned S3 uploads, and audit logging."
    },
    {
        "num": 20,
        "freq": "HIGH (~90%)",
        "category": "Engineering Leadership & Reflection",
        "question": "Looking back, what key engineering lesson did building TeamForge teach you?",
        "method": "STAR",
        "star": {
            "S": "In early development, I focused heavily on feature velocity, implementing endpoints rapidly without establishing strict API error contracts or comprehensive unit tests upfront.",
            "T": "Refactoring data models and auth logic mid-project became time-consuming due to a lack of regression test safety nets.",
            "A": "I paused feature development to establish strict Zod validation schemas, unified custom error classes, and built out an integration test suite using mongodb-memory-server. I adopted a Contract-First mindset for subsequent features.",
            "R": "Significantly reduced bug regression rates. I learned that upfront discipline in domain boundaries, types, and testing dramatically increases overall shipping speed in the long run."
        },
        "followups": [
            ("How has building TeamForge changed your approach to designing software systems?",
             "I now design systems with explicit domain boundaries and failure modes in mind from day one. I prioritize clear type contracts, defense-in-depth security, and testability over pure coding speed."),
            ("What advice would you give an engineer starting a multi-tenant project?",
             "Establish tenant boundaries (e.g., workspaceId) explicitly in data schemas and middleware at the very beginning. Retrofitting multi-tenancy and data isolation onto a single-tenant database architecture later is extremely difficult and error-prone.")
        ],
        "key_concept": "Contract-First design, upfront test architecture, and explicit tenant boundary modeling."
    }
]

def build_pdf():
    story = []

    # Cover / Header block
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("TeamForge", title_style))
    story.append(Paragraph("SDE 1 Interview Preparation Guide", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=1, color=HexColor("#7c3aed"), spaceAfter=12))

    intro_text = (
        "<b>How to use this guide:</b> "
        "Each answer is structured using either the <b>STAR method</b> (Situation, Task, Action, Result) for behavioral/engineering stories "
        "or the <b>PREP method</b> (Point, Reason, Evidence, Point) for technical design choices. "
        "Follow-up questions provide substantive 2-3 sentence answers matching interviewer expectations. "
        "All answers are grounded in the actual TeamForge codebase."
    )
    story.append(Paragraph(intro_text, note_style))
    story.append(Spacer(1, 0.2 * inch))

    # Section: Core Questions
    story.append(Paragraph("Project-Specific Technical Questions", section_style))

    for q in questions:
        freq_color_hex = "#dc2626" if "HIGH" in q["freq"] else ("#d97706" if "MEDIUM" in q["freq"] else "#059669")
        method_badge = "STAR Framework" if q["method"] == "STAR" else "PREP Framework"

        story.append(Paragraph(
            f'<font color="{freq_color_hex}" style="font-size:8pt;font-weight:bold">● {q["freq"]}</font> &nbsp;'
            f'<b>Q{q["num"]}: {q["question"]}</b>',
            q_style
        ))

        story.append(Paragraph(
            f'📂 {q["category"]} &nbsp;|&nbsp; <b>{method_badge}</b>',
            meta_style
        ))

        if q["method"] == "STAR":
            s = q["star"]
            star_html = (
                f'<b>S (Situation):</b> {s["S"]}<br/><br/>'
                f'<b>T (Task):</b> {s["T"]}<br/><br/>'
                f'<b>A (Action):</b> {s["A"]}<br/><br/>'
                f'<b>R (Result):</b> {s["R"]}'
            )
            story.append(Paragraph(star_html, star_box))
        else:
            p = q["prep"]
            prep_html = (
                f'<b>P (Point):</b> {p["P"]}<br/><br/>'
                f'<b>R (Reason):</b> {p["R"]}<br/><br/>'
                f'<b>E (Evidence):</b><br/>{p["E"]}<br/><br/>'
                f'<b>P (Point):</b> {p["P2"]}'
            )
            story.append(Paragraph(prep_html, prep_box))

        if "code" in q:
            story.append(Paragraph("<b>Code Anchor:</b>", ParagraphStyle("CodeLabel", parent=styles["Normal"], fontSize=8, fontName="Helvetica-Bold", textColor=HexColor("#374151"))))
            story.append(Paragraph(q["code"], code_style))

        fu_lines = []
        for q_fu, a_fu in q["followups"]:
            fu_lines.append(f'<b>Q: {q_fu}</b><br/><b>A:</b> {a_fu}')

        fu_text = "<b>Follow-up Questions & Interviewer-Expected Answers:</b><br/><br/>" + "<br/><br/>".join(fu_lines)
        story.append(Paragraph(fu_text, fu_style))

        story.append(Paragraph(f'<b>Key Takeaway:</b> {q["key_concept"]}', concept_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#e5e7eb"), spaceAfter=8))

    story.append(PageBreak())

    story.append(Paragraph("How to Ace Your TeamForge Technical Interview", section_style))

    strategy_text = """
<b>1. Master the STAR Method for Architectural & Behavioral Deep Dives</b><br/>
- <b>Situation:</b> State the application context in 1-2 tight sentences (e.g. multi-tenant isolation, cascade deletes).<br/>
- <b>Task:</b> State the engineering requirement or security constraint clearly.<br/>
- <b>Action:</b> Describe YOUR technical implementation details (middleware, schemas, transactions, React Query invalidations). Spend 60% of your time here.<br/>
- <b>Result:</b> Mention data integrity gains, bug elimination, or performance metrics.<br/><br/>

<b>2. Master the PREP Method for Technology Choices & Design Questions</b><br/>
- <b>P (Point):</b> State your technical choice upfront in one sentence.<br/>
- <b>R (Reason):</b> Explain WHY this tech choice fits TeamForge better than alternatives.<br/>
- <b>E (Evidence):</b> Reference explicit files, hooks, schemas, or query logic from the TeamForge codebase.<br/>
- <b>P (Point):</b> Re-state your conclusion.<br/><br/>

<b>3. Answer Follow-up Questions Like an SDE 1</b><br/>
- Avoid vague 1-line answers. Give 2-3 substantive sentences that explain the <b>mechanism</b> and the <b>trade-off</b>.<br/>
- Always tie answers back to code components (`roleGuard.ts`, `Member` collection, `isAuthenticated`, `usePermissions`).
"""
    story.append(Paragraph(strategy_text, note_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("TeamForge Core Stack Quick Reference", section_style))

    ref_rows = [
        ["Layer", "Technology", "Implementation Detail in TeamForge"],
        ["Frontend", "React 18 + Vite + TS", "Component architecture with strict typing"],
        ["Server State", "TanStack Query v5", "Query invalidation on mutation + stale-while-revalidate"],
        ["Client State", "Zustand + React Context", "Persistent auth store + usePermissions hook"],
        ["Backend API", "Node.js + Express + TS", "MVC architecture with asyncHandler and Zod schemas"],
        ["Authentication", "Passport.js + JWT + OAuth", "JWT in httpOnly cookie + Google OAuth account linking"],
        ["Authorization", "Custom RBAC Middleware", "roleGuard checking RolePermissions lookup map"],
        ["Database", "MongoDB + Mongoose", "7 collections, Mongoose Document typing, replica set"],
        ["Data Consistency", "MongoDB Transactions", "Mongoose session transactions for cascading deletes"],
        ["Testing", "Jest + Playwright", "In-memory MongoDB tests + browser E2E test suites"]
    ]

    ref_table = Table(ref_rows, colWidths=[1.1 * inch, 2.3 * inch, 3.8 * inch])
    ref_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#7c3aed")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f9fafb")),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e5e7eb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f9fafb"), white]),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
    ]))
    story.append(ref_table)

    story.append(Spacer(1, 0.3 * inch))

    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_footer)
    print("PDF build complete:", output_path)

if __name__ == "__main__":
    build_pdf()
