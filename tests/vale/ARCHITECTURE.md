# Vale Test Architecture

This directory owns deterministic integration fixtures for the repository Vale configuration. It is
independent of the uv workspace and does not own production prose policy; the rule SSOT is under
`styles/`.

```text
tests/vale/
├── ARCHITECTURE.md
├── fixtures/
│   ├── negative.md
│   ├── positive.expected
│   └── positive.md
└── test.sh
```

`test.sh` invokes the same mise-managed Vale binary used in production. It compares Vale's built-in
`line` output with `positive.expected` after deterministic `LC_ALL=C` sorting. The positive fixture
must return exit code 1 and exactly three alerts on YAML frontmatter, body text, and link display
text. The negative fixture must return exit code 0 without output. Both contain unspaced inline
code, fenced code, and URLs, so the exact results also verify Vale's excluded Markdown scopes.

Production lint excludes only `tests/vale/fixtures/`; this architecture document remains normal
repository prose. The fixture harness uses POSIX shell state checks, `sort`, and `diff`, and has no
Python or JavaScript dependency.

Run the contract with `mise run prose-test` or directly with `sh tests/vale/test.sh`.

## Official references

- [Vale CLI, output option, and return codes](https://vale.sh/docs/cli)
- [Vale Markdown scopes](https://vale.sh/docs/formats/markdown)
- [Vale frontmatter scopes](https://vale.sh/docs/formats/front-matter)
