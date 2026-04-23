import json
import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict
import os


class DataStorage:

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_json(self, news_data: List[Dict], filename: str = None):
        if not filename:
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)

        print(f"Сохранено в JSON: {filepath}")
        return filepath

    def save_csv(self, news_data: List[Dict], filename: str = None):
        if not filename:
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            if news_data:
                writer = csv.DictWriter(f, fieldnames=news_data[0].keys())
                writer.writeheader()
                writer.writerows(news_data)

        print(f"Сохранено в CSV: {filepath}")
        return filepath

    def save_excel(self, news_data: List[Dict], filename: str = None):
        """Сохраняет в Excel"""
        if not filename:
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        filepath = os.path.join(self.data_dir, filename)
        df = pd.DataFrame(news_data)
        df.to_excel(filepath, index=False)

        print(f"Сохранено в Excel: {filepath}")
        return filepath

    def print_summary(self, news_data: List[Dict]):
        if not news_data:
            print("Новости не найдены")
            return

        print("\n" + "=" * 80)
        print(f"НАЙДЕНО НОВОСТЕЙ: {len(news_data)}")
        print("=" * 80)

        for i, news in enumerate(news_data[:10], 1):
            print(f"\n{i}. {news['title'][:100]}")
            print(f"   Источник: {news['source']}")
            print(f"   {news['link']}")
            if news['summary']:
                print(f"   {news['summary'][:150]}...")

        if len(news_data) > 10:
            print(f"\n... и еще {len(news_data) - 10} новостей")