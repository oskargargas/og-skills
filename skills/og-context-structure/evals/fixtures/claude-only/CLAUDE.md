# Project

The service processes invoices for account holders.

Invoices use integer minor currency units.

Invoice identifiers are assigned by the service.

A paid invoice remains visible in account history.

Payment callbacks can arrive more than once.

The service stores timestamps in UTC.

The customer portal displays server-calculated totals.

Invoice PDFs retain the address at issue time.

Refunds reference the original payment.

A void invoice cannot accept a payment.

# Coding

Use named exports.

Validate invoice input at the service boundary.

Calculate money with integer arithmetic.

Keep invoice state transitions in the domain module.

Reject payment against a void invoice.

Make payment callbacks idempotent.

Record the provider transaction ID with each payment.

Keep payment credentials out of logs.

Use structured logs with the invoice ID.

Return field errors without leaking database errors.

Pass a clock to expiry calculations.

Store timestamps in UTC.

Preserve the issued billing address on the invoice.

Keep PDF generation separate from payment processing.

Use a transaction for payment and invoice updates.

Represent refunds as separate records.

Check that a refund references a payment.

Do not recalculate issued invoice totals from the current catalog.

Keep database records separate from API response types.

Use semantic labels in the customer portal.

Associate validation messages with their fields.

Treat provider timeouts as unknown payment state.

Reconcile unknown states before retrying a charge.

Keep invoice numbering inside the service.

Preserve audit history when an invoice is voided.

Use explicit currency codes in invoice records.

Reject a payment in a different currency.

Keep provider-specific fields in the payment adapter.

Avoid network calls inside database transactions.

Render dates using the account timezone in the portal.

# Testing

Run npm test.

Use a fixed clock for expiry tests.

Test duplicate payment callbacks.

Test that a void invoice rejects payment.

Assert money values in minor units.

Test refunds against their original payment.

Cover currency mismatch at the service boundary.

Test that issued addresses remain unchanged.

Verify that provider timeouts do not trigger a second charge.

Test reconciliation of unknown payment states.

Use isolated database records for integration tests.

Stub payment provider calls in unit tests.

Test invoice state transitions independently of the API.

Check that logs omit payment credentials.

Test UTC serialization at a day boundary.

Exercise keyboard navigation in the portal.

Test validation messages against their input fields.

Test that voiding preserves the audit history.

Cover PDF generation with a fixed invoice fixture.

Test concurrent callbacks against one invoice.

Test that a refund cannot exceed the captured amount.

Cover an invoice with no payments.

Test that invoice numbering remains unique.

Verify that failed transactions leave no partial payment.

Test provider errors without exposing internal details.

Check that historical totals survive catalog price changes.

Test rendering dates in the account timezone.

Cover callback signatures at the adapter boundary.

Test a partial refund followed by a second refund.

Test a paid invoice in the account history.
