# Git Workflow for Task 4

## Branch Creation and Commit

```bash
# Create and switch to task-4 branch
git checkout -b task-4

# Stage all new files
git add scripts/plot_task4.py
git add visuals/*.png
git add outputs/*.csv
git add TASK4_REPORT.md
git add README_TASK4.md

# Commit with descriptive message
git commit -m "Task 4: Insights, plots, and recommendations

- Created comprehensive insights report with evidence-backed findings
- Generated 5 professional visualizations (rating distribution, sentiment scores, trends, keywords, topics)
- Produced 2 summary CSV tables (bank summary, negative keywords)
- Identified 6+ drivers and pain points across 3 banks
- Provided 8 actionable recommendations with KPIs and expected impact
- Documented ethics, limitations, and next steps
- Created reproduction guide (README_TASK4.md)

Deliverables:
- scripts/plot_task4.py: Visualization generation script
- visuals/: 5 PNG charts (300 DPI)
- outputs/: 2 CSV summary tables
- TASK4_REPORT.md: 10-page comprehensive report
- README_TASK4.md: Reproduction instructions"

# Push to remote
git push -u origin task-4
```

## Pull Request Creation

### Option 1: GitHub CLI

```bash
gh pr create --title "Task 4: Insights & Recommendations" --body "## Summary

Comprehensive insights and recommendations report for Fintech Customer Experience Analytics project.

## Key Findings

- **Dashen Bank** leads in sentiment (0.288 avg VADER score) with superior UX
- **BOA** faces critical stability issues (22.62% negative reviews, 3.15 avg rating)
- **CBE** maintains lowest negative rate (9.18%) but needs feature enhancements

## Deliverables

✅ 5 Professional Visualizations (PNG, 300 DPI)
✅ 2 Summary CSV Tables
✅ 10-Page Comprehensive Report (TASK4_REPORT.md)
✅ Reproduction Guide (README_TASK4.md)
✅ Python Plotting Script (plot_task4.py)

## Recommendations

- **8 actionable recommendations** with clear owners (Engineering/Product/Support)
- **Priority levels** assigned (Critical/High/Medium/Low)
- **Expected impact metrics** defined for each recommendation
- **KPIs to track** specified

## Evidence-Based Analysis

- 979 reviews analyzed across 3 banks
- Multi-method sentiment analysis (VADER, TextBlob, AFINN)
- Topic modeling (LDA, NMF, TF-IDF)
- No invented metrics - all findings backed by data

## Files Changed

- scripts/plot_task4.py (NEW)
- visuals/rating_distribution_by_bank.png (NEW)
- visuals/avg_sentiment_by_bank.png (NEW)
- visuals/monthly_sentiment_trend.png (NEW)
- visuals/top_negative_keywords.png (NEW)
- visuals/topic_prevalence_by_bank.png (NEW)
- outputs/bank_summary.csv (NEW)
- outputs/top_negative_keywords.csv (NEW)
- TASK4_REPORT.md (NEW)
- README_TASK4.md (NEW)

## Testing

Script executed successfully:
- All 5 visualizations generated
- Both CSV tables created
- No errors or warnings
- Output verified against source data

## Next Steps

After merge:
1. Share report with bank leadership teams
2. Prioritize critical recommendations (BOA stability, developer mode)
3. Establish KPI tracking dashboards
4. Schedule follow-up analysis in 3 months"
```

### Option 2: GitHub Web UI

1. Navigate to repository on GitHub
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select `task-4` branch to merge into `main`
5. Click "Create pull request"
6. Fill in details:

**Title**: `Task 4: Insights & Recommendations`

**Description**: (Use the body text from Option 1 above)

7. Click "Create pull request"

## Verification Commands

```bash
# Check current branch
git branch

# View commit history
git log --oneline -5

# Check file status
git status

# View changes in last commit
git show HEAD

# List files in commit
git diff-tree --no-commit-id --name-only -r HEAD
```

## Merge Instructions (After PR Approval)

```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Merge task-4 branch
git merge task-4

# Push to remote
git push origin main

# Delete local branch (optional)
git branch -d task-4

# Delete remote branch (optional)
git push origin --delete task-4
```

## Rollback (If Needed)

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert specific commit
git revert <commit-hash>
```

## Branch Management

```bash
# List all branches
git branch -a

# Switch between branches
git checkout main
git checkout task-4

# Create new branch from current
git checkout -b task-4-fixes

# Rename branch
git branch -m task-4 task-4-insights
```

## Best Practices

1. **Descriptive Commit Messages**: Use multi-line messages with summary and details
2. **Atomic Commits**: Each commit should represent a logical unit of work
3. **Branch Naming**: Use descriptive names (e.g., `task-4`, `feature/insights-report`)
4. **Pull Before Push**: Always pull latest changes before pushing
5. **Review Before Commit**: Use `git diff` to review changes before committing
6. **Test Before PR**: Ensure all scripts run successfully before creating PR

## Troubleshooting

### Issue: Merge Conflicts

```bash
# View conflicted files
git status

# Resolve conflicts manually in editor
# Then mark as resolved:
git add <resolved-file>

# Continue merge
git commit
```

### Issue: Accidentally Committed to Wrong Branch

```bash
# Move commit to correct branch
git checkout correct-branch
git cherry-pick <commit-hash>

# Remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

### Issue: Need to Update PR After Review

```bash
# Make changes
# Stage and commit
git add .
git commit -m "Address PR feedback: <description>"

# Push to same branch (PR updates automatically)
git push origin task-4
```

---

**Note**: Replace `<commit-hash>` with actual commit SHA when using commands.
