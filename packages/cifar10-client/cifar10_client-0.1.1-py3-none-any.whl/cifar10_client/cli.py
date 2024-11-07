import click
from rich.console import Console
from rich.table import Table
from pathlib import Path
from .client import CIFAR10Client
import os

console = Console()

@click.command()
@click.argument('images', nargs=-1, type=click.Path(exists=True))
@click.option('--url', default='http://16.171.55.173:5000',
              help='API base URL')
@click.option('--top3', is_flag=True, help='Show top 3 predictions')
@click.option('--batch', is_flag=True, help='Process multiple images')
def main(images, url, top3, batch):
    """Predict image classes using CIFAR-10 API."""
    if not images:
        console.print("[red]Error:[/red] Please provide at least one image path")
        return

    client = CIFAR10Client(url)
    
    try:
        if batch:
            results = client.predict_batch(list(images))
            table = Table(title="Batch Predictions")
            table.add_column("File")
            table.add_column("Predictions")
            table.add_column("Confidences")
            
            for item in results['results']:
                preds = '\n'.join(item['predictions'])
                confs = '\n'.join(f"{conf}%" for conf in item['confidences'])
                table.add_row(item['filename'], preds, confs)
                
            console.print(table)
            
        elif top3:
            for image in images:
                result = client.predict_top3(image)
                table = Table(title=f"Top 3 Predictions - {Path(image).name}")
                table.add_column("Class")
                table.add_column("Confidence")
                
                for pred, conf in zip(result['predictions'], result['confidences']):
                    table.add_row(pred, f"{conf}%")
                    
                console.print(table)
                console.print()
                
        else:
            for image in images:
                result = client.predict_single(image)
                console.print(f"\n[bold]{Path(image).name}[/bold]")
                console.print(
                    f"Prediction: [green]{result['prediction']}[/green] "
                    f"([blue]{result['confidence']}%[/blue])"
                )
                
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")

if __name__ == '__main__':
    main()