# RocketBank — Modern FinTech Platform

RocketBank is a high-performance digital banking system engineered with Django 5.x, PostgreSQL, Redis, Celery, and a server-side HTML5/CSS design system.

> **Frontend Architecture & Template Credit**:
> RocketBank's UI/UX design system and presentation architecture are adapted from **TemplateMo 623 NovaPay** ([https://templatemo.com](https://templatemo.com)), implementing a dark-slate aesthetic (`#0F1319`), sky-blue accent (`#4A9EE8`), fluid responsive layouts, interactive tickers, 3D tilt effects, WCAG 2.1 AA accessibility, and seamless light/dark theme switcher.

---

## Phase 3: Server-Side Frontend, Views, Forms & Design System

### 1. Django Views, Mixins, Middleware & Context Processors (Section 7)
- **Class-Based Views (CBVs)**: Comprehensive usage across all apps:
  - `ListView`: `BankAccountListView`, `TransactionListView`, `CardProductListView`, `BankCardListView`, `CreditProductListView`, `LoanListView`, `DepositProductListView`, `DepositListView`, `NotificationListView`, `SupportTicketListView`, `FAQListView`.
  - `DetailView`: `BankAccountDetailView`, `AccountByIbanDetailView`, `TransactionDetailView` (Receipt), `CardProductDetailView`, `CreditProductDetailView`, `SupportTicketDetailView`.
  - `CreateView`: `LoanApplyCreateView`, `SupportTicketCreateView`, `OpenDepositCreateView`.
  - `UpdateView` / `FormView`: `ProfileView`, `SecuritySettingsView`, `LoginUserView`, `RegisterView`, `MoneyTransferView`, `OpenAccountCreateView`, `BeneficiaryFormsetView`, `CardApplyWizardView`, `KYCUploadView`.
  - `DeleteView`: `BeneficiaryDeleteView`, `SavingGoalDeleteView`.
  - `TemplateView`: `LandingHomeView`, `AboutView`, `ContactsView`, `LoanCalculatorView`.
- **Custom Mixins (`apps/core/mixins.py`)**:
  - `OwnerRequiredMixin`: Checks object ownership against `request.user` and returns `403 Forbidden` (`PermissionDenied`) if unauthorized.
  - `AjaxResponseMixin`: Detects asynchronous AJAX/JSON requests and formats validation errors into structured JSON payloads (`{"success": false, "errors": ...}`).
  - `RoleRequiredMixin`: Enforces role-based access control based on user group membership.
- **Function-Based Views (FBVs with explicit POST handling & decorators)**:
  - `toggle_card_freeze` (`apps/cards/views.py`): `@login_required`, `@require_POST` for immediate card locking/unlocking.
  - `mark_notification_as_read` (`apps/notifications/views.py`): `@login_required`, `@require_POST` for updating notification state.
  - `mark_all_notifications_as_read`: `@login_required`, `@require_POST` for bulk marking notifications as read.
- **Custom URL Path Converters (`apps/core/converters.py`)**:
  - `iban`: Matches 15–34 alphanumeric character IBAN identifiers (`KZ...`).
  - `ref`: Matches reference numbers formatted as `TXN-YYYY-XXXXXXXX`.
- **Middleware (`apps/core/middleware.py`)**:
  - `RequestTimingAndLastVisitMiddleware`: Measures request execution time, records session activity timestamp, and attaches `X-Request-Duration` and `X-Request-Duration-Ms` response headers.
- **Context Processor (`apps/core/context_processors.py`)**:
  - `global_context`: Supplies `unread_notifications_count`, `active_currencies`, and `user_theme_preference` across all templates.

---

### 2. Authentication, Roles, Forms & Formsets (Section 2 & 5)
- **Authentication**: Registration with email verification token flow (`TimestampSigner`), Login with dual email/username support and audit logging (`LoginAudit`), strict POST-only Logout (`LogoutUserView`), Password Reset flow (`CustomPasswordResetView`), and Password Change.
- **Forms**:
  - `MoneyTransferForm`: Cross-field validation for sender balance, account status, and currency matching.
  - `LoanApplicationForm`: Validates credit limits, term boundaries, and debt-to-income (DTI) feasibility.
  - `SupportTicketForm`: Subject and description min-length checks with custom widgets.
