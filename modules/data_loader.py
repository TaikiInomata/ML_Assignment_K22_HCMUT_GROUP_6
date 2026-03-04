"""
Module: Data Loader

Module này cung cấp các hàm để tải dữ liệu từ URL công khai
và đọc vào Pandas DataFrame.

Chức năng chính:
- Tải dữ liệu từ URL không cần Google Drive mount
- Đọc file thành DataFrame
- Trích xuất metadata cơ bản
"""

import os
import requests
import pandas as pd
from typing import Tuple, Dict, Any


def load_data_from_url(url: str, output_path: str, timeout: int = 30) -> str:
    """
    Tải dữ liệu từ URL công khai xuống local storage.
    
    Args:
        url: URL công khai của dataset cần tải
        output_path: Đường dẫn local để lưu file
        timeout: Thời gian timeout cho request (mặc định: 30 giây)
    
    Returns:
        Đường dẫn đến file đã tải
    
    Raises:
        ValueError: Nếu URL không hợp lệ hoặc không thể truy cập
        requests.exceptions.RequestException: Nếu download thất bại
    
    TODO: Implement logic tải file từ URL
    - Validate URL
    - Tạo thư mục nếu chưa tồn tại
    - Download file với progress tracking
    - Xử lý lỗi và retry logic
    """
    # TODO: Implement download logic
    print(f"[Data Loader] TODO: Tải dữ liệu từ {url}")
    pass


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
    
    TODO: Implement logic đọc file
    - Kiểm tra file tồn tại
    - Xác định loại file (CSV, Excel, JSON, etc.)
    - Đọc vào DataFrame
    - Trích xuất metadata (shape, dtypes, missing values)
    """
    # TODO: Implement file reading logic
    print(f"[Data Loader] TODO: Đọc file từ {file_path}")
    pass


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
    
    TODO: Implement pipeline
    - Gọi load_data_from_url để tải file
    - Gọi create_dataframe để đọc vào DataFrame
    - Trả về kết quả
    """
    # TODO: Implement pipeline
    print("[Data Loader] TODO: Thực hiện pipeline tải và đọc dữ liệu")
    pass


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm validate URL
# - Hàm xử lý các định dạng file đặc biệt
# - Hàm caching để tránh download lại
