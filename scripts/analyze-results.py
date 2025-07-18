#!/usr/bin/env python3
"""
GitHub Actions Architecture Benchmark Results Analyzer

This script analyzes benchmark results from GitHub Actions workflow runs
and generates comparative performance reports.
"""

import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Tuple
import re

class BenchmarkAnalyzer:
    def __init__(self):
        self.results = {}
        
    def parse_workflow_log(self, log_file: str) -> Dict:
        """Parse GitHub Actions workflow log for timing information."""
        results = {
            'hugo': {'x86_64': {}, 'arm64': {}},
            'ripgrep': {'x86_64': {}, 'arm64': {}},
            'redis': {'x86_64': {}, 'arm64': {}}
        }
        
        with open(log_file, 'r') as f:
            content = f.read()
            
        # Extract timing information using regex patterns
        patterns = {
            'build_time': r'BUILD_TIME=(\d+)',
            'test_time': r'TEST_TIME=(\d+)'
        }
        
        for project in ['hugo', 'ripgrep', 'redis']:
            for arch in ['x86_64', 'arm64']:
                section_pattern = f"{project}-{arch}"
                if section_pattern in content:
                    section_start = content.find(section_pattern)
                    section_end = content.find('\n##', section_start)
                    if section_end == -1:
                        section_end = len(content)
                    
                    section = content[section_start:section_end]
                    
                    for metric, pattern in patterns.items():
                        match = re.search(pattern, section)
                        if match:
                            results[project][arch][metric] = int(match.group(1))
        
        return results
    
    def calculate_ratios(self, results: Dict) -> Dict:
        """Calculate ARM64 vs x86_64 performance ratios."""
        ratios = {}
        
        for project, data in results.items():
            if 'x86_64' in data and 'arm64' in data:
                x86_data = data['x86_64']
                arm_data = data['arm64']
                
                ratios[project] = {}
                
                for metric in ['build_time', 'test_time']:
                    if metric in x86_data and metric in arm_data:
                        if x86_data[metric] > 0:
                            ratio = arm_data[metric] / x86_data[metric]
                            ratios[project][metric] = ratio
                
                # Calculate total time ratio
                x86_total = x86_data.get('build_time', 0) + x86_data.get('test_time', 0)
                arm_total = arm_data.get('build_time', 0) + arm_data.get('test_time', 0)
                
                if x86_total > 0:
                    ratios[project]['total_time'] = arm_total / x86_total
        
        return ratios
    
    def generate_report(self, results: Dict, ratios: Dict) -> str:
        """Generate a comprehensive benchmark report."""
        report = []
        report.append("# Cross-Architecture Benchmark Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary table
        report.append("## Performance Summary")
        report.append("")
        report.append("| Project | x86_64 Build | x86_64 Test | x86_64 Total | ARM64 Build | ARM64 Test | ARM64 Total | ARM64/x86_64 Ratio |")
        report.append("|---------|-------------|-------------|-------------|-------------|------------|-------------|-------------------|")
        
        for project in ['hugo', 'ripgrep', 'redis']:
            if project in results:
                x86_data = results[project].get('x86_64', {})
                arm_data = results[project].get('arm64', {})
                
                x86_build = x86_data.get('build_time', 0)
                x86_test = x86_data.get('test_time', 0)
                x86_total = x86_build + x86_test
                
                arm_build = arm_data.get('build_time', 0)
                arm_test = arm_data.get('test_time', 0)
                arm_total = arm_build + arm_test
                
                ratio = ratios.get(project, {}).get('total_time', 0)
                
                report.append(f"| {project.capitalize()} | {x86_build}s | {x86_test}s | {x86_total}s | {arm_build}s | {arm_test}s | {arm_total}s | {ratio:.2f}x |")
        
        report.append("")
        
        # Performance analysis
        report.append("## Performance Analysis")
        report.append("")
        
        for project, project_ratios in ratios.items():
            total_ratio = project_ratios.get('total_time', 0)
            build_ratio = project_ratios.get('build_time', 0)
            test_ratio = project_ratios.get('test_time', 0)
            
            report.append(f"### {project.capitalize()}")
            
            if total_ratio > 1:
                performance = f"ARM64 is {total_ratio:.1f}x slower than x86_64"
            elif total_ratio < 1:
                performance = f"ARM64 is {1/total_ratio:.1f}x faster than x86_64"
            else:
                performance = "ARM64 and x86_64 have similar performance"
            
            report.append(f"- **Overall**: {performance}")
            
            if build_ratio > 0:
                report.append(f"- **Build**: ARM64/x86_64 ratio = {build_ratio:.2f}")
            if test_ratio > 0:
                report.append(f"- **Test**: ARM64/x86_64 ratio = {test_ratio:.2f}")
            
            report.append("")
        
        # Insights
        report.append("## Key Insights")
        report.append("")
        
        avg_ratio = sum(r.get('total_time', 0) for r in ratios.values()) / len(ratios) if ratios else 0
        
        if avg_ratio > 1.1:
            report.append("- ARM64 runners show consistently slower performance across projects")
        elif avg_ratio < 0.9:
            report.append("- ARM64 runners demonstrate superior performance across projects")
        else:
            report.append("- ARM64 and x86_64 runners show comparable performance")
        
        report.append("- Performance differences may be attributed to:")
        report.append("  - Architecture-specific optimizations")
        report.append("  - Compiler toolchain differences")
        report.append("  - Memory hierarchy variations")
        report.append("  - Runner hardware specifications")
        
        return '\n'.join(report)
    
    def save_results(self, results: Dict, output_file: str):
        """Save results to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Analyze GitHub Actions benchmark results')
    parser.add_argument('--log', required=True, help='Path to workflow log file')
    parser.add_argument('--output', default='results/benchmark-analysis.md', help='Output report file')
    parser.add_argument('--json', default='results/benchmark-results.json', help='JSON results file')
    
    args = parser.parse_args()
    
    analyzer = BenchmarkAnalyzer()
    
    try:
        # Parse results
        results = analyzer.parse_workflow_log(args.log)
        
        # Calculate ratios
        ratios = analyzer.calculate_ratios(results)
        
        # Generate report
        report = analyzer.generate_report(results, ratios)
        
        # Save files
        with open(args.output, 'w') as f:
            f.write(report)
        
        analyzer.save_results({'results': results, 'ratios': ratios}, args.json)
        
        print(f"Analysis complete!")
        print(f"Report saved to: {args.output}")
        print(f"JSON data saved to: {args.json}")
        
    except FileNotFoundError:
        print(f"Error: Log file '{args.log}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing results: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()