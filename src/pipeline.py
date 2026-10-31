from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "automobileEDA_dirty_training.csv"
)
PROCESSED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "automobileEDA_processed.csv"
)

def load_data(file_path):
    """Membaca dataset tanpa mengubah file sumber."""
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {file_path}"
        )

    return pd.read_csv(file_path)


def inspect_data(df):
    """Menampilkan kondisi awal dataset di terminal."""

    print("\n=== 1. LIMA BARIS PERTAMA ===")
    print(df.head().to_string(index=False))

    print("\n=== 2. UKURAN DATASET ===")
    print(f"Jumlah baris : {df.shape[0]}")
    print(f"Jumlah kolom : {df.shape[1]}")

    print("\n=== 3. NAMA KOLOM ===")
    for number, column in enumerate(df.columns, start=1):
        print(f"{number}. {column!r}")

    print("\n=== 4. TIPE DATA SETIAP KOLOM ===")
    print(df.dtypes.to_string())

    print("\n=== 5. MISSING VALUES SETIAP KOLOM ===")
    print(df.isna().sum().to_string())

    print("\n=== 6. DUPLICATE RECORDS ===")
    duplicate_count = int(df.duplicated().sum())
    print(f"Jumlah baris duplikat tambahan: {duplicate_count}")

    print("\n=== 7. NILAI UNIK PADA KOLOM TEKS/KATEGORIKAL ===")
    text_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    for column in text_columns:
        print(f"\nKolom: {column}")
        print(f"Jumlah nilai unik: {df[column].nunique(dropna=False)}")

        # repr() membuat spasi di awal/akhir teks lebih terlihat.
        unique_values = [
            repr(value) for value in df[column].unique()
        ]
        print("Nilai unik:", ", ".join(unique_values))

def clean_data(df):
    """Membersihkan data berdasarkan temuan pemeriksaan awal."""
    cleaned = df.copy()

    rows_before = len(cleaned)
    missing_before = cleaned.isna().sum()

    # 1. Menghapus spasi di awal dan akhir nilai teks.
    text_columns = cleaned.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned[column] = cleaned[column].str.strip()

    # 2. Menyeragamkan kapitalisasi pada kolom yang bermasalah.
    category_columns = [
        "make",
        "body-style",
        "drive-wheels",
        "fuel-system",
    ]

    for column in category_columns:
        cleaned[column] = cleaned[column].str.lower()

    # 3. Mengonversi tanggal menggunakan empat format yang ditemukan.
    date_text = cleaned["transaction_date"]

    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%d-%b-%Y",
    ]

    parsed_dates = pd.Series(
        pd.NaT,
        index=cleaned.index,
        dtype="datetime64[ns]",
    )

    for date_format in date_formats:
        remaining = date_text.notna() & parsed_dates.isna()

        parsed_dates.loc[remaining] = pd.to_datetime(
            date_text.loc[remaining],
            format=date_format,
            errors="coerce",
        )

    invalid_dates = date_text.notna() & parsed_dates.isna()

    if invalid_dates.any():
        invalid_values = date_text.loc[invalid_dates].unique()
        raise ValueError(
            f"Format tanggal belum dikenali: {invalid_values}"
        )

    cleaned["transaction_date"] = parsed_dates

    changed_columns = [
        column
        for column in df.columns
        if not df[column].equals(cleaned[column])
    ]

    # 4. Menghapus duplikat setelah penulisan diseragamkan.
    duplicates_removed = int(cleaned.duplicated().sum())
    cleaned = cleaned.drop_duplicates().copy()

    # 5. Menghapus baris yang masih memiliki missing values.
    missing_columns = cleaned.columns[
        cleaned.isna().any()
    ].tolist()

    rows_before_dropna = len(cleaned)
    cleaned = cleaned.dropna().copy()
    rows_removed_missing = rows_before_dropna - len(cleaned)

    missing_after = cleaned.isna().sum()

    # 6. Menampilkan hasil cleaning.
    print("\n=== HASIL DATA CLEANING ===")
    print(f"Jumlah baris sebelum cleaning: {rows_before}")
    print(f"Jumlah baris sesudah cleaning: {len(cleaned)}")
    print(f"Baris duplikat yang dihapus: {duplicates_removed}")
    print(
        "Baris yang dihapus karena missing values: "
        f"{rows_removed_missing}"
    )

    print("\n=== MISSING VALUES SEBELUM DAN SESUDAH ===")
    missing_summary = pd.DataFrame({
        "sebelum": missing_before,
        "sesudah": missing_after,
    })
    print(missing_summary.to_string())

    print("\n=== KOLOM YANG NILAI ATAU TIPE DATANYA BERUBAH ===")
    for column in changed_columns:
        print(f"- {column}")

    print("\n=== KOLOM DENGAN MISSING VALUES PENYEBAB PENGHAPUSAN BARIS ===")
    for column in missing_columns:
        print(f"- {column}")

    return cleaned

def transform_data(df):
    """Normalisasi satu kolom numerik dan encoding satu kolom kategorikal."""
    transformed = df.copy()

    # 1. Min-Max Scaling pada horsepower.
    horsepower_min = transformed["horsepower"].min()
    horsepower_max = transformed["horsepower"].max()

    if horsepower_max == horsepower_min:
        transformed["horsepower_normalized"] = 0.0
    else:
        transformed["horsepower_normalized"] = (
            (transformed["horsepower"] - horsepower_min)
            / (horsepower_max - horsepower_min)
        )

    # 2. Encoding pada aspiration.
    aspiration_mapping = {
        "std": 0,
        "turbo": 1,
    }

    transformed["aspiration_encoded"] = (
        transformed["aspiration"].map(aspiration_mapping)
    )

    # 3. Menampilkan hasil transformasi.
    print("\n=== HASIL DATA TRANSFORMATION ===")
    print(f"Nilai minimum horsepower: {horsepower_min}")
    print(f"Nilai maksimum horsepower: {horsepower_max}")
    print("Encoding aspiration: std = 0, turbo = 1")

    print("\n=== PERBANDINGAN NORMALISASI HORSEPOWER ===")
    print(
        transformed[
            ["horsepower", "horsepower_normalized"]
        ].head().to_string(index=False)
    )

    print("\n=== PERBANDINGAN ENCODING ASPIRATION ===")
    print(
        transformed[
            ["aspiration", "aspiration_encoded"]
        ].drop_duplicates().to_string(index=False)
    )

    print("\n=== UKURAN DATASET SETELAH TRANSFORMASI ===")
    print(f"Jumlah baris: {transformed.shape[0]}")
    print(f"Jumlah kolom: {transformed.shape[1]}")

    return transformed

def save_data(df, file_path):
    """Menyimpan hasil pengolahan sebagai file CSV baru."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        file_path,
        index=False,
        date_format="%Y-%m-%d",
    )

    print("\n=== HASIL PENYIMPANAN ===")
    print(f"Dataset hasil disimpan di: {file_path}")
    print(f"Jumlah baris: {df.shape[0]}")
    print(f"Jumlah kolom: {df.shape[1]}")

def main():
    df = load_data(RAW_FILE)
    
    inspect_data(df)
    cleaned_df = clean_data(df)
    transformed_df = transform_data(cleaned_df)

    save_data(transformed_df, PROCESSED_FILE)


if __name__ == "__main__":
    main()