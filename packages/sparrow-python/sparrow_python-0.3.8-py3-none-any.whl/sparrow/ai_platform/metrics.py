import os
from tabulate import tabulate
from datetime import datetime
from sparrow import yaml_dump
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class MetricsCalculator:
    def __init__(self, df: "DataFrame", pred_col: str = 'predict', label_col: str = 'label', include_macro_micro_avg=False):
        self.df = df
        self.y_pred = df[pred_col]
        self.y_true = df[label_col]
        self.all_labels = sorted(list(set(self.y_true.unique()).union(set(self.y_pred.unique()))))
        self.include_macro_micro_avg = include_macro_micro_avg
        self.metrics = self._calculate_metrics()

    def plot_confusion_matrix(self, save_path: str = None, figsize=(10, 8), font_scale=1.2):
        import matplotlib.pyplot as plt
        import seaborn as sns
        # 计算混淆矩阵
        conf_matrix = self.metrics['confusion_matrix']

        # 设置绘图的大小和风格
        plt.figure(figsize)
        sns.set_theme(font_scale=font_scale)

        # 绘制热力图
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=self.all_labels,
                    yticklabels=self.all_labels)

        # 设置标题和轴标签
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted Labels")
        plt.ylabel("True Labels")

        # 保存或显示图表
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def _calculate_metrics(self):
        from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix, \
            classification_report
        # 计算准确率
        accuracy = accuracy_score(self.y_true, self.y_pred)

        # 计算每个类别的精确率和召回率
        precision = precision_score(self.y_true, self.y_pred, labels=self.all_labels, average='weighted',
                                    zero_division=0)
        recall = recall_score(self.y_true, self.y_pred, labels=self.all_labels, average='weighted', zero_division=0)

        # 计算混淆矩阵
        conf_matrix = confusion_matrix(self.y_true, self.y_pred, labels=self.all_labels)

        # 计算每个类别的精确率、召回率、F1分数等
        report = classification_report(self.y_true, self.y_pred, labels=self.all_labels, output_dict=True,
                                       zero_division=0)

        # 移除宏平均和微平均，默认只保留加权平均
        if not self.include_macro_micro_avg:
            report = {label: metrics for label, metrics in report.items() if
                      label in self.all_labels or label == 'weighted avg'}

        # 返回结果
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'confusion_matrix': conf_matrix,
            'classification_report': report
        }

    def get_metrics(self):
        return self.metrics

    def format_classification_report_as_markdown(self):
        report = self.metrics['classification_report']
        header = "| Label | Precision | Recall | F1-score | Support |\n"
        separator = "|-------|-----------|--------|----------|---------|\n"
        rows = []
        for label, metrics in report.items():
            if isinstance(metrics, dict):
                rows.append(
                    f"| {label} | {metrics['precision']:.2f} | {metrics['recall']:.2f} | {metrics['f1-score']:.2f} | {metrics['support']:.0f} |")
        return header + separator + "\n".join(rows)

    def format_confusion_matrix_as_markdown(self):
        matrix = self.metrics['confusion_matrix']
        labels = self.all_labels
        header = "| | " + " | ".join(labels) + " |\n"
        separator = "|---" + "|---" * len(labels) + "|\n"
        rows = []
        for i, row in enumerate(matrix):
            rows.append(f"| {labels[i]} | " + " | ".join(map(str, row)) + " |")
        return header + separator + "\n".join(rows)


def save_pred_metrics(df, pred_col: str, label_col: str, record_folder='record', config=None, prompt=None):
    """ 保存预测结果的指标概览和分类报告 """
    metrics_calculator = MetricsCalculator(df, pred_col=pred_col, label_col=label_col)
    metrics = metrics_calculator.get_metrics()

    table = [["指标概览", "Accuracy", "Precision", "Recall"],
             ["值", metrics['accuracy'], metrics['precision'], metrics['recall']]]
    md = tabulate(table, headers="firstrow", tablefmt="github")
    metrics_md = metrics_calculator.format_classification_report_as_markdown()
    confusion_matrix_md = metrics_calculator.format_confusion_matrix_as_markdown()
    md += (f"\n### Classification Report\n{metrics_md}\n"
           f"\n{confusion_matrix_md}")
    now = datetime.now().strftime("%m月%d日%H时%M分%S秒")
    record_folder = Path(record_folder)
    record_folder = record_folder/f'记录时间-{now}'
    record_folder.mkdir(parents=True, exist_ok=True)
    console = Console()
    console.print(Markdown(md))

    # save files:
    with open(os.path.join(record_folder, 'metrics.md'), 'w', encoding='utf-8') as f:
        f.write(md)

    if prompt:
        yaml_dump(os.path.join(record_folder, 'prompt.yaml'), prompt)
    if config:
        yaml_dump(os.path.join(record_folder, 'config.yaml'), config)

    result_path = os.path.join(record_folder, 'result.xlsx')
    df.to_excel(result_path, index=False)

    bad_case_df = df[df[pred_col] != df[label_col]]
    bad_case_df.to_excel(os.path.join(record_folder, 'bad_case.xlsx'), index=False)

if __name__ == "__main__":
    import pandas as pd
    # 示例使用
    data = {
        'predict': ['cat', 'dog', 'cat', 'cat', 'dog', 'bird'],
        'label': ['cat', 'dog', 'dog', 'cat', 'dog', 'cat']
    }
    df = pd.DataFrame(data)

    metrics_calculator = MetricsCalculator(df)
    metrics = metrics_calculator.get_metrics()

    print("Accuracy:", metrics['accuracy'])
    print("Precision:", metrics['precision'])
    print("Recall:", metrics['recall'])
    print("\nClassification Report (Markdown Format):\n")
    print(metrics_calculator.format_classification_report_as_markdown())
    print("\nConfusion Matrix (Markdown Format):\n")
    print(metrics_calculator.format_confusion_matrix_as_markdown())
    metrics_calculator.plot_confusion_matrix()
    save_pred_metrics(df, pred_col='predict', label_col='label')