#!/bin/bash
# Master pipeline script for automated data ingestion
# Usage: ./run_pipeline.sh [command] [options]
#
# Commands:
#   run         - Run the full pipeline
#   dry-run     - Show what would be done without making changes
#   validate    - Validate data only
#   status      - Show scheduler status
#   health      - Check pipeline health
#   schedule    - Run scheduled tasks (called by cron/systemd)
#   enable      - Enable automatic scheduling
#   disable     - Disable automatic scheduling
#   help        - Show this help message

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PIPELINE_DIR="$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check if required packages are installed
    if ! python3 -c "import requests" 2>/dev/null; then
        log_warning "requests package not found. Installing..."
        pip3 install requests --quiet
    fi
}

# Check if API is running
check_api() {
    local api_url="${API_URL:-http://localhost:8000}"
    
    log_info "Checking API at $api_url..."
    
    if curl -s -o /dev/null -w "%{http_code}" "$api_url/health" | grep -q "200"; then
        log_success "API is running"
        return 0
    else
        log_warning "API is not running at $api_url"
        log_info "Start the API with: ./start-api.sh"
        return 1
    fi
}

# Run validation
run_validation() {
    log_info "Running data validation..."
    
    cd "$PROJECT_DIR"
    
    # Validate lab data
    if python3 "$PIPELINE_DIR/validate_data.py" --type lab "$PROJECT_DIR/data/raw/lab_announcements.json"; then
        log_success "Lab data validation passed"
    else
        log_error "Lab data validation failed"
        return 1
    fi
    
    # Validate benchmark data
    if python3 "$PIPELINE_DIR/validate_data.py" --type benchmark "$PROJECT_DIR/data/processed/benchmark_scores.json"; then
        log_success "Benchmark data validation passed"
    else
        log_error "Benchmark data validation failed"
        return 1
    fi
    
    return 0
}

# Run ingestion
run_ingestion() {
    local dry_run="$1"
    local api_url="${API_URL:-http://localhost:8000}"
    
    log_info "Running data ingestion..."
    
    if [ "$dry_run" = "true" ]; then
        log_info "DRY RUN MODE - No changes will be made"
    fi
    
    cd "$PROJECT_DIR"
    
    local dry_flag=""
    if [ "$dry_run" = "true" ]; then
        dry_flag="--dry-run"
    fi
    
    # Ingest lab data
    log_info "Ingesting lab announcement data..."
    if python3 "$PIPELINE_DIR/ingest_lab_data.py" --api-url "$api_url" $dry_flag; then
        if [ "$dry_run" = "true" ]; then
            log_success "Lab data dry-run completed"
        else
            log_success "Lab data ingestion completed"
        fi
    else
        log_error "Lab data ingestion failed"
        return 1
    fi
    
    # Ingest benchmark data
    log_info "Ingesting benchmark scores..."
    if python3 "$PIPELINE_DIR/ingest_benchmarks.py" --api-url "$api_url" $dry_flag; then
        if [ "$dry_run" = "true" ]; then
            log_success "Benchmark data dry-run completed"
        else
            log_success "Benchmark data ingestion completed"
        fi
    else
        log_error "Benchmark data ingestion failed"
        return 1
    fi
    
    return 0
}

# Show help
show_help() {
    cat << EOF
Data Pipeline for AI Model Research Team
========================================

Automated ingestion pipeline for model and benchmark data.

USAGE:
    ./run_pipeline.sh [COMMAND] [OPTIONS]

COMMANDS:
    run         Run the full pipeline (validate + ingest)
    dry-run     Show what would be done without making changes
    validate    Validate data only
    status      Show scheduler status
    health      Check pipeline health
    schedule    Run scheduled tasks (called by cron/systemd)
    enable      Enable automatic scheduling
    disable     Disable automatic scheduling
    help        Show this help message

ENVIRONMENT VARIABLES:
    API_URL     Base URL of the API (default: http://localhost:8000)

EXAMPLES:
    ./run_pipeline.sh run           # Run full pipeline
    ./run_pipeline.sh dry-run       # Preview changes
    ./run_pipeline.sh validate      # Validate data only
    ./run_pipeline.sh status        # Check status

FILES:
    Data files:
      - data/raw/lab_announcements.json
      - data/processed/benchmark_scores.json
    
    Pipeline scripts:
      - scripts/pipeline/validate_data.py
      - scripts/pipeline/ingest_lab_data.py
      - scripts/pipeline/ingest_benchmarks.py
      - scripts/pipeline/scheduler.py

For more information, see docs/pipeline/README.md
EOF
}

# Main function
main() {
    local command="${1:-help}"
    
    # Setup Python environment
    check_python
    
    case "$command" in
        run)
            log_info "Starting data pipeline..."
            
            # Check API
            if ! check_api; then
                log_error "API must be running before ingestion"
                exit 1
            fi
            
            # Run validation
            if ! run_validation; then
                log_error "Validation failed. Pipeline aborted."
                exit 1
            fi
            
            # Run ingestion
            if run_ingestion "false"; then
                log_success "Pipeline completed successfully!"
            else
                log_error "Pipeline failed during ingestion"
                exit 1
            fi
            ;;
        
        dry-run)
            log_info "Starting pipeline dry-run..."
            
            # Run validation (always dry)
            if ! run_validation; then
                log_warning "Validation found issues"
            fi
            
            # Run ingestion in dry-run mode
            if run_ingestion "true"; then
                log_success "Dry-run completed"
            else
                log_error "Dry-run encountered errors"
                exit 1
            fi
            ;;
        
        validate)
            run_validation
            ;;
        
        status)
            python3 "$PIPELINE_DIR/scheduler.py" status
            ;;
        
        health)
            python3 "$PIPELINE_DIR/scheduler.py" health
            ;;
        
        schedule)
            # Called by cron/systemd for scheduled runs
            log_info "Running scheduled pipeline..."
            
            if check_api && run_validation && run_ingestion "false"; then
                log_success "Scheduled pipeline completed"
            else
                log_error "Scheduled pipeline failed"
                exit 1
            fi
            ;;
        
        enable)
            python3 "$PIPELINE_DIR/scheduler.py" enable
            ;;
        
        disable)
            python3 "$PIPELINE_DIR/scheduler.py" disable
            ;;
        
        help|--help|-h)
            show_help
            ;;
        
        *)
            log_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
