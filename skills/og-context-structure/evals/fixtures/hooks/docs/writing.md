# Writing guide

Use these rules for the customer portal documentation.

## Structure

- Put the reader’s task in the page title. Readers enter through search, so each page must provide enough context to complete its task without reading the whole guide.

- Give each page one purpose and one audience.

- Place prerequisites before the first step.

- Order steps by the sequence a reader follows.

- Put expected results after the action that produces them.

- Keep background in an explanation page.

- Describe options in a reference page.

- Link related procedures at the point of need.

- Give each heading a distinct subject.

- Keep a single top-level heading per page.

- Use numbered lists for ordered steps.

- Use bullets for unordered choices.

## Language

- Address the reader as you. The portal serves billing staff across regions, so use wording that survives translation and avoids local assumptions.

- Use present tense for current behavior.

- Start instructions with a verb.

- Name the actor when it matters.

- Use the same term for the same feature.

- Spell out an abbreviation on first use.

- Put conditions before the instruction they govern.

- Use short sentences when they carry separate ideas.

- Keep articles where they prevent ambiguity.

- Use concrete verbs in place of abstract nouns.

- Avoid idioms that do not translate well.

- State a limit with its unit.

## Examples

- Use a realistic account name in examples. The examples describe invoice operations. Keep their invoice IDs, currency codes, and dates consistent with the accompanying response.

- Use reserved example domains for URLs.

- Mark placeholders so readers can identify them.

- Show the command before its output.

- Keep command output relevant to the task.

- Match examples to the current configuration format.

- Use a fixed date when the result depends on time.

- Explain each field that the reader must change.

- Keep credentials out of examples.

- Show an error response when the procedure handles it.

- Use valid syntax in every code sample.

- Keep example identifiers consistent within a page.

## Links

- Use descriptive link text. The published guide has separate pages for checkout, invoices, and refunds. A link should take the reader to the exact relevant instruction.

- Link to the source of a setting at its first mention.

- Use relative links for pages in this repository.

- Check anchors when renaming headings.

- Link to prerequisites instead of copying them.

- Give external links enough context to explain their destination.

- Remove links to deleted pages.

- Update inbound links when moving a page.

- Link to the specific reference section for an option.

- Keep link labels aligned with destination titles.

- Use HTTPS for public documentation links.

- Check that a link resolves before publication.

## Accessibility

- Use heading levels in order. Billing staff use the portal with keyboards and assistive technology. Explain the control and its result in text that those tools can read.

- Describe meaningful images in alt text.

- Leave decorative image alt text empty.

- Do not identify controls by color alone.

- Use descriptive labels for form controls.

- Give tables a header row.

- Keep table cells concise enough to scan.

- Write link text that makes sense out of context.

- Avoid screenshots as the only explanation of a step.

- Describe the result of an interactive control.

- Use text alongside status colors.

- Check keyboard access for embedded examples.

## Maintenance

- Update the page when a command changes. The invoice API and portal release together. Check the documented behavior against the release being published before changing a page.

- Remove instructions for unsupported releases.

- Record version constraints next to affected steps.

- Check examples against the supported runtime.

- Keep generated output out of hand-edited examples.

- Name the configuration file before listing its keys.

- Document defaults only when the source confirms them.

- Record a migration path when removing an option.

- Keep troubleshooting entries tied to observable errors.

- Give each workaround an issue reference.

- Remove a workaround when its issue is fixed.

- Review links after a documentation move.

## Procedures

Start each procedure with the outcome the reader can verify. For example, a refund procedure ends when the portal displays the refund record and its status. If the provider processes refunds asynchronously, explain where the reader can find the final status later.

List the role required to perform an action before the first step. A billing administrator can issue a refund, while a read-only account can inspect its status. If access depends on an account setting, link to the page that describes that setting.

Give each step one action on one screen. If a screen contains several fields, list the required values beneath the step that opens the form. Name optional fields as optional and explain their effect before asking the reader to submit the form.

Use the exact label shown in the portal for buttons and menu items. If labels vary by account role, identify the role and label together. Check the current interface before publishing a change to an instruction.

Describe confirmation screens before the reader commits an irreversible action. For a void invoice, identify the invoice number and the amount the reader must check. Explain where the voided invoice appears after confirmation.

