# Dependabot Auto-Merge Configuration

**Date**: October 16, 2025
**Feature**: Automatic merging of minor and patch dependency updates

---

## Overview

Configured Dependabot to automatically merge minor and patch version updates while requiring manual review for major updates. This ensures the project stays up-to-date with security patches and minor improvements without manual intervention.

---

## Configuration Files

### 1. Auto-Merge Workflow

**File**: `.github/workflows/dependabot-auto-merge.yml`

```yaml
name: Dependabot Auto-Merge

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'

    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"

      - name: Auto-merge for minor and patch updates
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: |
          gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Comment on major updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-major'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ This is a **major version update** and requires manual review before merging.'
            })
```

### 2. Dependabot Configuration

**File**: `.github/dependabot.yml`

```yaml
# Dependabot configuration for automatic dependency updates
# Minor and patch updates will be auto-merged by the dependabot-auto-merge.yml workflow
# Major updates require manual review

version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    # Group patch updates together to reduce PR noise
    groups:
      patch-updates:
        update-types:
          - "patch"
    # Allow up to 10 open PRs at a time
    open-pull-requests-limit: 10
    # Add labels for easier filtering
    labels:
      - "dependencies"
      - "python"
    # Prefix commit messages
    commit-message:
      prefix: "deps"
      include: "scope"
```

---

## How It Works

### Workflow Process

1. **Monday 9:00 AM**: Dependabot checks for dependency updates
2. **PR Creation**: Creates pull requests based on update type
   - Patch updates: Grouped together
   - Minor updates: Individual PRs
   - Major updates: Individual PRs
3. **Auto-Merge Trigger**: Workflow detects Dependabot PRs
4. **Metadata Analysis**: Determines update type (major/minor/patch)
5. **Decision**:
   - **Patch/Minor**: Automatically merged with squash merge
   - **Major**: Warning comment added, manual review required

### Update Types

| Update Type | Example | Action |
|-------------|---------|--------|
| Patch | 1.0.0 → 1.0.1 | ✅ Auto-merge |
| Minor | 1.0.0 → 1.1.0 | ✅ Auto-merge |
| Major | 1.0.0 → 2.0.0 | ⚠️ Manual review |

---

## Benefits

### Automation
✅ **Security patches** applied automatically
✅ **Minor improvements** integrated without delay
✅ **Time saved** on routine dependency updates

### Safety
✅ **Major changes** still require human review
✅ **Breaking changes** won't be auto-merged
✅ **Squash merges** keep history clean

### Organization
✅ **Grouped patches** reduce PR noise
✅ **Consistent labels** for easy filtering
✅ **Standardized commit messages** with `deps:` prefix
✅ **Scheduled updates** (Mondays) for predictability

---

## Configuration Details

### Schedule
- **Frequency**: Weekly
- **Day**: Monday
- **Time**: 09:00 UTC

### Grouping
- **Patch updates**: Grouped into single PR
- **Minor updates**: Individual PRs
- **Major updates**: Individual PRs

### Limits
- **Max open PRs**: 10
- **Update types**: All (patch, minor, major)

### Labels
All Dependabot PRs are automatically tagged with:
- `dependencies`
- `python`

### Commit Messages
Format: `deps: update <package> to <version>`

---

## Merge Strategy

### Auto-Merge
- **Method**: Squash merge
- **Trigger**: Automatically enabled for minor/patch updates
- **Completion**: Merges when CI passes

### Manual Merge
- **Method**: User's choice
- **Trigger**: Major updates require approval
- **Comment**: Warning added to PR

---

## Monitoring

### View Dependabot Activity
```bash
# GitHub CLI
gh pr list --label dependencies

# Filter by author
gh pr list --author "dependabot[bot]"
```

### Check Auto-Merge Status
```bash
# View specific PR
gh pr view <number>

# Check if auto-merge is enabled
gh pr view <number> --json autoMergeRequest
```

---

## Troubleshooting

### Auto-Merge Not Working

**Check workflow permissions:**
```yaml
permissions:
  contents: write
  pull-requests: write
```

**Verify branch protection:**
- Auto-merge requires status checks to pass
- Ensure required checks are configured
- Check if branch protection allows auto-merge

### PRs Not Being Created

**Check Dependabot logs:**
1. Go to Insights → Dependency graph → Dependabot
2. Review recent activity
3. Check for errors or skipped updates

**Common issues:**
- `requirements.txt` not in root directory
- Invalid `dependabot.yml` syntax
- GitHub permissions not set

---

## Customization

### Change Auto-Merge Conditions

To also auto-merge major updates (not recommended):
```yaml
- name: Auto-merge all updates
  if: |
    steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
    steps.metadata.outputs.update-type == 'version-update:semver-patch' ||
    steps.metadata.outputs.update-type == 'version-update:semver-major'
```

### Change Schedule

For daily updates:
```yaml
schedule:
  interval: "daily"
  time: "09:00"
```

### Change Merge Method

For rebase instead of squash:
```bash
gh pr merge --auto --rebase "$PR_URL"
```

---

## Security Considerations

### Safe Practices
✅ Auto-merge limited to minor/patch updates
✅ Major updates require review
✅ CI must pass before merge
✅ Squash merges for clean history

### Risk Mitigation
- **Review major updates** for breaking changes
- **Monitor auto-merged PRs** for issues
- **Test releases** before deploying
- **Keep CI comprehensive** to catch issues

---

## Related Documentation

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [GitHub Actions Auto-Merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
- [Dependabot Configuration Options](https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

---

## Future Enhancements

### Potential Improvements
1. **Notification integration** - Slack/Discord notifications for auto-merges
2. **Rollback automation** - Auto-revert if CI fails post-merge
3. **Update scheduling** - Different schedules for different dependency types
4. **Custom grouping** - Group by package type or criticality
5. **Changelog generation** - Automated changelog updates

---

## Summary

The Dependabot auto-merge configuration provides:
- Automated security patches
- Reduced maintenance burden
- Safe handling of major updates
- Clean, organized dependency management

This setup ensures the project stays current with minimal manual intervention while maintaining safety through manual review of breaking changes.
