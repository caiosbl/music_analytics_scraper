import openpyxl
import os

class WorkbookService:

    @staticmethod
    def create_workbook():
        return openpyxl.Workbook()

    @staticmethod
    def save_workbook_to_file(workbook, filename, folder="reports"):
        file_path = f"{folder}/{filename}.xlsx"
        os.makedirs("reports", exist_ok=True)
        workbook.save(file_path)