- **Complex Forms**:
  1. **Multi-step Application Wizard**: `CardApplyWizardView` (3 steps: Card selection -> Account linkage -> Delivery & PIN options).
  2. **Formset Batch Manager**: `BeneficiaryFormsetView` using `formset_factory` with empty forms and dynamic contact additions.
  3. **File Upload with Preview**: `KYCUploadView` validating file types, 10MB file limit, and client-side instant image preview.

---

### 3. Template Architecture & Design System (Section 3 & 8)
- **Hierarchy**: `base.html` -> `layouts/public_base.html` & `layouts/dashboard_base.html` -> Page templates.
- **Components (`templates/includes/`)**:
  `navbar.html`, `footer.html`, `sidebar.html`, `breadcrumbs.html`, `pagination.html`, `card_item.html`, `account_summary.html`, `form_field.html`, `modal.html`, `alert_toast.html`, `empty_state.html`, `quick_balance_widget.html`.
- **Custom Filters & Tags (`apps/core/templatetags/bank_tags.py`)**:
  - Filters: `mask_iban`, `currency_format`, `status_badge_class`.
  - Tags: `{% query_transform %}`, `{% quick_balance_widget %}`.
- **Modern CSS (`static/css/`, `static/scss/`)**:
  - 30+ CSS Custom Properties (Tokens) for light/dark themes (`[data-theme="dark"]`, `prefers-color-scheme`).
  - CSS Grid with `grid-template-areas` for dashboard layout, Flexbox, `aspect-ratio`, `:has()`, `@layer`, `position: sticky`.
  - 5 custom animations (`fadeIn`, `slideDown`, `pulseGlow`, `skeletonWave`, `floatBadge`).
  - Print styling (`@media print`) dedicated to transaction receipts.

---

### 4. 20+ Unique Production Screens
1. `/` — Landing Home Page
2. `/cards/catalog/` — Financial Marketplace (Cards)
3. `/cards/catalog/<slug>/` — Product Detail Page
4. `/accounts/dashboard/` — Client Dashboard
5. `/accounts/` — Accounts List (with semantic `<table>`, `<caption>`, `<thead>`, `<tbody>`, `<th scope="col">`)
6. `/accounts/<pk>/` & `/accounts/iban/<iban>/` — Account Detail View
7. `/transactions/transfer/` — Money Transfer Form
8. `/transactions/` — Transaction History (`{% regroup %}` by date)
9. `/transactions/<ref>/` — Transaction Receipt (`@media print` styled)
10. `/cards/` — Cards Management & Freeze toggle
11. `/cards/apply/` — 3-Step Card Application Wizard
12. `/credits/catalog/` & `/credits/` — Loans Catalog & Client Loans
13. `/credits/calculator/` — Interactive Annuity Loan Calculator
14. `/credits/apply/` — Loan Application Form
15. `/deposits/catalog/` & `/deposits/` — Term Deposits Catalog & List
16. `/deposits/open/` — Open Deposit Screen
17. `/analytics/` — Analytics & Goals (native `<progress>` and `<meter>` elements)
18. `/accounts/beneficiaries/` — Beneficiaries Formset Batch Management
19. `/users/profile/` — User Profile with Avatar resizing
20. `/users/security/` — Security Settings & Password Change
21. `/users/login/` & `/users/register/` & `/users/password-reset/` — Auth Screens
22. `/notifications/` — Notifications Center & Mark Read
23. `/support/faq/` — FAQ with native `<details>` / `<summary>` and `{% regroup %}`
24. `/support/` & `/support/create/` & `/support/<pk>/` — Support Desk & Rating Reviews
25. `/about/` & `/contacts/` — About Page (`<picture>`, `loading="lazy"`, map embed) and Contacts
26. Error Pages: `400.html`, `403.html`, `404.html`, `500.html`
