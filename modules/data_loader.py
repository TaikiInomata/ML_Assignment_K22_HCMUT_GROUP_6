"""
Module: Data Loader

Module này cung cấp các hàm để tải dữ liệu từ URL công khai
và đọc vào Pandas DataFrame.

Chức năng chính:
- Tải dữ liệu từ URL công khai (GitHub Raw, HTTP direct file)
- Hỗ trợ link dataset Kaggle thông qua Kaggle CLI
- Đọc file thành DataFrame
- Trích xuất metadata cơ bản

Lưu ý:
- Không dùng Google Drive mount.
- Với link Kaggle dạng trang dataset, cần cài Kaggle CLI và cấu hình API token.
"""

from __future__ import annotations

import json
import shutil
import shlex
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib.parse import urlparse

import pandas as pd
import requests


def _looks_like_kaggle_slug(value: str) -> bool:
    """Kiểm tra định dạng owner/dataset của Kaggle."""
    parts = [p for p in value.strip().split("/") if p]
    return len(parts) == 2 and all(parts)


def _is_http_url(value: str) -> bool:
    """Kiểm tra chuỗi có phải HTTP/HTTPS URL."""
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_kaggle_dataset_url(url: str) -> bool:
    """Kiểm tra URL có phải trang dataset Kaggle hay không."""
    parsed = urlparse(url)
    return "kaggle.com" in parsed.netloc and "/datasets/" in parsed.path


def _extract_kaggle_slug_from_command(command: str) -> str:
    """Hỗ trợ input kiểu: kaggle datasets download owner/dataset."""
    tokens = shlex.split(command)
    if len(tokens) < 4:
        raise ValueError(f"Câu lệnh Kaggle CLI không hợp lệ: {command}")
    if tokens[0] != "kaggle" or tokens[1] != "datasets" or tokens[2] != "download":
        raise ValueError(f"Câu lệnh Kaggle CLI không hợp lệ: {command}")
    slug = tokens[3]
    if not _looks_like_kaggle_slug(slug):
        raise ValueError(f"Dataset slug không hợp lệ trong command: {slug}")
    return slug


def _resolve_source(source: str) -> Dict[str, str]:
    """
    Chuẩn hóa input nguồn dữ liệu.

    Hỗ trợ các dạng:
    - HTTP/HTTPS direct URL
    - URL trang dataset Kaggle
    - Kaggle slug: owner/dataset
    - kaggle://owner/dataset
    - Câu lệnh: kaggle datasets download owner/dataset
    """
    value = source.strip()
    if not value:
        raise ValueError("Nguồn dữ liệu rỗng.")

    if value.startswith("kaggle datasets download "):
        return {"type": "kaggle", "slug": _extract_kaggle_slug_from_command(value)}

    if value.startswith("kaggle://"):
        slug = value.replace("kaggle://", "", 1)
        if not _looks_like_kaggle_slug(slug):
            raise ValueError(f"Kaggle source không hợp lệ: {value}")
        return {"type": "kaggle", "slug": slug}

    if _looks_like_kaggle_slug(value):
        return {"type": "kaggle", "slug": value}

    if _is_http_url(value):
        if _is_kaggle_dataset_url(value):
            return {"type": "kaggle", "slug": _extract_kaggle_slug(value)}
        return {"type": "direct", "url": value}

    raise ValueError(
        "Nguồn dữ liệu không hợp lệ. Hỗ trợ: direct URL, Kaggle URL, "
        "owner/dataset, kaggle://owner/dataset, hoặc 'kaggle datasets download owner/dataset'."
    )


def _extract_kaggle_slug(url: str) -> str:
    """Lấy slug author/dataset từ URL Kaggle dataset."""
    # Ví dụ: /datasets/jessemostipak/hotel-booking-demand
    parts = [p for p in urlparse(url).path.split("/") if p]
    try:
        idx = parts.index("datasets")
        owner = parts[idx + 1]
        dataset = parts[idx + 2]
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Không trích xuất được slug Kaggle từ URL: {url}") from exc
    return f"{owner}/{dataset}"


