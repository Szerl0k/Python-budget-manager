from utils.serialization_handler import SerializationHandler


def generate_report(transactions: list, report_name: str):

    serialization_handler = SerializationHandler("reports/"+report_name)
    serialization_handler.serialize(transactions, flag="report")