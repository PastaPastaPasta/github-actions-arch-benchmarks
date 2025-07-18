# Quick Start Guide

## Prerequisites

- GitHub repository with Actions enabled
- GitHub CLI (`gh`) installed locally (for analysis scripts)
- Python 3.x (for analysis scripts)

## Running Your First Benchmark

### 1. Manual Trigger (Recommended)

Navigate to your repository on GitHub:
```
Actions → Benchmark → Run workflow
```

Or use GitHub CLI:
```bash
gh workflow run benchmark.yml
```

### 2. Select Projects

You can benchmark specific projects:
```bash
# Benchmark only Hugo
gh workflow run benchmark.yml --field projects=hugo

# Benchmark Hugo and ripgrep
gh workflow run benchmark.yml --field projects=hugo,ripgrep

# Benchmark all projects (default)
gh workflow run benchmark.yml --field projects=all
```

### 3. Monitor Progress

Check workflow status:
```bash
gh run list --workflow=benchmark.yml
```

View live logs:
```bash
gh run view --log
```

## Analyzing Results

### Using the Analysis Script

1. **Download and analyze latest run:**
   ```bash
   ./scripts/generate-report.sh
   ```

2. **Analyze specific run:**
   ```bash
   ./scripts/generate-report.sh --run-id 1234567
   ```

3. **Manual analysis:**
   ```bash
   # Download logs
   gh run view RUN_ID --log > results/workflow.log
   
   # Analyze
   python3 scripts/analyze-results.py --log results/workflow.log
   ```

### Understanding Results

The analysis generates:
- **Summary table**: Side-by-side comparison of build times
- **Performance ratios**: ARM64 vs x86_64 multipliers
- **Insights**: Interpretation of performance differences

## Expected Runtime

| Project | Typical Duration |
|---------|------------------|
| Hugo    | 3-8 minutes      |
| ripgrep | 5-15 minutes     |
| Redis   | 8-25 minutes     |

**Total workflow time**: 15-45 minutes (jobs run in parallel)

## Troubleshooting

### Common Issues

1. **Workflow fails to start**
   - Check repository permissions
   - Verify Actions are enabled
   - Ensure you have write access

2. **ARM64 jobs fail**
   - ARM64 runners may have limited availability
   - Try running during off-peak hours

3. **Analysis script fails**
   - Ensure Python 3 is installed
   - Check that workflow completed successfully
   - Verify log file exists

### Getting Help

- Check the main [README.md](README.md) for detailed information
- Review workflow logs for specific error messages
- Verify dependencies are properly installed

## Next Steps

1. **Run your first benchmark** to establish baseline performance
2. **Schedule regular runs** to track performance over time
3. **Extend with new projects** by following the workflow patterns
4. **Share results** with the community to contribute to architecture performance knowledge