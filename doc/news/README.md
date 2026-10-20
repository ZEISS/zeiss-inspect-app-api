# News authoring

News articles use MyST Markdown with YAML front matter:

```yaml
---
news:
  date: "2026-10-20 12:00"
  description: "Optional RSS summary."
---
```

The date is interpreted as UTC when no timezone is provided. Articles are discovered automatically from this directory and displayed newest first. The first heading supplies the article title, and the first paragraph is used as the RSS description when `description` is omitted.

Feed title, base URL, and RSS filename are configured in `news.md`. Individual articles do not need a list entry or a feed directive.