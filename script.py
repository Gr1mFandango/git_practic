import sys
from typing import List, Set


class LogMobileDistinguisher:
    def __init__(self, desktop_file_name: str, mobile_file_name: str):
        self.desktop = self.read_file(desktop_file_name)
        self.mobile = self.read_file(mobile_file_name)
        self.process_log()

    @staticmethod
    def read_file(file_name: str) -> Set[str]:
        with open(file_name, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())

    def get_line_client(self, line_ua: str) -> str:
        if line_ua in self.desktop:
            return 'desktop'
        if line_ua in self.mobile:
            return 'mobile'
        return 'unknown'

    @staticmethod
    def get_line_fields(line: str) -> List[str]:
        fields = []
        temp = []
        inside_quotes = False

        for token in line.strip().split(' '):
            if token.startswith('"') and not token.endswith('"'):
                temp = [token[1:]]
                inside_quotes = True
            elif inside_quotes:
                if token.endswith('"'):
                    temp.append(token[:-1])
                    fields.append(' '.join(temp))
                    inside_quotes = False
                else:
                    temp.append(token)
            else:
                fields.append(token)

        return fields

    def process_log(self):
        for line in sys.stdin:
            fields = self.get_line_fields(line)
            if len(fields) < 7:
                continue  # защита от некорректных строк
            user_agent = fields[-1]
            client = self.get_line_client(user_agent)
            print(f"{client} {line.strip()}")


if __name__ == '__main__':
    LogMobileDistinguisher('d.txt', 'm.txt')

