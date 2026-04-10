"""
Stage 3 - Member 3: SVM training and kernel optimization.

Chạy file này để hoàn thành phần việc Stage 3 của Thành viên 3:
- Preprocess dữ liệu với train/test split (không data leakage)
- Tối ưu SVM qua nhiều kernel bằng GridSearchCV
- Lưu artifacts: best model, metrics, best params, ranking kết quả
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import argparse

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

# Ensure project root is importable when running the script directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import CONFIG
from modules.data_loader import create_dataframe, load_data_from_config
from modules.models import optimize_svm_with_kernel_search
from modules.preprocessing import preprocess_with_train_test_split


def ensure_output_dirs() -> Path:
    output_dir = Path("reports/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def load_dataset_from_config() -> pd.DataFrame:
    data_path = Path(CONFIG["data"]["file_path"])

    if data_path.exists():
        df, _ = create_dataframe(str(data_path))
        return df

    # Fallback: tải theo config nếu file local chưa có
    df, _ = load_data_from_config()
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Stage 3 Member 3 SVM workflow")
    parser.add_argument(
        "--max-train-samples",
        type=int,
        default=5000,
        help="Giới hạn số samples train để tăng tốc GridSearchCV (0 = dùng toàn bộ).",
    )
    parser.add_argument(
        "--cv",
        type=int,
        default=2,
        help="Số folds cho GridSearchCV.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Dùng lưới tham số gọn để chạy nhanh.",
    )
    args = parser.parse_args()

    output_dir = ensure_output_dirs()

    print("[Stage3-Member3] Load dataset...")
    df = load_dataset_from_config()

    print("[Stage3-Member3] Preprocess với train/test split...")
    X_train, X_test, y_train, y_test, _ = preprocess_with_train_test_split(
        df=df,
        target_column=CONFIG["data"]["target_column"],
        config=CONFIG["preprocessing"],
        test_size=CONFIG["models"]["train_test_split"]["test_size"],
        random_state=CONFIG["models"]["train_test_split"]["random_state"],
    )

    # Tăng tốc tune nếu train set quá lớn.
    if args.max_train_samples > 0 and len(X_train) > args.max_train_samples:
        X_train, _, y_train, _ = train_test_split(
            X_train,
            y_train,
            train_size=args.max_train_samples,
            stratify=y_train,
            random_state=42,
        )
        print(
            "[Stage3-Member3] Downsample train set cho GridSearchCV: "
            f"{X_train.shape[0]} samples"
        )

    print("[Stage3-Member3] Tối ưu SVM qua nhiều kernel...")
    svm_tuning_cfg = CONFIG["models"]["svm"].get("tuning", {})
    if not svm_tuning_cfg.get("enabled", True):
        raise ValueError("SVM tuning đang tắt trong config.py. Hãy bật models.svm.tuning.enabled = True")

    svm_tuning_cfg = dict(svm_tuning_cfg)
    svm_tuning_cfg["cv"] = args.cv
    base_params = dict(svm_tuning_cfg.get("base_params", {}))
    base_params.setdefault("max_iter", 2000)
    svm_tuning_cfg["base_params"] = base_params
    if args.quick:
        svm_tuning_cfg["param_grid"] = {
            "kernel": ["linear", "rbf", "sigmoid"],
            "C": [1.0],
            "gamma": ["scale"],
        }
        print("[Stage3-Member3] Quick tuning enabled: thử 3 kernel với grid gọn")

    result = optimize_svm_with_kernel_search(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        params=svm_tuning_cfg,
    )

    print("[Stage3-Member3] Lưu artifacts...")
    model_path = output_dir / "svm_best_model.joblib"
    metrics_path = output_dir / "svm_test_metrics.json"
    summary_path = output_dir / "svm_stage3_summary.json"
    ranking_path = output_dir / "svm_grid_ranking.csv"

    joblib.dump(result["best_model"], model_path)

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(result["test_metrics"], f, indent=2, ensure_ascii=False)

    summary = {
        "best_params": result["best_params"],
        "cv_best_score": result["cv_best_score"],
        "test_metrics": result["test_metrics"],
        "artifacts": {
            "best_model": str(model_path),
            "metrics": str(metrics_path),
            "ranking": str(ranking_path),
        },
    }
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    ranking_df = pd.DataFrame(
        {
            "params": result["grid_results"]["params"],
            "mean_test_score": result["grid_results"]["mean_test_score"],
            "rank_test_score": result["grid_results"]["rank_test_score"],
        }
    ).sort_values("rank_test_score", ascending=True)
    ranking_df.to_csv(ranking_path, index=False)

    print("\n[Stage3-Member3] HOÀN THÀNH")
    print(f"  - Best params: {result['best_params']}")
    print(f"  - CV best score: {result['cv_best_score']:.4f}")
    print(f"  - Test metrics: {result['test_metrics']}")
    print(f"  - Summary: {summary_path}")


if __name__ == "__main__":
    main()
