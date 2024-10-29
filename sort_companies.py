import re
import sys
import pathlib


def sort_table_in_readme(file_path: pathlib.Path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    table_start, table_end = None, None
    for i, line in enumerate(lines):
        if line.strip().startswith("| Company Name"):
            table_start = i
        if table_start is not None and (
            line.strip() == "" or not line.strip().startswith("|")
        ):
            table_end = i
            break

    if table_start is None or table_end is None:
        print("Table not found or incomplete in the README.md file.")
        sys.exit(1)

    table_header = lines[table_start].strip()
    table_separator = lines[table_start + 1].strip()
    table_rows = []
    current_row = ""
    for line in lines[table_start + 2 : table_end]:
        if line.strip().startswith("|"):
            if current_row:
                table_rows.append(current_row)
            current_row = line
        else:
            current_row += line
    if current_row:
        table_rows.append(current_row)

    sorted_rows = sorted(table_rows, key=lambda row: row.split("|")[1].strip().lower())

    columns = [col.strip() for col in table_header.split("|")[1:-1]]
    column_widths = [
        max(len(col), max(len(row.split("|")[i + 1].strip()) for row in sorted_rows))
        for i, col in enumerate(columns)
    ]

    def format_row(row, widths):
        cells = [cell.strip() for cell in row.split("|")[1:-1]]
        padded_cells = [f" {cell.ljust(width)} " for cell, width in zip(cells, widths)]
        return "|".join([""] + padded_cells + [""])

    padded_header = format_row(table_header, column_widths)
    padded_separator = format_row(
        table_separator.replace("-", ""), column_widths
    ).replace(" ", "-")
    padded_rows = [format_row(row, column_widths) for row in sorted_rows]

    final_lines = (
        lines[:table_start]
        + [padded_header + "\n", padded_separator + "\n"]
        + [row + "\n" for row in padded_rows]
        + lines[table_end:]
    )

    with open(file_path, "w") as file:
        file.writelines(final_lines)


if __name__ == "__main__":
    sort_table_in_readme(pathlib.Path("README.md"))
