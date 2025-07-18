#!/bin/bash
# Generate benchmark report from GitHub Actions workflow run

set -e

# Configuration
REPO="${GITHUB_REPOSITORY:-owner/github-actions-arch-benchmarks}"
WORKFLOW_FILE="benchmark.yml"
OUTPUT_DIR="results"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) not found. Please install it first."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install it first."
        exit 1
    fi
    
    print_status "Dependencies check passed"
}

# Function to get latest workflow run
get_latest_run() {
    print_status "Fetching latest workflow run..."
    
    local run_id=$(gh run list --workflow="$WORKFLOW_FILE" --limit=1 --json databaseId --jq '.[0].databaseId')
    
    if [ -z "$run_id" ]; then
        print_error "No workflow runs found"
        exit 1
    fi
    
    echo "$run_id"
}

# Function to download workflow logs
download_logs() {
    local run_id=$1
    local log_file="$OUTPUT_DIR/workflow-run-$run_id.log"
    
    print_status "Downloading workflow logs..."
    
    mkdir -p "$OUTPUT_DIR"
    
    if gh run view "$run_id" --log > "$log_file" 2>/dev/null; then
        print_status "Logs downloaded to: $log_file"
        echo "$log_file"
    else
        print_error "Failed to download workflow logs"
        exit 1
    fi
}

# Function to analyze results
analyze_results() {
    local log_file=$1
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local report_file="$OUTPUT_DIR/benchmark-report-$timestamp.md"
    local json_file="$OUTPUT_DIR/benchmark-results-$timestamp.json"
    
    print_status "Analyzing benchmark results..."
    
    if python3 scripts/analyze-results.py --log "$log_file" --output "$report_file" --json "$json_file"; then
        print_status "Analysis complete!"
        echo ""
        echo "Generated files:"
        echo "  Report: $report_file"
        echo "  Data:   $json_file"
        echo ""
        
        # Show summary
        if [ -f "$report_file" ]; then
            print_status "Report Preview:"
            echo "----------------------------------------"
            head -n 20 "$report_file"
            echo "----------------------------------------"
            echo "(See full report in $report_file)"
        fi
    else
        print_error "Analysis failed"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --run-id ID     Use specific workflow run ID"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Analyze latest workflow run"
    echo "  $0 --run-id 1234567   # Analyze specific run"
}

# Main execution
main() {
    local run_id=""
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --run-id)
                run_id="$2"
                shift 2
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Check dependencies
    check_dependencies
    
    # Get run ID if not provided
    if [ -z "$run_id" ]; then
        run_id=$(get_latest_run)
    fi
    
    print_status "Processing workflow run: $run_id"
    
    # Download logs
    log_file=$(download_logs "$run_id")
    
    # Analyze results
    analyze_results "$log_file"
    
    print_status "Report generation complete!"
}

# Run main function
main "$@"