def _download_direct_file(url: str, destination: Path, timeout: int = 60) -> None:
    """Download file trực tiếp từ URL (GitHub Raw/HTTP direct)."""
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        content_type = (response.headers.get("Content-Type") or "").lower()

        # Tránh ghi nhầm HTML page (thường xảy ra khi URL không phải file trực tiếp).
        if "text/html" in content_type:
            raise ValueError(
                "URL trả về HTML thay vì file dữ liệu. "
                "Hãy dùng direct file link (ví dụ GitHub Raw) hoặc URL Kaggle dataset."
            )

        with destination.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def _download_from_kaggle_slug(slug: str, destination: Path, timeout: int = 300) -> None:
    """
    Download từ Kaggle dataset URL bằng Kaggle CLI.

    Yêu cầu:
    - Cài đặt `kaggle` CLI.
    - Có API token tại ~/.kaggle/kaggle.json hoặc env vars tương ứng.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        cmd = [
            "kaggle",
            "datasets",
            "download",
            "-d",
            slug,
            "-p",
            tmp_dir,
            "--force",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Không tìm thấy Kaggle CLI. Cài bằng: pip install kaggle"
            ) from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise RuntimeError(
                "Tải từ Kaggle thất bại. Hãy kiểm tra API token Kaggle. "
                f"Chi tiết: {stderr}"
            ) from exc

        # Kaggle thường trả về file zip.
        zip_files = list(Path(tmp_dir).glob("*.zip"))
        if not zip_files:
            # Trường hợp hiếm khi CLI đã lưu trực tiếp file.
            candidates = list(Path(tmp_dir).iterdir())
            if not candidates:
                raise RuntimeError(
                    "Không tìm thấy file nào sau khi tải Kaggle. "
                    f"CLI output: {(result.stdout or '').strip()}"
                )
            shutil.copy2(candidates[0], destination)
            return

        with zipfile.ZipFile(zip_files[0], "r") as zf:
            members = zf.namelist()
            if not members:
                raise RuntimeError("File zip từ Kaggle rỗng.")

            # Ưu tiên CSV nếu có.
            preferred = None
            for member in members:
                if member.lower().endswith(".csv"):
                    preferred = member
                    break

            selected = preferred or members[0]
            extracted_path = Path(tmp_dir) / selected
            zf.extract(selected, path=tmp_dir)
            extracted_path = Path(tmp_dir) / selected
            extracted_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(extracted_path, destination)


def load_data_from_url(
    url: str,
    output_path: str,
    timeout: int = 60,
    force_download: bool = False,
) -> str:
    """
    Tải dữ liệu từ nguồn public xuống local storage.
    
    Args:
        url: Nguồn dữ liệu. Hỗ trợ:
            - direct URL (GitHub Raw/HTTP)
            - Kaggle URL
            - Kaggle slug dạng owner/dataset
            - Câu lệnh dạng: kaggle datasets download owner/dataset
        output_path: Đường dẫn local để lưu file
        timeout: Thời gian timeout cho request (mặc định: 30 giây)
    
    Returns:
        Đường dẫn đến file đã tải
    
    Raises:
        ValueError: Nếu URL không hợp lệ hoặc không thể truy cập
        requests.exceptions.RequestException: Nếu download trực tiếp thất bại
        RuntimeError: Nếu tải Kaggle thất bại do thiếu CLI/token
    """
    resolved = _resolve_source(url)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() and not force_download:
        print(f"[Data Loader] Dùng file cache: {destination}")
        return str(destination)

    print(f"[Data Loader] Bắt đầu tải dữ liệu từ: {url}")
    if resolved["type"] == "kaggle":
        _download_from_kaggle_slug(resolved["slug"], destination, timeout=timeout)
    else:
        _download_direct_file(resolved["url"], destination, timeout=timeout)

    if not destination.exists() or destination.stat().st_size == 0:
        raise RuntimeError(f"Tải dữ liệu thất bại, file không hợp lệ: {destination}")

    print(f"[Data Loader] Đã tải xong: {destination}")
    return str(destination)


def create_dataframe(file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Đọc file dữ liệu thành Pandas DataFrame và trích xuất metadata.
    
    Args:
        file_path: Đường dẫn đến file dữ liệu (CSV, Excel, etc.)
        **kwargs: Các tham số bổ sung cho hàm đọc pandas
    
    Returns:
        Tuple chứa:
            - DataFrame: Dữ liệu đã load
            - Dict: Metadata bao gồm số dòng, cột, dtypes, missing values
    
    Raises:
        FileNotFoundError: Nếu file không tồn tại
        ValueError: Nếu định dạng file không được hỗ trợ
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path, **kwargs)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path, **kwargs)
    elif suffix == ".json":
        df = pd.read_json(path, **kwargs)
    elif suffix == ".parquet":
        df = pd.read_parquet(path, **kwargs)
    else:
        raise ValueError(
            f"Định dạng file không được hỗ trợ: {suffix}. "
            "Hỗ trợ: .csv, .xlsx, .xls, .json, .parquet"
        )

    metadata: Dict[str, Any] = {
        "file_path": str(path),
        "n_rows": int(df.shape[0]),
        "n_columns": int(df.shape[1]),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {col: int(v) for col, v in df.isnull().sum().items()},
        "total_missing": int(df.isnull().sum().sum()),
    }

    print(
        "[Data Loader] Đọc dữ liệu thành công - "
        f"shape: ({metadata['n_rows']}, {metadata['n_columns']})"
    )
    return df, metadata


def load_data_pipeline(url: str, output_path: str, **read_kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Pipeline hoàn chỉnh: download từ URL và load vào DataFrame.
    
    Hàm tiện ích kết hợp load_data_from_url và create_dataframe.
    
    Args:
        url: URL công khai của dataset
        output_path: Đường dẫn local để lưu file
        **read_kwargs: Các tham số bổ sung cho hàm đọc pandas
    
    Returns:
        Tuple chứa:
            - DataFrame: Dữ liệu đã load
            - Dict: Metadata
    
    """
    downloaded_path = load_data_from_url(
        url=url,
        output_path=output_path,
        timeout=read_kwargs.pop("download_timeout", 60),
        force_download=read_kwargs.pop("force_download", False),
    )
    df, metadata = create_dataframe(downloaded_path, **read_kwargs)
    return df, metadata


