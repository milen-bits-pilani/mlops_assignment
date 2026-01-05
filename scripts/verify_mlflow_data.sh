#!/bin/bash
# Verify MLflow data exists and show summary

echo "=========================================="
echo "MLflow Data Verification"
echo "=========================================="
echo ""

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$PROJECT_ROOT"

# Check if mlruns exists
if [ ! -d "mlruns" ]; then
    echo "❌ Error: mlruns directory not found!"
    echo "   Please run training first: python src/models/train.py"
    exit 1
fi

echo "✅ mlruns directory found"
echo ""

# List experiments
echo "Experiments:"
for exp_dir in mlruns/*/; do
    if [ -f "${exp_dir}meta.yaml" ]; then
        exp_name=$(grep "^name:" "${exp_dir}meta.yaml" | cut -d' ' -f2)
        exp_id=$(basename "$exp_dir")
        run_count=$(find "${exp_dir}" -maxdepth 1 -type d -name "[0-9a-f]*" | wc -l)
        echo "  - $exp_name (ID: $exp_id) - $run_count runs"
    fi
done

echo ""
echo "Runs in 'heart_disease' experiment:"
if [ -d "mlruns/547036990868872200" ]; then
    for run_dir in mlruns/547036990868872200/*/; do
        if [ -f "${run_dir}meta.yaml" ]; then
            run_name=$(grep "^run_name:" "${run_dir}meta.yaml" | cut -d' ' -f2)
            run_id=$(basename "$run_dir")
            if [ -n "$run_name" ]; then
                echo "  - $run_name ($run_id)"
            fi
        fi
    done
fi

echo ""
echo "=========================================="
echo "To view in MLflow UI:"
echo "  cd $PROJECT_ROOT"
echo "  ./scripts/start_mlflow_ui.sh"
echo "  Then open: http://localhost:5000"
echo "=========================================="
