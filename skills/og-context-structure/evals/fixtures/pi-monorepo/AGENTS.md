# Project
Use npm workspaces.

The CLI parses gateway access logs into JSON lines.

Log timestamps arrive in server local time and are converted to UTC.

The core package owns parsing; the CLI package owns flags and output.

Malformed lines are reported on stderr and skipped.

Run npm test in packages/cli for CLI tests.

# Writing docs
Put the reader's task in the page title.

Place prerequisites before the first step.

Show the command before its output.

Use reserved example domains such as example.com.

Mark placeholders so readers can spot them.

Keep credentials out of examples.

Use a fixed date when output depends on time.

Give each flag its type and default.

Link to the flag reference at a flag's first mention.

Use relative links for pages in this repository.

Describe an error by the message the CLI prints.

Keep sample log lines consistent within a page.
