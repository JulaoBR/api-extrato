from datetime import datetime, timedelta, timezone

def formatar_data(data, formato="%d/%m/%Y"):
    return data.strftime(formato)