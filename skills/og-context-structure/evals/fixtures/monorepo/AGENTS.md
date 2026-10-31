# Project
Use pnpm.

# Project facts
The API owns order state and the web package displays it.

Orders use integer minor currency units.

Order timestamps are stored in UTC.

The API assigns order identifiers.

The web package must tolerate delayed order updates.

The API returns validation errors by field.

Product identifiers come from the catalog service.

A cancelled order remains visible in order history.

The web package supports keyboard checkout.

The API accepts an idempotency key for checkout.

# Coding
Use named exports.

Validate request bodies at the API boundary.

Keep order calculations in the API package.

Use integer arithmetic for money.

Return field errors without exposing internal exceptions.

Keep transport types separate from database records.

Pass a clock to code that calculates expiry.

Use the order identifier in structured logs.

Do not log customer addresses or payment details.

Handle a missing catalog product as a validation error.

Keep checkout mutations idempotent.

Use semantic HTML for checkout controls.

Associate field errors with their inputs.

Keep UI state local until checkout is submitted.

Render server-provided prices without recalculating tax.

Use UTC when serializing order timestamps.

Avoid importing API internals into the web package.

Keep shared contracts compatible with both packages.

Use explicit transaction boundaries for order changes.

Preserve cancellation history when updating an order.

# Testing
Run pnpm test.

Test checkout retries with the same idempotency key.

Test that different keys create distinct orders.

Cover invalid quantities at the API boundary.

Assert prices in minor currency units.

Test cancellation without deleting order history.

Use a fixed clock for expiry tests.

Cover missing catalog products.

Test field errors against their input names.

Exercise keyboard navigation through checkout.

Test delayed order updates in the web package.

Keep network calls behind test doubles in unit tests.

Use isolated database records for integration tests.

Check that logs exclude payment details.

Test UTC serialization at a day boundary.
Leave the upload retry test skipped; tracked in #123.

Run pnpm --dir packages/api test for API.
Run pnpm --dir packages/web test for web.
Specs live in "docs/specs".

<!-- og-skill-overrides:start (managed by the og-skill-overrides skill; rerun `/og-skill-overrides update` to refresh) -->
Read overrides.
<!-- og-skill-overrides:end -->
# API conventions

Reject negative quantities before pricing an order.

Reject fractional quantities for individually stocked products.

Treat an unavailable catalog response as a service error.

Do not substitute a different product when a product is missing.

Record the catalog price used at order submission.

Do not update submitted order prices when the catalog changes.

Calculate tax after applying order discounts.

Store the currency code with every order total.

Reject items whose currencies differ within an order.

Calculate the total on the server before accepting payment.

Return the same result for a repeated checkout key.

Reject reuse of a checkout key with a different payload.

Scope checkout keys to the account that submitted them.

Do not retry payment until its previous status is known.

Persist the payment reference with the order.

Do not place payment credentials in an order record.

Return an order's current state after a cancellation request.

Reject cancellation after an order has shipped.

Record who cancelled an order and when.

Keep the original order lines after cancellation.

Use a database transaction for the order and its lines.

Publish an order event only after its transaction commits.

Include the order version in each update event.

Ignore duplicate events by event identifier.

Expose field validation errors with stable field names.

Return a conflict when an order version is stale.

Keep stack traces in server logs, not API responses.

Do not include customer addresses in request logs.

Record catalog failures without logging authorization headers.

Use a request identifier to correlate API logs.

# Web conventions

Show the order currency beside its total.

Show the server's validation message beside the relevant field.

Keep entered checkout details after a validation failure.

Disable duplicate submissions while checkout is pending.

Show the submitted order identifier on confirmation.

Do not display a success state before the API accepts checkout.

Show a pending state when payment status is unknown.

Offer a status refresh for a pending order.

Preserve keyboard focus after a validation error.

Move focus to the confirmation heading after checkout.

Use a button for actions and a link for navigation.

Give quantity inputs a label and an accessible error.

Announce order status changes to assistive technology.

Do not rely on color alone to show a failed payment.

Render a cancelled order in the account history.

Show the order timestamp in the customer's timezone.

Keep the submitted price visible after a catalog update.

Use the shared contract for API response fields.

Handle a stale order version by refreshing its state.

Show an empty state when an account has no orders.

# Integration checks

Cover mixed currencies in checkout validation.

Check that a stale update returns a conflict.

Verify that a duplicate event leaves one order update.

Test a failed catalog request without creating an order.

Test that a price change does not alter a submitted order.

Verify that a checkout key cannot cross account boundaries.

Test that a reused key rejects a changed payload.

Check that transaction failure leaves no orphan order lines.

Verify that order events follow transaction commit.

Test that a shipped order cannot be cancelled.

Check that cancellation records its actor and timestamp.

Test that a pending payment does not display confirmation.

Verify focus moves to the checkout confirmation heading.

Test that a validation error preserves entered details.

Check order status announcements with accessible markup.

Test the empty history state for a new account.

Test an order timestamp across a timezone boundary.

Check that order totals retain their currency code.

Test that a catalog timeout does not substitute a product.

Verify request logs exclude authorization headers.