def load_data_from_source(
    source: str,
    output_path: str,
    timeout: int = 60,
    force_download: bool = False,
) -> str:
    """Alias rõ nghĩa cho load_data_from_url để dùng source linh hoạt."""
    return load_data_from_url(
        url=source,
        output_path=output_path,
        timeout=timeout,
        force_download=force_download,
    )


def load_hotel_bookings_dataset(
    output_path: str = "data/hotel_bookings.csv",
    url: str = "jessemostipak/hotel-booking-demand",
    force_download: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Hàm tiện ích cho dataset Hotel Booking Demand.

    Args:
        output_path: Nơi lưu file CSV sau khi tải
        url: URL Kaggle hoặc direct file URL (GitHub Raw)
        force_download: True để bỏ cache local và tải lại

    Returns:
        DataFrame và metadata
    """
    return load_data_pipeline(
        url=url,
        output_path=output_path,
        force_download=force_download,
    )


def _print_metadata_summary(metadata: Dict[str, Any], preview_missing_top_n: int = 10) -> None:
    """In metadata theo định dạng dễ đọc trên terminal."""
    print("\n" + "=" * 72)
    print("DATASET SUMMARY")
    print("=" * 72)
    print(f"File path      : {metadata['file_path']}")
    print(f"Rows           : {metadata['n_rows']}")
    print(f"Columns        : {metadata['n_columns']}")
    print(f"Total missing  : {metadata['total_missing']}")

    print("\nColumns:")
    print(", ".join(metadata["columns"]))

    print("\nDtypes:")
    print(json.dumps(metadata["dtypes"], indent=2, ensure_ascii=False))

    missing_items = sorted(
        metadata["missing_values"].items(),
        key=lambda item: item[1],
        reverse=True,
    )
    print(f"\nTop {preview_missing_top_n} missing-value columns:")
    for column, missing_count in missing_items[:preview_missing_top_n]:
        print(f"- {column}: {missing_count}")

    print("=" * 72)


if __name__ == "__main__":
    # Ví dụ chạy nhanh:
    # python -m modules.data_loader
    #
    # Lưu ý với Kaggle URL: cần cấu hình Kaggle API token trước khi chạy.
    try:
        df_, meta_ = load_hotel_bookings_dataset()
        print("\n" + "=" * 72)
        print("DATA PREVIEW")
        print("=" * 72)
        print(df_.head().to_string())
        _print_metadata_summary(meta_)
    except Exception as exc:
        print(f"[Data Loader] Lỗi: {exc}")