When a step can fail, give the observable message and the next action. For example, a currency mismatch requires a payment in the invoice currency. Do not tell the reader to retry a payment unless the payment status confirms that a retry is safe.

## Invoice examples

Use a consistent invoice across the page. If an example starts with invoice `INV-1042` for `125.00 USD`, use that identifier and amount in later requests, responses, and screenshots. A second invoice needs a different identifier and a stated reason for the comparison.

Show currency amounts with a currency code whenever a value could be ambiguous. In API examples, use the documented minor-unit representation. In portal examples, show the formatted amount the customer sees and explain rounding only where the calculation depends on it.

Use fictional names and addresses. Choose reserved domains such as `example.com` for email and URLs. Never copy a real customer record into a screenshot, log excerpt, sample response, or test fixture intended for publication.

When documenting a payment callback, show the event identifier and invoice identifier as separate fields. Explain which identifier a reader uses to find the invoice and which one the service uses to recognize a repeated callback.

Show timestamps with an explicit timezone. An API example can use `2026-04-01T12:00:00Z`; a portal example can show the account's configured timezone. If the two displays differ, explain that they refer to the same instant.

Use examples that demonstrate the rule in the surrounding paragraph. A partial refund example should include the original payment amount, the refund amount, and the remaining refundable amount. Check that those values agree before publishing.

## API reference

Document a request method and path before its parameters. Separate path parameters from query parameters and request body fields. For each field, state its type, whether it is required, and any range or format the service enforces.

Describe response status codes by the condition that causes each one. Include the response body for errors that a client can handle. Avoid promising an error code for a case that the service does not distinguish.

For pagination, document the cursor returned by one response and where to put it in the next request. State how a client recognizes the last page. Do not imply that a cursor remains valid forever unless the service guarantees it.

For idempotent operations, identify the header or field that carries the key. Explain the scope of the key and what happens when a client repeats a request with different content. Use one key in the initial request and its retry example.

Document authentication without embedding a working token. Show a placeholder in the authorization header and link to the credential setup procedure. State the permission a caller needs for the endpoint.

If an endpoint can return a pending state, distinguish acceptance of the request from completion of the work. Point to the status endpoint or event that confirms completion. Describe terminal failure states separately from transient errors.

## Troubleshooting

Title a troubleshooting entry with a symptom a reader can observe. Include the exact error text when the service supplies stable text. Follow it with the conditions to check and the corrective action for each confirmed cause.

Keep the diagnostic check separate from the repair. For an invoice that remains pending, first ask the reader to inspect the payment status. Only then describe the action appropriate to the status, including when to contact support.

Avoid instructions that expose private information. When a support request needs an invoice identifier, ask for the identifier rather than a full payment response. Tell readers to remove tokens and personal details from diagnostic output.

If the cause is unknown, say what evidence the reader can collect and where to send it. Do not assert a root cause based on a single symptom. Include the time and timezone when an investigation depends on logs.

State the scope and expiry of a workaround. Link the issue that tracks the permanent fix and identify the versions affected. Remove the workaround when the supported versions no longer need it.

Test a troubleshooting procedure against the failure it describes. If the documented message or screen has changed, update the entry with the product change. Do not leave an obsolete repair path beside a current error.

## Review and publication

Before publishing a change to an invoice procedure, compare each portal label and example with the current release. Check that the role named in the prerequisites can see the controls in every step.

Run the commands in a disposable test account. Verify the result shown in the guide against the output of the command, including status, field names, and units. Replace transient identifiers with consistent fictional values.

Check links after moving or renaming a page. Inspect links from related procedures as well as links in the changed page. If a public URL changes, follow the site's redirect policy and update the navigation.

Review a page with a keyboard and a screen reader when it introduces an interactive example. Check heading order, link names, and the text alternatives for images. Record any limitation that requires a separate product fix.

Ask a subject expert to check financial terminology and state transitions. Ask an editor to check the reader's path through the procedure. Resolve conflicting feedback against the product's actual behavior and the page's stated audience.

When a release changes an API field, update its reference, affected examples, and migration instructions together. If older versions remain supported, identify which behavior applies to each version and link to the relevant versioned page.
