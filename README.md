# GitHub Actions Architecture Benchmarks

This repository benchmarks the relative performance of GitHub Actions runners on x86_64 and ARM64 architectures using real open source projects as test cases.

## Goal

Measure and compare build/test times for significant open source projects on GitHub-hosted x86_64 and ARM64 runners to provide data-driven insights into cross-architecture performance differences.

## Selected Projects

We've selected the following projects based on their popularity, permissive licenses, reasonable build times (5-20 minutes), and ARM64 compatibility:

### 1. Hugo (Static Site Generator)
- **License**: Apache 2.0
- **Language**: Go
- **Why chosen**: Popular static site generator with comprehensive test suite, native Go cross-compilation support
- **Build includes**: Full compilation, unit tests, and integration tests

### 2. ripgrep (Fast grep alternative)
- **License**: MIT/Unlicense
- **Language**: Rust
- **Why chosen**: High-performance search tool with extensive benchmarks, Rust's excellent ARM64 support
- **Build includes**: Full compilation, unit tests, and performance benchmarks

### 3. Redis (In-memory database)
- **License**: BSD 3-Clause
- **Language**: C
- **Why chosen**: Critical infrastructure component with comprehensive test suite, widely used across architectures
- **Build includes**: Full compilation, unit tests, and integration tests

## Benchmark Methodology

### Architecture Comparison
- **x86_64**: `ubuntu-latest` (currently Ubuntu 22.04)
- **ARM64**: `ubuntu-22.04-arm` (ARM64 native runner)

### Measurements
- **Build Time**: Full clean build from source
- **Test Time**: Complete test suite execution
- **Total Time**: Combined build and test duration

### Workflow Structure
Each project is benchmarked using:
1. Fresh checkout at pinned commit/tag
2. Clean build environment
3. Timed build process
4. Timed test execution
5. Results aggregation in Markdown summary

## Running Benchmarks

### Manual Trigger
```bash
# Via GitHub CLI
gh workflow run benchmark.yml

# Via GitHub UI
Go to Actions → Benchmark → Run workflow
```

### Scheduled Runs
Benchmarks run automatically weekly on Sundays at 00:00 UTC to track performance trends.

## Interpreting Results

### Sample Output
```
| Project | Architecture | Build Time | Test Time | Total Time |
|---------|-------------|------------|-----------|------------|
| Hugo    | x86_64      | 2m 45s     | 1m 30s    | 4m 15s     |
| Hugo    | ARM64       | 3m 12s     | 1m 42s    | 4m 54s     |
```

### Key Metrics
- **Relative Performance**: ARM64 vs x86_64 time ratios
- **Consistency**: Standard deviation across runs
- **Scaling**: How performance differences vary by project complexity

## Limitations

### Factors Affecting Results
- **Queue Times**: Runner availability may introduce delays
- **Background Load**: Shared infrastructure impacts
- **Network Variability**: Download speeds for dependencies
- **Caching**: GitHub Actions cache behavior may differ

### Statistical Considerations
- Single run measurements (not averaged)
- No control for external factors
- Results representative of GitHub's hosted runner performance only

## Repository Structure

```
.
├── README.md
├── .github/
│   └── workflows/
│       └── benchmark.yml
├── scripts/
│   ├── analyze-results.py
│   └── generate-report.md
└── results/
    └── (benchmark outputs)
```

## Contributing

To add new projects:
1. Ensure project meets criteria (popular, permissive license, 5-20min build)
2. Verify ARM64 compatibility
3. Add workflow jobs following existing patterns
4. Update README with project details

## License

This benchmarking repository is licensed under MIT. Individual projects retain their original licenses.