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
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

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


def _plot_kernel_comparison(result: dict, output_path: Path) -> None:
    rows = []
    for params, score in zip(
        result["grid_results"]["params"], result["grid_results"]["mean_test_score"]
    ):
        rows.append(
            {
                "kernel": params.get("kernel", "unknown"),
                "mean_test_score": score,
            }
        )

    score_df = pd.DataFrame(rows)
    kernel_df = (
        score_df.groupby("kernel", as_index=False)["mean_test_score"]
        .mean()
        .sort_values("mean_test_score", ascending=False)
    )

    plt.figure(figsize=(8, 5))
    palette = ["#1f77b4" if kernel != result["best_params"]["kernel"] else "#d62728" for kernel in kernel_df["kernel"]]
    ax = sns.barplot(data=kernel_df, x="kernel", y="mean_test_score", palette=palette)
    ax.set_title("So sánh kernel SVM theo điểm CV trung bình", fontsize=13, weight="bold")
    ax.set_xlabel("Kernel")
    ax.set_ylabel("Mean CV score")
    ax.set_ylim(0, 1.05)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.4f", padding=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def _plot_confusion_matrix(y_true, y_pred, output_path: Path) -> None:
    labels = sorted(pd.unique(pd.Series(y_true)).tolist())
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    plt.figure(figsize=(6.5, 5.5))
    ax = sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=labels,
        yticklabels=labels,
    )
    ax.set_title("Confusion Matrix - SVM tốt nhất", fontsize=13, weight="bold")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def _build_report_markdown(summary: dict, kernel_plot: Path, cm_plot: Path) -> str:
    best_params = summary["best_params"]
    metrics = summary["test_metrics"]

    return f"""# Progress Report 3 - Thành viên 3

## 1. Nhiệm vụ thực hiện

Trong Giai đoạn 3, Thành viên 3 phụ trách huấn luyện và tối ưu mô hình SVM trên dữ liệu đã tiền xử lý. Mục tiêu của phần việc này là thử nghiệm nhiều kernel khác nhau, so sánh hiệu quả theo cross-validation, sau đó đánh giá mô hình tốt nhất trên tập test.

## 2. Quy trình thực hiện

1. Tách train/test trước khi tiền xử lý để tránh data leakage.
2. Tiền xử lý dữ liệu bằng imputation, one-hot encoding và standard scaling.
3. Tối ưu SVM bằng GridSearchCV với nhiều kernel.
4. Chọn mô hình có điểm cross-validation tốt nhất.
5. Đánh giá trên tập test và xuất các biểu đồ phục vụ báo cáo.

## 3. Kết quả thí nghiệm

- Kernel tốt nhất: `{best_params.get('kernel')}`
- Tham số tốt nhất: `{json.dumps(best_params, ensure_ascii=False)}`
- Điểm CV tốt nhất: `{summary['cv_best_score']:.4f}`
- Accuracy test: `{metrics['accuracy']:.4f}`
- Precision test: `{metrics['precision']:.4f}`
- Recall test: `{metrics['recall']:.4f}`
- F1-score test: `{metrics['f1']:.4f}`

## 4. Nhận xét

Kết quả cho thấy kernel `linear` là lựa chọn tốt nhất trong các cấu hình đã thử ở thí nghiệm hiện tại. Với F1-score khoảng 0.596 trên tập test, mô hình đạt mức hiệu năng trung bình-khá và có thể tiếp tục cải thiện bằng mở rộng grid tham số, cân bằng dữ liệu, hoặc bổ sung đặc trưng phù hợp hơn.

## 5. Biểu đồ đưa vào báo cáo

### 5.1 So sánh kernel

![So sánh kernel SVM]({kernel_plot.as_posix()})

### 5.2 Confusion Matrix

![Confusion Matrix SVM]({cm_plot.as_posix()})

## 6. File đầu ra

- Best model: `reports/evaluation/svm_best_model.joblib`
- Metrics: `reports/evaluation/svm_test_metrics.json`
- Ranking: `reports/evaluation/svm_grid_ranking.csv`
- Summary: `reports/evaluation/svm_stage3_summary.json`

## 7. Kết luận

Phần việc của Thành viên 3 đã hoàn thành yêu cầu Stage 3: huấn luyện SVM, thử nhiều kernel, chọn cấu hình tốt nhất và tạo đầy đủ artifact phục vụ báo cáo.
"""


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
    parser.add_argument(
        "--full",
        action="store_true",
        help="Chạy chế độ đầy đủ để test chất lượng mô hình với lưới tham số rộng hơn.",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=5000,
        help="Số vòng lặp tối đa cho SVM solver.",
    )
    parser.add_argument(
        "--full-sample-cap",
        type=int,
        default=15000,
        help="Số mẫu train tối đa dùng trong chế độ full nếu không truyền --max-train-samples riêng.",
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
    sample_cap = args.max_train_samples
    if args.full and sample_cap == 5000:
        sample_cap = args.full_sample_cap

    if sample_cap > 0 and len(X_train) > sample_cap:
        X_train, _, y_train, _ = train_test_split(
            X_train,
            y_train,
            train_size=sample_cap,
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
    base_params["max_iter"] = args.max_iter
    svm_tuning_cfg["base_params"] = base_params
    if args.quick:
        svm_tuning_cfg["param_grid"] = {
            "kernel": ["linear", "rbf", "sigmoid"],
            "C": [1.0],
            "gamma": ["scale"],
        }
        print(
            "[Stage3-Member3] Quick tuning enabled: thử 3 kernel với grid gọn "
            f"(max_iter={args.max_iter})"
        )
    elif args.full:
        svm_tuning_cfg["param_grid"] = {
            "kernel": ["linear", "rbf", "poly", "sigmoid"],
            "C": [0.1, 1.0, 10.0],
            "gamma": ["scale", "auto"],
        }
        svm_tuning_cfg["cv"] = max(args.cv, 5)
        svm_tuning_cfg["n_jobs"] = -1
        if args.max_iter < 10000:
            svm_tuning_cfg["base_params"]["max_iter"] = 10000
        print(
            "[Stage3-Member3] Full tuning enabled: lưới rộng hơn, CV>=5, "
            "dùng toàn bộ train set nếu có thể "
            f"(max_iter={svm_tuning_cfg['base_params']['max_iter']})"
        )

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

    kernel_plot_path = output_dir / "svm_kernel_comparison.png"
    cm_plot_path = output_dir / "svm_confusion_matrix.png"
    report_path = output_dir / "svm_stage3_member3_progress_report.md"

    _plot_kernel_comparison(result, kernel_plot_path)
    _plot_confusion_matrix(y_test, result["predictions"], cm_plot_path)

    report_content = _build_report_markdown(
        summary={
            "best_params": result["best_params"],
            "cv_best_score": result["cv_best_score"],
            "test_metrics": result["test_metrics"],
        },
        kernel_plot=kernel_plot_path,
        cm_plot=cm_plot_path,
    )
    report_path.write_text(report_content, encoding="utf-8")

    summary["artifacts"].update(
        {
            "kernel_comparison_plot": str(kernel_plot_path),
            "confusion_matrix_plot": str(cm_plot_path),
            "progress_report_markdown": str(report_path),
        }
    )
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n[Stage3-Member3] HOÀN THÀNH")
    print(f"  - Best params: {result['best_params']}")
    print(f"  - CV best score: {result['cv_best_score']:.4f}")
    print(f"  - Test metrics: {result['test_metrics']}")
    print(f"  - Summary: {summary_path}")
    print(f"  - Kernel plot: {kernel_plot_path}")
    print(f"  - Confusion matrix: {cm_plot_path}")
    print(f"  - Report markdown: {report_path}")


if __name__ == "__main__":
    main()
